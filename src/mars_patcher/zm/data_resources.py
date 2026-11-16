from importlib import resources
from importlib.resources.abc import Traversable

import mars_patcher.zm as zm_module


def get_data_resource(*path: str) -> Traversable:
    return resources.files(zm_module).joinpath("data", *path)
