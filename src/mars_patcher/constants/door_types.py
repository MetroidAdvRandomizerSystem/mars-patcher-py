from enum import IntEnum, auto


class DoorType(IntEnum):
    AREA_CONNECTION = 1
    NO_HATCH = auto()
    OPEN_HATCH = auto()
    LOCKABLE_HATCH = auto()

    REMOVE_MOTHERSHIP = auto()
    """Zero Mission only."""
    SET_MOTHERSHIP = auto()
    """Zero Mission only."""
