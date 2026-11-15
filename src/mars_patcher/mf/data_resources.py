from importlib import resources
from importlib.resources.abc import Traversable


def get_data_resource(*path: str) -> Traversable:
    # Maybe use module instead of hardcoded package path?
    return resources.files("mars_patcher.mf.data").joinpath(*path)
