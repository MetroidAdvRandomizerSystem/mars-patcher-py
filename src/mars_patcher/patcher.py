import json
import typing
from collections.abc import Callable
from os import PathLike

from jsonschema import validate

from mars_patcher.auto_generated_types import MarsSchema
from mars_patcher.color_spaces import RgbBitSize, RgbColor
from mars_patcher.connections import Connections
from mars_patcher.credits import write_credits
from mars_patcher.data import get_data_path
from mars_patcher.door_locks import set_door_locks
from mars_patcher.item_patcher import ItemPatcher, set_required_metroid_count, set_tank_increments
from mars_patcher.level_edits import apply_level_edits
from mars_patcher.locations import LocationSettings
from mars_patcher.minimap import apply_base_minimap_edits, apply_minimap_edits
from mars_patcher.misc_patches import (
    apply_anti_softlock_edits,
    apply_base_patch,
    apply_pbs_without_bombs,
    apply_reveal_hidden_tiles,
    apply_reveal_unexplored_doors,
    apply_unexplored_map,
    change_missile_limit,
    disable_demos,
    disable_music,
    disable_sound_effects,
    skip_door_transitions,
    stereo_default,
)
from mars_patcher.navigation_text import NavigationText
from mars_patcher.random_palettes import (
    MF_TILESET_ALT_PAL_ROWS,
    Palette,
    PaletteRandomizer,
    PaletteSettings,
)
from mars_patcher.rom import Rom
from mars_patcher.room_names import write_room_names
from mars_patcher.starting import set_starting_items, set_starting_location
from mars_patcher.text import write_seed_hash


def validate_patch_data(patch_data: dict) -> MarsSchema:
    """
    Validates whether the specified patch_data satisfies the schema for it.

    Raises:
        ValidationError: If the patch data does not satisfy the schema.
    """
    with open(get_data_path("schema.json")) as f:
        schema = json.load(f)
    validate(patch_data, schema)
    return typing.cast("MarsSchema", patch_data)


