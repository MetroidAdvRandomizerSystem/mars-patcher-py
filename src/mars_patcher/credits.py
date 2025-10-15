from mars_patcher.constants.credits import (
    LINE_TYPE_VALS,
    TEXT_LINE_TYPES,
    LineType,
)
from mars_patcher.mf.auto_generated_types import MarsschemamfCreditstextItem
from mars_patcher.rom import Rom

FULL_LINE_LEN = 36
LINE_WIDTH = 30


class CreditsLine:
    LINE_TYPE_ENUMS = {
        "Blank": LineType.BLANK,
        "Blue": LineType.BLUE,
        "Red": LineType.RED,
        "White1": LineType.WHITE1,
        "White2": LineType.WHITE2,
    }

    def __init__(
        self,
        line_type: LineType,
        blank_lines: int = 0,
        text: str | None = None,
        centered: bool = True,
    ):
        self.line_type = line_type
        self.blank_lines = blank_lines
        self.text = text
        self.centered = centered

    @classmethod
    def from_json(cls, data: MarsschemamfCreditstextItem) -> "CreditsLine":
        line_type = cls.LINE_TYPE_ENUMS[data["LineType"]]
        blank_lines = data.get("BlankLines", 0)
        text = data.get("Text")
        centered = data.get("Centered", True)
        return CreditsLine(line_type, blank_lines, text, centered)


def write_credits_lines(rom: Rom, pointer: int, orig_length: int, lines: list[CreditsLine]) -> None:
    credits_bytes = bytearray()
    for line in lines:
        # Add bytes indicating line type and number of blank lines
        lt_val = LINE_TYPE_VALS[line.line_type]
        line_bytes = bytearray([lt_val, line.blank_lines])
        if line.line_type in TEXT_LINE_TYPES and line.text:
            text = line.text
            if line.centered:
                spacing = " " * ((LINE_WIDTH - len(text)) // 2)
                text = spacing + text
            line_bytes.extend(text.encode("ascii"))
        # Pad line to full line length
        remaining = FULL_LINE_LEN - len(line_bytes)
        if remaining < 0:
            raise ValueError(f"Line too long: {line_bytes}")
        line_bytes.extend(b"\x00" * remaining)
        credits_bytes += line_bytes
    # Write to ROM
    addr = rom.read_ptr(pointer)
    rom.write_repointable_data(addr, orig_length, credits_bytes, [pointer])
