from enum import IntEnum, auto

from mars_patcher.zm.data import get_data_path


class MajorSource(IntEnum):
    LONG_BEAM = 0
    CHARGE_BEAM = auto()
    ICE_BEAM = auto()
    WAVE_BEAM = auto()
    PLASMA_BEAM = auto()
    BOMBS = auto()
    VARIA_SUIT = auto()
    GRAVITY_SUIT = auto()
    MORPH_BALL = auto()
    SPEED_BOOSTER = auto()
    HI_JUMP = auto()
    SCREW_ATTACK = auto()
    SPACE_JUMP = auto()
    POWER_GRIP = auto()
    FULLY_POWERED = auto()
    ZIPLINES = auto()


class ItemType(IntEnum):
    UNDEFINED = -1
    NONE = 0
    ENERGY_TANK = auto()
    MISSILE_TANK = auto()
    SUPER_MISSILE_TANK = auto()
    POWER_BOMB_TANK = auto()
    LONG_BEAM = auto()
    CHARGE_BEAM = auto()
    ICE_BEAM = auto()
    WAVE_BEAM = auto()
    PLASMA_BEAM = auto()
    BOMBS = auto()
    VARIA_SUIT = auto()
    GRAVITY_SUIT = auto()
    MORPH_BALL = auto()
    SPEED_BOOSTER = auto()
    HI_JUMP = auto()
    SCREW_ATTACK = auto()
    SPACE_JUMP = auto()
    POWER_GRIP = auto()
    FULLY_POWERED = auto()
    ZIPLINES = auto()
    ICE_TRAP = auto()


class ItemSprite(IntEnum):
    DEFAULT = auto()
    EMPTY = auto()
    ENERGY_TANK = auto()
    MISSILE_TANK = auto()
    SUPER_MISSILE_TANK = auto()
    POWER_BOMB_TANK = auto()
    LONG_BEAM = auto()
    CHARGE_BEAM = auto()
    ICE_BEAM = auto()
    WAVE_BEAM = auto()
    PLASMA_BEAM = auto()
    BOMBS = auto()
    VARIA_SUIT = auto()
    GRAVITY_SUIT = auto()
    MORPH_BALL = auto()
    SPEED_BOOSTER = auto()
    HI_JUMP = auto()
    SCREW_ATTACK = auto()
    SPACE_JUMP = auto()
    POWER_GRIP = auto()
    FULLY_POWERED = auto()
    ZIPLINES = auto()
    ANONYMOUS = auto()
    SHINY_MISSILE_TANK = auto()
    SHINY_POWER_BOMB_TANK = auto()


ITEM_TO_SPRITE = {
    ItemType.NONE: ItemSprite.EMPTY,
    ItemType.ENERGY_TANK: ItemSprite.ENERGY_TANK,
    ItemType.MISSILE_TANK: ItemSprite.MISSILE_TANK,
    ItemType.SUPER_MISSILE_TANK: ItemSprite.SUPER_MISSILE_TANK,
    ItemType.POWER_BOMB_TANK: ItemSprite.POWER_BOMB_TANK,
    ItemType.LONG_BEAM: ItemSprite.LONG_BEAM,
    ItemType.CHARGE_BEAM: ItemSprite.CHARGE_BEAM,
    ItemType.ICE_BEAM: ItemSprite.ICE_BEAM,
    ItemType.WAVE_BEAM: ItemSprite.WAVE_BEAM,
    ItemType.PLASMA_BEAM: ItemSprite.PLASMA_BEAM,
    ItemType.BOMBS: ItemSprite.BOMBS,
    ItemType.VARIA_SUIT: ItemSprite.VARIA_SUIT,
    ItemType.GRAVITY_SUIT: ItemSprite.GRAVITY_SUIT,
    ItemType.MORPH_BALL: ItemSprite.MORPH_BALL,
    ItemType.SPEED_BOOSTER: ItemSprite.SPEED_BOOSTER,
    ItemType.HI_JUMP: ItemSprite.HI_JUMP,
    ItemType.SCREW_ATTACK: ItemSprite.SCREW_ATTACK,
    ItemType.SPACE_JUMP: ItemSprite.SPACE_JUMP,
    ItemType.POWER_GRIP: ItemSprite.POWER_GRIP,
    ItemType.FULLY_POWERED: ItemSprite.FULLY_POWERED,
    ItemType.ZIPLINES: ItemSprite.ZIPLINES,
}


PALETTE_NAMES = {
    ItemSprite.EMPTY: "tank",
    ItemSprite.ENERGY_TANK: "tank",
    ItemSprite.MISSILE_TANK: "tank",
    ItemSprite.SUPER_MISSILE_TANK: "tank",
    ItemSprite.POWER_BOMB_TANK: "tank",
    ItemSprite.LONG_BEAM: "long_beam",
    ItemSprite.CHARGE_BEAM: "charge_beam",
    ItemSprite.ICE_BEAM: "ice_beam",
    ItemSprite.WAVE_BEAM: "wave_beam",
    ItemSprite.PLASMA_BEAM: "plasma_beam",
    ItemSprite.BOMBS: "bombs",
    ItemSprite.VARIA_SUIT: "varia_suit",
    ItemSprite.GRAVITY_SUIT: "gravity_suit",
    ItemSprite.MORPH_BALL: "morph_ball",
    ItemSprite.SPEED_BOOSTER: "speed_booster",
    ItemSprite.HI_JUMP: "hi_jump",
    ItemSprite.SCREW_ATTACK: "screw_attack",
    ItemSprite.SPACE_JUMP: "space_jump",
    ItemSprite.POWER_GRIP: "power_grip",
    ItemSprite.FULLY_POWERED: "morph_ball",  # TODO: Add palette for this
    ItemSprite.ZIPLINES: "ziplines",
    ItemSprite.ANONYMOUS: "tank",
    # TODO: Add palettes for these
    # ItemSprite.SHINY_MISSILE_TANK: "shiny_tank",
    # ItemSprite.SHINY_POWER_BOMB_TANK: "shiny_tank",
}


def get_sprite_palette(sprite: ItemSprite) -> bytes:
    name = PALETTE_NAMES[sprite] + ".pal"
    path = get_data_path("item_palettes", name)
    with open(path, "rb") as f:
        return f.read()


class ItemJingle(IntEnum):
    DEFAULT = 0
    MINOR = auto()
    MAJOR = auto()
    UNKNOWN = auto()
    FULLY_POWERED = auto()


class HintLocation(IntEnum):
    NONE = -1
    LONG_BEAM = 0
    BOMBS = auto()
    ICE_BEAM = auto()
    SPEED_BOOSTER = auto()
    HI_JUMP = auto()
    VARIA_SUIT = auto()
    WAVE_BEAM = auto()
    SCREW_ATTACK = auto()


BEAM_BOMB_FLAGS = {
    "LONG_BEAM": 1 << 0,
    "ICE_BEAM": 1 << 1,
    "WAVE_BEAM": 1 << 2,
    "PLASMA_BEAM": 1 << 3,
    "CHARGE_BEAM": 1 << 4,
    "BOMBS": 1 << 7,
}

SUIT_MISC_FLAGS = {
    "HI_JUMP": 1 << 0,
    "SPEED_BOOSTER": 1 << 1,
    "SPACE_JUMP": 1 << 2,
    "SCREW_ATTACK": 1 << 3,
    "VARIA_SUIT": 1 << 4,
    "GRAVITY_SUIT": 1 << 5,
    "MORPH_BALL": 1 << 6,
    "POWER_GRIP": 1 << 7,
}
