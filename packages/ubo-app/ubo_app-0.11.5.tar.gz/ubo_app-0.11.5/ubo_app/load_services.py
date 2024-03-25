# ruff: noqa: D100, D101, D102, D103, D104, D105, D107
from __future__ import annotations

import asyncio
import importlib
import importlib.abc
import importlib.util
import os
import sys
import threading
import traceback
import uuid
from importlib.machinery import PathFinder, SourceFileLoader
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Coroutine, Sequence, cast

from redux import CombineReducerRegisterAction, FinishEvent, ReducerType

from ubo_app.constants import DEBUG_MODE, SERVICES_PATH
from ubo_app.logging import logger

if TYPE_CHECKING:
    from importlib.machinery import ModuleSpec
    from types import ModuleType

ROOT_PATH = Path(__file__).parent
REGISTERED_PATHS: dict[Path, UboServiceThread] = {}


# Customized module finder and module loader for ubo services to avoid mistakenly
# loading conflicting names in different services.
# This is a temporary hack until each service runs in its own process.
class UboServiceModuleLoader(SourceFileLoader):
    cache: ClassVar[dict[str, ModuleType]] = {}

    @property
    def cache_id(self: UboServiceModuleLoader) -> str:
        return f'{self.path}:{self.name}'

    def create_module(
        self: UboServiceModuleLoader,
        spec: ModuleSpec,
    ) -> ModuleType | None:
        _ = spec
        if self.cache_id in UboServiceModuleLoader.cache:
            return UboServiceModuleLoader.cache[self.cache_id]
        return None

    def exec_module(self: UboServiceModuleLoader, module: ModuleType) -> None:
        if self.cache_id in UboServiceModuleLoader.cache:
            return
        super().exec_module(module)
        UboServiceModuleLoader.cache[self.cache_id] = module

    def get_filename(self: UboServiceModuleLoader, name: str | None = None) -> str:
        return super().get_filename(name.split(':')[-1] if name else name)


class UboServiceLoopLoader(importlib.abc.Loader):
    def __init__(self: UboServiceLoopLoader, service: UboServiceThread) -> None:
        self.service = service

    def exec_module(self: UboServiceLoopLoader, module: ModuleType) -> None:
        cast(Any, module).current_loop = lambda: self.service.loop
        cast(Any, module)._create_task = (  # noqa: SLF001
            lambda task: self.service.loop.call_soon_threadsafe(
                self.service.loop.create_task,
                task,
            )
        )
        cast(Any, module)._run_in_executor = (  # noqa: SLF001
            lambda executor, task, *args: self.service.loop.run_in_executor(
                executor,
                task,
                *args,
            )
        )

    def __repr__(self: UboServiceLoopLoader) -> str:
        return f'{self.service.path}'


