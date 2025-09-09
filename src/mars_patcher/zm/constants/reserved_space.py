class ReservedConstantsZM:
    """
    These are constants that are in the ROM's 'Reserved Space'; things that are intended to be
    modified by this patcher. Most of these are pointers at a hard-coded address that point to
    various pieces of data.
    """

    # Important addresses:
    # 0x760D38 - End of data (U region)
    # 0x7C0000 - Patcher data free space
    # 0x7D0000 - Randomizer data pointers
    # 0x7D8000 - NES Metroid data

    # These need to be kept in sync with the data pointers in the decomp, which can be found in
    # src/data/randomizer_pointers.c
    RANDO_POINTERS_ADDR = 0x7D0000

    # Existing data
    ROOM_AREA_ENTRIES_PTR = RANDO_POINTERS_ADDR + 0x00
    """Pointer to the list of pointers to the room entries for each area."""
    TILESET_ENTRIES_PTR = RANDO_POINTERS_ADDR + 0x04
    """Pointer to the list of tileset entries."""
    TILESET_TILEMAP_SIZES_PTR = RANDO_POINTERS_ADDR + 0x08
    """Pointer to an array containing the size of each tileset's tilemap."""
    MINIMAPS_PTR = RANDO_POINTERS_ADDR + 0x0C
    """Pointer to a list of pointers to the minimap data for each area."""
    AREA_DOORS_PTR = RANDO_POINTERS_ADDR + 0x10
    """Pointer to the list of pointers to the door entries for each area."""
    AREA_CONNECTIONS_PTR = RANDO_POINTERS_ADDR + 0x14
    """Pointer to the list of area connections."""
    ANIM_PALETTE_ENTRIES_PTR = RANDO_POINTERS_ADDR + 0x18
    """Pointer to the list of animated palette entries."""
    SPRITE_GRAPHICS_PTR = RANDO_POINTERS_ADDR + 0x1C
    """Pointer to the list of pointers to the graphics for each sprite."""
    SPRITE_PALETTES_PTR = RANDO_POINTERS_ADDR + 0x20
    """Pointer to the list of pointers to the palette for each sprite."""
    SPRITESET_PTR = RANDO_POINTERS_ADDR + 0x24
    """Pointer to the list of pointers to spriteset entries."""
    SAMUS_PALETTES_PTR = RANDO_POINTERS_ADDR + 0x28
    """Pointer to the start of all of Samus's palettes."""
    HELMET_CURSOR_PALETTES_PTR = RANDO_POINTERS_ADDR + 0x2C
    """Pointer to the palette used for the helmet cursor in menus."""
    BEAM_PALETTES_PTR = RANDO_POINTERS_ADDR + 0x30
    """Pointer to the start of the beam palettes."""
    CHARACTER_WIDTHS_PTR = RANDO_POINTERS_ADDR + 0x34
    """Pointer to the character widths table."""
    SOUND_DATA_PTR = RANDO_POINTERS_ADDR + 0x38
    """Pointer to the list of sound data entries."""
    CHOZO_STATUE_TARGETS_PTR = RANDO_POINTERS_ADDR + 0x3C
    """Pointer to the list of Chozo statue targets."""

    # Rando data
    INTRO_CUTSCENE_DATA_PTR = RANDO_POINTERS_ADDR + 0x40
    """Pointer to the in-game cutscene data for the intro cutscene;
    needed for writing the starting area."""
    STARTING_INFO_PTR = RANDO_POINTERS_ADDR + 0x44
    """Pointer to a struct containing the starting location and items."""
    MAJOR_LOCATIONS_PTR = RANDO_POINTERS_ADDR + 0x48
    """Pointer to a list of major locations and the items they have."""
    MINOR_LOCATIONS_PTR = RANDO_POINTERS_ADDR + 0x4C
    """Pointer to a list of minor locations and the items they have."""

    # Rando options
    DIFFICULTY_OPTIONS_PTR = RANDO_POINTERS_ADDR + 0x50
    METROID_SPRITE_STATS_PTR = RANDO_POINTERS_ADDR + 0x54
    BLACK_PIRATES_REQUIRE_PLASMA_PTR = RANDO_POINTERS_ADDR + 0x58
    SKIP_DOOR_TRANSITIONS_PTR = RANDO_POINTERS_ADDR + 0x5C
    BALL_LAUNCHER_WITHOUT_BOMBS_PTR = RANDO_POINTERS_ADDR + 0x60
    DISABLE_MIDAIR_BOMB_JUMP_PTR = RANDO_POINTERS_ADDR + 0x64
    DISABLE_WALLJUMP_PTR = RANDO_POINTERS_ADDR + 0x68
    REMOVE_CUTSCENES_PTR = RANDO_POINTERS_ADDR + 0x6C
    SKIP_SUITLESS_SEQUENCE_PTR = RANDO_POINTERS_ADDR + 0x70

    ENERGY_TANK_INCREASE_AMOUNT_PTR = RANDO_POINTERS_ADDR + 0x74
    MISSILE_TANK_INCREASE_AMOUNT_PTR = RANDO_POINTERS_ADDR + 0x78
    SUPER_MISSILE_TANK_INCREASE_AMOUNT_PTR = RANDO_POINTERS_ADDR + 0x7C
    POWER_BOMB_TANK_INCREASE_AMOUNT_PTR = RANDO_POINTERS_ADDR + 0x80

    TITLE_TEXT_LINES_PTR = RANDO_POINTERS_ADDR + 0x84

    # Address for any additional data that the patcher may need to write
    PATCHER_FREE_SPACE_ADDR = 0x7C0000
    PATCHER_FREE_SPACE_END = RANDO_POINTERS_ADDR - PATCHER_FREE_SPACE_ADDR
