from enum import Enum


class LineType(Enum):
    BLANK = 0
    BLUE = 1
    RED = 2
    WHITE1 = 3
    WHITE2 = 4
    COPYRIGHT1 = 5
    COPYRIGHT2 = 6
    COPYRIGHT3 = 7
    COPYRIGHT4 = 8
    END = 9


LINE_TYPE_VALS = {
    LineType.BLANK: 0x5,
    LineType.BLUE: 0x0,
    LineType.RED: 0x1,
    LineType.WHITE1: 0x3,
    LineType.WHITE2: 0x2,
    LineType.COPYRIGHT1: 0xA,
    LineType.COPYRIGHT2: 0xB,
    LineType.COPYRIGHT3: 0xC,
    LineType.COPYRIGHT4: 0xD,
    LineType.END: 0x6,
}

TEXT_LINE_TYPES = {LineType.BLUE, LineType.RED, LineType.WHITE1, LineType.WHITE2}
