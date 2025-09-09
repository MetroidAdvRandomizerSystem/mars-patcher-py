from mars_patcher.rom import Rom
from mars_patcher.zm.constants.reserved_space import ReservedConstantsZM


def tileset_tilemap_sizes_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.TILESET_TILEMAP_SIZES_PTR)


def chozo_statue_targets_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.CHOZO_STATUE_TARGETS_PTR)


def intro_cutscene_data_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.INTRO_CUTSCENE_DATA_PTR)


def starting_info_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.STARTING_INFO_PTR)


def major_locations_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.MAJOR_LOCATIONS_PTR)


def minor_locations_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.MINOR_LOCATIONS_PTR)


def difficulty_options_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.DIFFICULTY_OPTIONS_PTR)


def metroid_sprite_stats_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.METROID_SPRITE_STATS_PTR)


def black_pirates_require_plasma_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.BLACK_PIRATES_REQUIRE_PLASMA_PTR)


def skip_door_transitions_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.SKIP_DOOR_TRANSITIONS_PTR)


def ball_launcher_without_bombs_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.BALL_LAUNCHER_WITHOUT_BOMBS_PTR)


def disable_midair_bomb_jump_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.DISABLE_MIDAIR_BOMB_JUMP_PTR)


def disable_walljump_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.DISABLE_WALLJUMP_PTR)


def remove_cutscenes_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.REMOVE_CUTSCENES_PTR)


def skip_suitless_sequence_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.SKIP_SUITLESS_SEQUENCE_PTR)


def energy_tank_increase_amount_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.ENERGY_TANK_INCREASE_AMOUNT_PTR)


def missile_tank_increase_amount_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.MISSILE_TANK_INCREASE_AMOUNT_PTR)


def super_missile_tank_increase_amount_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.SUPER_MISSILE_TANK_INCREASE_AMOUNT_PTR)


def power_bomb_tank_increase_amount_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.POWER_BOMB_TANK_INCREASE_AMOUNT_PTR)


def title_text_lines_addr(rom: Rom) -> int:
    return rom.read_ptr(ReservedConstantsZM.TITLE_TEXT_LINES_PTR)
