from mars_patcher.credits import CreditsLine, write_credits_lines
from mars_patcher.mf.auto_generated_types import MarsschemamfCreditstextItem
from mars_patcher.mf.constants.credits_lines import (
    FUSION_STAFF_LINES,
    MARS_CREDITS,
    RDV_CREDITS,
)
from mars_patcher.rom import Rom

CREDITS_POINTER = 0xA231C
CREDITS_LEN = 0x2B98


def write_credits(rom: Rom, data: list[MarsschemamfCreditstextItem]) -> None:
    # MARS credits
    lines = [CreditsLine(*line) for line in MARS_CREDITS]
    # RDV credits
    lines += [CreditsLine(*line) for line in RDV_CREDITS]
    # Custom credits
    lines += [CreditsLine.from_json(d) for d in data]
    # Fusion staff credits
    lines += [CreditsLine(*line) for line in FUSION_STAFF_LINES]
    # Write lines to ROM
    write_credits_lines(rom, CREDITS_POINTER, CREDITS_LEN, lines)
