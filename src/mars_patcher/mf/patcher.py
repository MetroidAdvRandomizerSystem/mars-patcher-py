import json
from collections.abc import Callable
from os import PathLike

from mars_patcher.color_spaces import RgbBitSize, RgbColor
from mars_patcher.level_edits import apply_level_edits
from mars_patcher.mf.auto_generated_types import MarsSchemaMF
from mars_patcher.mf.connections import Connections
from mars_patcher.mf.constants.palettes import MF_TILESET_ALT_PAL_ROWS
from mars_patcher.mf.credits import write_credits
from mars_patcher.mf.data import get_data_path
from mars_patcher.mf.door_locks import set_door_locks
from mars_patcher.mf.item_patcher import (
    ItemPatcher,
    set_required_metroid_count,
    set_tank_increments,
)
from mars_patcher.mf.locations import LocationSettings
from mars_patcher.mf.misc_patches import (
    apply_accessibility_patch,
    apply_alternative_health_layout,
    apply_base_patch,
    apply_instant_unmorph_patch,
    apply_nerf_gerons,
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
from mars_patcher.mf.navigation_text import NavigationText
from mars_patcher.mf.room_names import write_room_names
from mars_patcher.mf.starting import set_starting_items, set_starting_location
from mars_patcher.minimap import apply_minimap_edits
from mars_patcher.palette import Palette
from mars_patcher.random_palettes import PaletteRandomizer, PaletteSettings
from mars_patcher.rom import Rom
from mars_patcher.text import write_seed_hash
from mars_patcher.titlescreen_text import write_title_text


def patch_mf(
    rom: Rom,
    output_path: str | PathLike[str],
    patch_data: MarsSchemaMF,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized Fusion game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        rom: Rom object for an unmodified Metroid Fusion (U) ROM.
        output_path: The path where the randomized Fusion ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
            This function assumes that it satisfies the needed schema. To validate it, use
            validate_patch_data_mf().
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Apply base asm patch first
    apply_base_patch(rom)

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
    if patch_data.get("AccessibilityPatches"):
        apply_accessibility_patch(rom)

    if patch_data.get("DisableDemos"):
        disable_demos(rom)

    if patch_data.get("InstantUnmorph"):
        apply_instant_unmorph_patch(rom)

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

    if patch_data.get("NerfGerons"):
        apply_nerf_gerons(rom)

    if patch_data.get("UseAlternativeHudHealthLayout"):
        apply_alternative_health_layout(rom)

    if patch_data.get("UnexploredMap"):
        apply_unexplored_map(rom)

        if not patch_data.get("HideDoorsOnMinimap", False):
            apply_reveal_unexplored_doors(rom)

    if patch_data.get("RevealHiddenTiles"):
        apply_reveal_hidden_tiles(rom)

    if "LevelEdits" in patch_data:
        apply_level_edits(rom, patch_data["LevelEdits"])

    # Apply base minimap edits
    with open(get_data_path("base_minimap_edits.json")) as f:
        edits_dict = json.load(f)
    apply_minimap_edits(rom, edits_dict)

    # Apply JSON minimap edits
    if "MinimapEdits" in patch_data:
        apply_minimap_edits(rom, patch_data["MinimapEdits"])

    # Door locks
    if door_locks := patch_data.get("DoorLocks", []):
        status_update("Writing door locks...", -1)
        set_door_locks(rom, door_locks)

    write_seed_hash(rom, patch_data["SeedHash"])

    fuck_with_colors(rom)

    # Title-screen text
    if title_screen_text := patch_data.get("TitleText"):
        status_update("Writing title screen text...", -1)
        write_title_text(rom, title_screen_text)

    rom.save(output_path)
    status_update(f"Output written to {output_path}", -1)


def fuck_with_colors(rom: Rom) -> None:
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

    class ColorVariations:
        normal: RgbColor
        darker: RgbColor
        darkest: RgbColor
        brighter: RgbColor
        alt_normal: RgbColor
        alt_darker: RgbColor
        alt_darkest: RgbColor
        alt_brighter: RgbColor

        def __init__(self, base_color: RgbColor) -> None:
            self.normal = base_color

            mods = [
                (1, 1, 1),  # normal
                (1.0063, 1.1923, 0.7420),  # darker
                (1.0305, 1.1923, 0.5162),  # darkest
                (0.9710, 0.6154, 1),  # brighter
                (1.0939, 1.1923, 0.6452),  # alt_normal
                (1.1415, 1.1923, 0.4839),  # alt_darker
                (1.1732, 1.1923, 0.3226),  # alt_darkest
                (1.1014, 0.9062, 0.8065),  # alt_brighter
            ]

            self.normal = adjust_hsv_and_return_as_rgb(base_color, *mods[0])
            self.darker = adjust_hsv_and_return_as_rgb(base_color, *mods[1])
            self.darkest = adjust_hsv_and_return_as_rgb(base_color, *mods[2])
            self.brighter = adjust_hsv_and_return_as_rgb(base_color, *mods[3])

            self.alt_normal = adjust_hsv_and_return_as_rgb(base_color, *mods[4])
            self.alt_darker = adjust_hsv_and_return_as_rgb(base_color, *mods[5])
            self.alt_darkest = adjust_hsv_and_return_as_rgb(base_color, *mods[6])
            self.alt_brighter = adjust_hsv_and_return_as_rgb(base_color, *mods[7])

    # Always brighten gray map bg to provide better contrast
    # TODO: move this to asm?
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

    blues = ColorVariations(blue_color)
    greens = ColorVariations(green_color)
    yellows = ColorVariations(yellow_color)
    reds = ColorVariations(red_color)
    purples = ColorVariations(purple_map_color)

    # Palettes
    palettes_to_change: dict[int, dict[int, dict[int, RgbColor]]] = {}
    door_palettes = {
        # still
        0x40807C: {
            0: {
                8: blues.normal,
                9: blues.alt_normal,
                10: greens.normal,
                11: greens.alt_normal,
                12: yellows.normal,
                13: yellows.alt_normal,
                14: reds.normal,
                15: reds.alt_normal,
            }
        },
        # animated
        0x40825C: {
            0: {
                8: blues.normal,
                9: blues.alt_normal,
                10: greens.normal,
                11: greens.alt_normal,
                12: yellows.normal,
                13: yellows.alt_normal,
                14: reds.normal,
                15: reds.alt_normal,
            },
            1: {
                8: blues.darker,
                9: blues.alt_darker,
                10: greens.darker,
                11: greens.alt_darker,
                12: yellows.darker,
                13: yellows.alt_darker,
                14: reds.darker,
                15: reds.alt_darker,
            },
            2: {
                8: blues.darkest,
                9: blues.alt_darkest,
                10: greens.darkest,
                11: greens.alt_darkest,
                12: yellows.darkest,
                13: yellows.alt_darkest,
                14: reds.darkest,
                15: reds.alt_darkest,
            },
            5: {
                8: blues.brighter,
                9: blues.alt_brighter,
                10: greens.brighter,
                11: greens.alt_brighter,
                12: yellows.brighter,
                13: yellows.alt_brighter,
                14: reds.brighter,
                15: reds.alt_brighter,
            },
        },
    }
    door_palettes[0x40825C][3] = door_palettes[0x40825C][1]
    door_palettes[0x40825C][4] = door_palettes[0x40825C][0]

    palettes_to_change |= door_palettes

    for address, row in MF_TILESET_ALT_PAL_ROWS.items():
        palettes_to_change[address] = {
            row: {
                7: greens.alt_darkest,
                8: greens.alt_normal,
                9: greens.normal,
                10: blues.alt_brighter,
                11: blues.normal,
                12: yellows.alt_normal,
                13: yellows.normal,
                14: reds.alt_normal,
                15: reds.normal,
            }
        }

    normal_item_palettes = {
        0x40805C: {
            0: {
                7: yellows.normal,
                8: yellows.alt_normal,
                9: purples.normal,
                10: purples.alt_normal,
                11: reds.alt_normal,
                12: blues.brighter,
                13: blues.normal,
                14: blues.darker,
                15: blues.darkest,
            }
        }
    }

    palettes_to_change |= normal_item_palettes

    map_palettes = {
        0x5657A8: {
            0: {
                4: blues.alt_normal,
                5: blues.alt_darkest,
                7: yellows.normal,
                8: blues.normal,
                9: greens.brighter,
                10: reds.normal,
                11: yellows.normal,
                12: blues.normal,
                13: greens.brighter,
                14: reds.normal,
                15: yellows.normal,
            },
            1: {
                2: purples.normal,
                3: purples.normal,
                4: blues.alt_normal,
                5: blues.alt_darkest,
                7: yellows.normal,
                8: blues.normal,
                9: greens.brighter,
                10: reds.normal,
                11: yellows.normal,
                12: blues.normal,
                13: greens.brighter,
                14: reds.normal,
                15: yellows.normal,
            },
            2: {
                2: greens.alt_brighter,
                3: greens.alt_brighter,
                4: blues.alt_normal,
                5: blues.alt_darkest,
                7: yellows.normal,
                8: blues.normal,
                9: greens.brighter,
                10: reds.normal,
                11: yellows.normal,
                12: blues.normal,
                13: greens.brighter,
                14: reds.normal,
                15: yellows.normal,
            },
        }
    }

    animated_map_palettes = {
        0x57BCD4: {
            0: {
                0: purples.normal,
                1: purples.darker,
                2: purples.darkest,
                3: purples.darker,
                4: purples.normal,
            },
            1: {
                0: greens.alt_brighter,
                1: greens.alt_normal,
                2: greens.alt_darker,
                3: greens.alt_normal,
                4: greens.alt_brighter,
            },
        }
    }

    minimap_palettes = {
        0x3E415C: {
            0: {
                2: greens.normal,
                3: greens.alt_brighter,
                4: greens.alt_normal,
                5: blues.alt_darkest,
                6: reds.normal,
                7: yellows.normal,
                8: blues.normal,
                10: reds.normal,
                11: yellows.darker,
                13: purples.normal,
                14: blues.alt_normal,
            }
        }
    }

    map_keylock_palettes = {
        0x565C28: {
            0: {
                2: blues.normal,
                3: blues.darker,
                4: blues.darkest,
                5: greens.normal,
                6: greens.darker,
                7: greens.darkest,
                8: yellows.normal,
                9: yellows.darker,
                10: yellows.darkest,
                11: reds.brighter,
                12: reds.normal,
                13: reds.darker,
            }
        }
    }

    map_l_r_button_palettes = {
        0x565CA8: {
            0: {
                2: blues.brighter,
                3: blues.normal,
                4: blues.darker,
                5: greens.normal,
                6: greens.alt_brighter,
                7: greens.alt_normal,
            },
            1: {
                2: blues.brighter,
                3: blues.darker,
                4: blues.alt_normal,
                5: greens.normal,
                6: greens.alt_brighter,
                7: greens.alt_normal,
            },
            2: {
                2: blues.normal,
                3: blues.darker,
                4: blues.alt_normal,
                5: greens.normal,
                6: greens.alt_brighter,
                7: greens.alt_normal,
            },
        }
    }

    palettes_to_change |= map_palettes
    palettes_to_change |= animated_map_palettes
    palettes_to_change |= minimap_palettes
    palettes_to_change |= map_keylock_palettes
    palettes_to_change |= map_l_r_button_palettes

    x_palettes = {
        # Normal X
        0x3E40DC: {
            0: {
                11: reds.brighter,
                12: reds.darker,
                13: reds.darkest,
            },
            1: {
                11: greens.normal,
                12: greens.darker,
                13: greens.darkest,
            },
            2: {
                11: yellows.alt_normal,
                12: yellows.alt_darker,
                13: yellows.alt_darkest,
            },
        },
        # Ice-X
        0x35EE98: {
            0: {
                3: blues.normal,
                4: blues.darker,
                5: blues.alt_darker,
                6: blues.alt_normal,
                7: blues.brighter,
                11: blues.normal,
                12: blues.darker,
                13: blues.alt_darker,
                14: blues.alt_darkest,
            }
        },
    }

    palettes_to_change |= x_palettes

    text_palettes = {
        0x565B28: {
            0: {
                4: reds.normal,
                6: purples.normal,
                8: yellows.normal,
                10: greens.normal,
                12: blues.alt_normal,
                14: blues.normal,
            }
        }
    }

    palettes_to_change |= text_palettes

    for base_address, data in palettes_to_change.items():
        for row, row_data in data.items():
            palette_address = base_address + 0x20 * row
            palette = Palette(1, rom, palette_address)
            for element, color in row_data.items():
                palette.colors[element] = color

            palette.write(rom, palette_address)
