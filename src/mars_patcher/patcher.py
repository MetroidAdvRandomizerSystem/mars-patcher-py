from collections.abc import Callable
from os import PathLike

from mars_patcher.mf.patcher import patch_mf
from mars_patcher.rom import Rom
from mars_patcher.zm.patcher import patch_zm


def patch(
    input_path: str | PathLike[str],
    output_path: str | PathLike[str],
    patch_data: dict,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized GBA Metroid game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        input_path: The path to an unmodified GBA Metroid (U) ROM.
        output_path: The path where the randomized GBA Metroid ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Load input rom
    rom = Rom(input_path)

    if rom.is_mf():
        patch_mf(rom, output_path, patch_data, status_update)
    elif rom.is_zm():
        patch_zm(rom, output_path, patch_data, status_update)
    else:
        raise ValueError(rom)
