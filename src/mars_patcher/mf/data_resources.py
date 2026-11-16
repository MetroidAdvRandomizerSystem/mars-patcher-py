from importlib import resources
from importlib.resources.abc import Traversable

import mars_patcher.mf as mf_module


def get_data_resource(*path: str) -> Traversable:
    # Maybe use module instead of hardcoded package path?
    return resources.files(mf_module).joinpath("data", *path)
