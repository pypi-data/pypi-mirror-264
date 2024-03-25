from types import ModuleType
from multiprocessing import Process, Queue

import os
import time
import logging
import subprocess
import importlib


class DynamicModule:

    def __init__(self, module: ModuleType, timestamp: float):
        self.module = module
        self.timestamp = timestamp


class DynamicCode:

    def __init__(self, src: str):
        self.dynamic_package = self._import_dynamic_package(src)
        self.queue = Queue()
        self.last_result = None

    def validate_code(self) -> Process:
        p = Process(target=_validate_code_proc, args=(self.queue,))
        p.start()
        return p

    def get_validate_code_result(self) -> subprocess.CompletedProcess:
        return self.queue.get()

    def execute_code(self, id, context):
        self.dynamic_package = self._reload_dynamic_package(
            "brain", self.dynamic_package
        )
        self.last_result = self.dynamic_package["brain.brain"].module.think(id, context)
        return self.last_result

    def get_execute_code_result(self):
        return self.last_result

    def _import_dynamic_package(self, package_name: str, dynamic_package: dict = {}):
        packages = self._list_packages(package_name)
        for file, package in packages:
            dynamic_package = self._import_one_package(package, file, dynamic_package)
        return dynamic_package

    def _reload_dynamic_package(self, package_name: str, dynamic_package: dict):
        modules = self._list_packages(package_name)
        for file, package in modules:
            if package in dynamic_package.keys():
                timestamp = os.path.getmtime(file)
                if timestamp > dynamic_package[package].timestamp:
                    dynamic_package = self._reload_one_package(
                        package, timestamp, dynamic_package
                    )
            else:
                dynamic_package = self._import_one_package(
                    package, file, dynamic_package
                )
        return dynamic_package

    def _import_one_package(self, package: str, file: str, dynamic_package: dict):
        logging.debug(
            f"DEBUG: CODE: [{package}] Found a new module to load and monitor"
        )
        dynamic_package[package] = DynamicModule(
            importlib.import_module(package), os.path.getmtime(file)
        )
        return dynamic_package

    def _reload_one_package(
        self, package: str, timestamp: float, dynamic_package: dict
    ):
        logging.debug(f"DEBUG: CODE: [{package}] Found an existing module to reload")
        importlib.reload(dynamic_package[package].module)
        dynamic_package[package].timestamp = timestamp
        return dynamic_package

    def _list_packages(self, package_name: str):
        return [
            (os.path.join(package_name, file), f"{package_name}.{file[:-3]}")
            for file in os.listdir(package_name)
            if self._is_valid_module_name(os.path.join(package_name, file))
        ]

    def _is_valid_module_name(self, file: str):
        return file.endswith(".py") and os.path.isfile(file)


def _validate_code_proc(queue: Queue):
    result = subprocess.run(["coverage", "run", "--module", "pytest"])
    if result.returncode != 0:
        time.sleep(1)
        return queue.put(result)

    result = subprocess.run(
        [
            "coverage",
            "report",
            "--show-missing",
            "--skip-covered",
            "--fail-under=80",
            "--include=brain/*.py",
            "--omit=brain/__init__.py",
        ]
    )
    if result.returncode != 0:
        time.sleep(1)
        return queue.put(result)

    time.sleep(1)
    return queue.put(result)