class UboServiceFinder(importlib.abc.MetaPathFinder):
    def find_spec(
        self: UboServiceFinder,
        fullname: str,
        _: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        stack = traceback.extract_stack()
        matching_path = next(
            (
                registered_path
                for stack_path in stack[-2::-1]
                for registered_path in (*REGISTERED_PATHS.keys(), Path('/'))
                if stack_path.filename.startswith(registered_path.as_posix())
            ),
            None,
        )

        if matching_path in REGISTERED_PATHS:
            service = REGISTERED_PATHS[matching_path]
            module_name = f'{service.service_uid}:{fullname}'

            if fullname == 'ubo_app.utils.loop':
                return importlib.util.spec_from_loader(
                    module_name,
                    UboServiceLoopLoader(service),
                )

            spec = PathFinder.find_spec(
                fullname,
                [matching_path.as_posix()],
                target,
            )
            if spec and spec.origin:
                spec.name = module_name
                spec.loader = UboServiceModuleLoader(fullname, spec.origin)
            return spec
        return None


sys.meta_path.insert(0, UboServiceFinder())


class UboServiceThread(threading.Thread):
    def __init__(
        self: UboServiceThread,
        path: Path,
        white_list: Sequence[str] | None = None,
    ) -> None:
        name = path.name
        super().__init__()
        self.service_uid = f'{uuid.uuid4().hex}:{name}'
        self.name = name
        self.label = '<NOT SET>'
        self.service_id = '-not-set-'

        self.path = path
        self.white_list = white_list

        self.loop = asyncio.new_event_loop()
        self.module = None
        if DEBUG_MODE:
            self.loop.set_debug(enabled=True)

    def run(self: UboServiceThread) -> None:
        from ubo_app import store

        try:
            if self.path.exists():
                module_name = f'{self.service_uid}:ubo_handle'
                self.spec = PathFinder.find_spec(
                    'ubo_handle',
                    [self.path.as_posix()],
                    None,
                )
                if not self.spec or not self.spec.origin:
                    return
                self.spec.name = module_name
                self.spec.loader = UboServiceModuleLoader(
                    'ubo_handle',
                    self.spec.origin,
                )
                self.module = importlib.util.module_from_spec(self.spec)

        except Exception as exception:  # noqa: BLE001
            logger.error(f'Error loading "{self.path}"', exc_info=exception)

        asyncio.set_event_loop(self.loop)
        if self.module and self.spec and self.spec.loader:
            try:
                self.spec.loader.exec_module(self.module)
            except Exception as exception:  # noqa: BLE001
                logger.error(f'Error loading "{self.path}"', exc_info=exception)
                return

        store.subscribe_event(FinishEvent, self.stop)
        self.loop.run_forever()

    def stop(self: UboServiceThread) -> None:
        self.loop.call_soon_threadsafe(self.loop.stop)

    def __repr__(self: UboServiceThread) -> str:
        return f'<UboServiceThread id={self.name} label={self.label}>'


def register_service(
    service_id: str,
    label: str,
    reducer: ReducerType | None = None,
    init: Callable[[], None | Coroutine] | None = None,
) -> None:
    from ubo_app import store

    thread = threading.current_thread()
    if not isinstance(thread, UboServiceThread):
        logger.error(
            'Service registration outside of service thread',
            extra={
                'service_id': service_id,
                'label': label,
            },
        )
        return

    if service_id in os.environ.get('UBO_DISABLED_SERVICES', '').split(','):
        logger.info(
            'Skipping disabled ubo service',
            extra={
                'service_id': service_id,
                'label': label,
                'disabled_services': os.environ.get('UBO_DISABLED_SERVICES'),
            },
        )
        thread.stop()
        return

    if thread.white_list and service_id not in thread.white_list:
        logger.info(
            'Service is not in services white list',
            extra={
                'service_id': service_id,
                'label': label,
                'white_list': thread.white_list,
            },
        )
        thread.stop()
        return

    thread.label = label
    thread.service_id = service_id

    logger.info(
        'Registering ubo serivce',
        extra={
            'service_id': service_id,
            'label': label,
            'has_reducer': reducer is not None,
        },
    )

    if reducer is not None:
        store.dispatch(
            CombineReducerRegisterAction(
                _id=store.root_reducer_id,
                key=service_id,
                reducer=reducer,
            ),
        )

    if init is not None:
        result = init()
        if asyncio.iscoroutine(result):
            thread.loop.create_task(result)


def load_services(service_ids: Sequence[str] | None = None) -> None:
    for services_directory_path in [
        ROOT_PATH.joinpath('services').as_posix(),
        *SERVICES_PATH,
    ]:
        if Path(services_directory_path).is_dir():
            for service_path in Path(services_directory_path).iterdir():
                if not service_path.is_dir():
                    continue
                current_path = Path().absolute()
                os.chdir(service_path.as_posix())

                service = UboServiceThread(service_path, white_list=service_ids)
                REGISTERED_PATHS[service_path] = service
                service.start()

                os.chdir(current_path)
