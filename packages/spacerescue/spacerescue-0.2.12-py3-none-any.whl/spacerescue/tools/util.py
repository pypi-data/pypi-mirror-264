from functools import lru_cache, wraps
from importlib import resources as impresources

import numpy as np
import yaml


def first_not_none(a: list):
    return next((x for x in a if x is not None), None)


def wait_while_true(pred):
    while pred():
        pass


def call_and_return(func, x):
    func(x)
    return x


def np_cache_method(function):
    @lru_cache()
    def cached_wrapper(self, hashable_array):
        array = np.array(hashable_array)
        return function(self, array)

    @wraps(function)
    def wrapper(self, array):
        return cached_wrapper(self, tuple(array))

    # copy lru_cache attributes over too
    wrapper.cache_info = cached_wrapper.cache_info  # type: ignore
    wrapper.cache_clear = cached_wrapper.cache_clear  # type: ignore

    return wrapper


def load_yaml(file: str):
    with open(file, "r") as f:
        return yaml.safe_load(f)


def load_res_yaml(res: impresources.Package, file: str):
    inp_file = impresources.files(res) / file
    with inp_file.open("r") as f:
        return yaml.safe_load(f)


def load_lines(file: str):
    with open(file, "r") as f:
        return [line.rstrip("\n") for line in f]


def load_res_lines(res: impresources.Package, file: str) -> list[str]:
    inp_file = impresources.files(res) / file
    with inp_file.open("r") as f:
        return [line.rstrip("\n") for line in f]


def secret_token(len: int) -> str:
    token = ""
    for i in range(len):
        id = np.random.randint(0, 256)
        token += "{:02x}".format(id)
    return token