def patch(
    input_path: str | PathLike[str],
    output_path: str | PathLike[str],
    patch_data: MarsSchema,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized Fusion game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        input_path: The path to an unmodified Metroid Fusion (U) ROM.
        output_path: The path where the randomized Fusion ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
            This function assumes that it satisfies the needed schema. To validate it, use
            validate_patch_data().
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Load input rom
    rom = Rom(input_path)

    # Apply base asm patch first
    apply_base_patch(rom)

    # Softlock edits need to be done early to prevent later edits messing things up.
    if patch_data.get("AntiSoftlockRoomEdits"):
        apply_anti_softlock_edits(rom)

    # Randomize palettes - palettes are randomized first in case the item
    # patcher needs to copy tilesets
    if "Palettes" in patch_data:
        status_update("Randomizing palettes...", -1)
        pal_settings = PaletteSettings.from_json(patch_data["Palettes"])
        pal_randomizer = PaletteRandomizer(rom, pal_settings)
        pal_randomizer.randomize()

    # Load locations and set assignments
    status_update("Writing item assignments...", -1)
    loc_settings = LocationSettings.initialize()
    loc_settings.set_assignments(patch_data["Locations"])
    item_patcher = ItemPatcher(rom, loc_settings)
    item_patcher.write_items()

    # Required metroid count
    set_required_metroid_count(rom, patch_data["RequiredMetroidCount"])

    # Starting location
    if "StartingLocation" in patch_data:
        status_update("Writing starting location...", -1)
        set_starting_location(rom, patch_data["StartingLocation"])

    # Starting items
    if "StartingItems" in patch_data:
        status_update("Writing starting items...", -1)
        set_starting_items(rom, patch_data["StartingItems"])

    # Tank increments
    if "TankIncrements" in patch_data:
        status_update("Writing tank increments...", -1)
        set_tank_increments(rom, patch_data["TankIncrements"])

    # Elevator connections
    conns = None
    if "ElevatorConnections" in patch_data:
        status_update("Writing elevator connections...", -1)
        conns = Connections(rom)
        conns.set_elevator_connections(patch_data["ElevatorConnections"])

    # Sector shortcuts
    if "SectorShortcuts" in patch_data:
        status_update("Writing sector shortcuts...", -1)
        if conns is None:
            conns = Connections(rom)
        conns.set_shortcut_connections(patch_data["SectorShortcuts"])

    # Hints
    if nav_text := patch_data.get("NavigationText", {}):
        status_update("Writing navigation text...", -1)
        navigation_text = NavigationText.from_json(nav_text)
        navigation_text.write(rom)

    if nav_locks := patch_data.get("NavStationLocks", {}):
        status_update("Writing navigation locks...", -1)
        NavigationText.apply_hint_security(rom, nav_locks)

    # Room Names
    if room_names := patch_data.get("RoomNames", []):
        status_update("Writing room names...", -1)
        write_room_names(rom, room_names)

    # Credits
    if credits_text := patch_data.get("CreditsText", []):
        status_update("Writing credits text...", -1)
        write_credits(rom, credits_text)

    # Misc patches

    if patch_data.get("DisableDemos"):
        disable_demos(rom)

    if patch_data.get("SkipDoorTransitions"):
        skip_door_transitions(rom)

    if patch_data.get("StereoDefault", True):
        stereo_default(rom)

    if patch_data.get("DisableMusic"):
        disable_music(rom)

    if patch_data.get("DisableSoundEffects"):
        disable_sound_effects(rom)

    if "MissileLimit" in patch_data:
        change_missile_limit(rom, patch_data["MissileLimit"])

    if patch_data.get("PowerBombsWithoutBombs"):
        apply_pbs_without_bombs(rom)

    if patch_data.get("UnexploredMap"):
        apply_unexplored_map(rom)

        if not patch_data.get("HideDoorsOnMinimap", False):
            apply_reveal_unexplored_doors(rom)

    if patch_data.get("RevealHiddenTiles"):
        apply_reveal_hidden_tiles(rom)

    if "LevelEdits" in patch_data:
        apply_level_edits(rom, patch_data["LevelEdits"])

    # Apply base minimap edits
    apply_base_minimap_edits(rom)

    # Apply JSON minimap edits
    if "MinimapEdits" in patch_data:
        apply_minimap_edits(rom, patch_data["MinimapEdits"])

    # Door locks
    if door_locks := patch_data.get("DoorLocks", []):
        status_update("Writing door locks...", -1)
        set_door_locks(rom, door_locks)

    write_seed_hash(rom, patch_data["SeedHash"])

    fuck_with_colors(rom)

    rom.save(output_path)
    status_update(f"Output written to {output_path}", -1)

    # Remove once in public beta
    print("------")
    print("Report all issues to the Randovania Discord Server (https://discord.gg/M23gCxj6fw)")
    print(
        "or alternatively this project's issue page (https://github.com/MetroidAdvRandomizerSystem/mars-patcher/issues)"
    )
    print("Thank you")


def fuck_with_colors(rom: Rom) -> None:
    # TODO: clean up
    def round_down(num: int, divisor: int) -> int:
        return num - (num % divisor)

    def adjust_hsv_and_return_as_rgb(col: RgbColor, h: float, s: float, v: float) -> RgbColor:
        color = col.hsv()
        color.hue *= h
        color.hue = color.hue % 360
        color.saturation *= s
        if color.saturation > 1:
            color.saturation = 1
        color.value *= v
        if color.value > 1:
            color.value = 1

        final = color.rgb()
        return final

    # Always brighten gray map bg to provide better contrast
    gray = RgbColor(153, 153, 153, RgbBitSize.Rgb8)
    minimap_pal = Palette(1, rom, 0x3E415C)
    minimap_pal.colors[12] = gray
    minimap_pal.write(rom, 0x3E415C)
    map_pal = Palette(1, rom, 0x5657A8)
    map_pal.colors[2] = map_pal.colors[3] = gray
    map_pal.write(rom, 0x5657A8)

    blue_color = RgbColor(255, 41, 41, RgbBitSize.Rgb8)
    green_color = RgbColor(156, 41, 251, RgbBitSize.Rgb8)
    yellow_color = RgbColor(40, 248, 40, RgbBitSize.Rgb8)
    red_color = RgbColor(40, 84, 248, RgbBitSize.Rgb8)
    purple_map_color = RgbColor(255, 99, 34, RgbBitSize.Rgb8)

    base_colors = {
        8: blue_color,
        10: green_color,
        12: yellow_color,
        14: red_color,
    }

    mods = {
        0: (1, 1, 1),
        1: (1.0063, 1.1923, 0.7420),
        2: (1.0305, 1.1923, 0.5162),
        5: (0.9710, 0.6154, 1),
    }
    mods[3] = mods[1]
    mods[4] = mods[0]

    mods_alt = {
        0: (1.0939, 1.1923, 0.6452),
        1: (1.1415, 1.1923, 0.4839),
        2: (1.1732, 1.1923, 0.3226),
        5: (1.1014, 0.9062, 0.8065),
    }
    mods_alt[3] = mods_alt[1]
    mods_alt[4] = mods_alt[0]

    # Patch common door graphics
    def fix_door_colors(addr: int, rows: int) -> None:
        door_pal = Palette(rows, rom, addr)
        for index in range(rows):
            for col_index in range(8, 16):
                base_color = base_colors[round_down(col_index, 2)]
                if col_index % 2 == 0:
                    h, s, v = mods[index]
                else:
                    h, s, v = mods_alt[index]
                final_index = index * 16 + col_index
                final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
                door_pal.colors[final_index] = final
        door_pal.write(rom, addr)

    fix_door_colors(0x40807C, 1)  # common graphics for still/locked door
    fix_door_colors(0x40825C, 6)  # common graphics for animated door

    # Patch item palettes
    base_colors = {
        8: green_color,
        10: blue_color,
        12: yellow_color,
        14: red_color,
    }
    for address, offset in MF_TILESET_ALT_PAL_ROWS.items():
        pal = Palette(1, rom, address + (0x20 * offset))
        sp_h, sp_s, sp_v = mods_alt[2]
        pal.colors[7] = adjust_hsv_and_return_as_rgb(base_colors[8], sp_h, sp_s, sp_v)
        for col_index in range(8, 16):
            base_color = base_colors[round_down(col_index, 2)]
            if col_index % 2 == 0:
                h, s, v = mods_alt[0]
            else:
                h, s, v = mods[0]
            final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
            pal.colors[col_index] = final

        pal.write(rom, address + (0x20 * offset))

    # Patch map door palettes
    base_colors = {
        0: yellow_color,
        1: blue_color,
        2: green_color,
        3: red_color,
    }
    minimap_pal = Palette(3, rom, 0x5657A8)
    for row in range(3):
        # change green/purple bg color too
        if row == 1 or row == 2:
            for index in range(2, 4):
                base_color = base_colors[2]
                h, s, v = mods_alt[0]
                if row == 1:
                    base_color = purple_map_color
                    h, s, v = mods[0]
                final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
                minimap_pal.colors[row * 16 + index] = final

        for index in range(7, 16):
            col_index = index - 7
            h, s, v = mods[0]
            base_color = base_colors[col_index % 4]
            final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
            minimap_pal.colors[row * 16 + index] = final
    minimap_pal.write(rom, 0x5657A8)

    # Change animated bg colors
    anim_pal = Palette(2, rom, 0x57BCD4)
    for row in range(2):
        for index in range(5):
            h, s, v = mods_alt[index]
            base_color = base_colors[2]
            if row == 0:
                base_color = purple_map_color
                h, s, v = mods[index]
            final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
            anim_pal.colors[index + row * 16] = final
    anim_pal.write(rom, 0x57BCD4)

    # Change minimap color too
    minimap_pal = Palette(1, rom, 0x3E415C)
    # Green BG + Green Door
    for index in range(2, 5):
        base_color = base_colors[2]
        h, s, v = mods_alt[index - 2]
        final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
        minimap_pal.colors[index] = final
    # Purple BG
    base_color = purple_map_color
    h, s, v = mods[0]
    final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
    minimap_pal.colors[13] = final
    # Doors
    for index in [6, 7, 8, 10, 11, 14]:
        if index == 6 or index == 10:
            base_color = base_colors[3]
        elif index == 7 or index == 11:
            base_color = base_colors[0]
        else:  # index == 8 or index == 14
            base_color = base_colors[1]

        if index < 10:
            h, s, v = mods[0]
        else:
            h, s, v = mods_alt[0]

        final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
        minimap_pal.colors[index] = final

    minimap_pal.write(rom, 0x3E415C)

    # Patch minimap keylock icon palette    # TODO WARP and STATUS icon flash a bit, probably need to change 0x565CA8
    base_colors = {
        2: blue_color,
        5: green_color,
        8: yellow_color,
        11: red_color,
    }
    keylock_pal = Palette(1, rom, 0x565C28)
    for index in range(2, 14):
        col_index = index - 2
        if col_index % 3 == 0:
            h, s, v = mods[5]
        elif col_index % 3 == 1:
            h, s, v = mods[0]
        else:  # % 3 == 2
            h, s, v = mods_alt[0]

        base_color = base_colors[round_down(col_index, 3) + 2]
        final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
        keylock_pal.colors[col_index + 2] = final
    keylock_pal.write(rom, 0x565C28)

    # Change x colors
    base_colors = {0: red_color, 1: green_color, 2: yellow_color}
    x_pal = Palette(3, rom, 0x3E40DC)
    for row in range(3):
        for index in range(11, 14):
            if index == 11:
                h, s, v = mods[5]
            elif index == 12:
                h, s, v = mods[0]
            else:  # index == 13
                h, s, v = mods_alt[1]

            base_color = base_colors[row]
            final = adjust_hsv_and_return_as_rgb(base_color, h, s, v)
            x_pal.colors[row * 16 + index] = final

    x_pal.write(rom, 0x3E40DC)

    # TODO: change colored nav text
    # TODO: map doesnt have grid colors changed
    # TODO: change the other item palette?
