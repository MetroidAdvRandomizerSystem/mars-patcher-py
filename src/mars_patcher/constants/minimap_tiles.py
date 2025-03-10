from __future__ import annotations

from enum import Enum
from typing import NamedTuple

# ruff: noqa: E741


class Edge(Enum):
    EMPTY = "x"
    WALL = "W"
    SHORTCUT = "S"
    DOOR = "D"

    # aliases
    X = EMPTY
    W = WALL
    S = SHORTCUT
    D = DOOR


class ColorDoor(Enum):
    BLUE = "B"
    GREEN = "G"
    YELLOW = "Y"
    RED = "R"

    # aliases
    B = BLUE
    G = GREEN
    Y = YELLOW
    R = RED


# aliases for ease of definition
X = Edge.X
W = Edge.W
S = Edge.S
D = Edge.D
BLUE = ColorDoor.B
GREEN = ColorDoor.G
YELLOW = ColorDoor.Y
RED = ColorDoor.R


class Content(Enum):
    EMPTY = "x"
    NAVIGATION = "N"
    SAVE = "S"
    RECHARGE = "R"
    HIDDEN_RECHARGE = "H"
    DATA = "D"
    ITEM = "I"
    OBTAINED_ITEM = "O"
    BOSS = "B"
    GUNSHIP = "G"
    GUNSHIP_EDGE = "P"

    # aliases
    X = EMPTY
    N = NAVIGATION
    S = SAVE
    R = RECHARGE
    H = HIDDEN_RECHARGE
    D = DATA
    I = ITEM
    O = OBTAINED_ITEM
    B = BOSS
    G = GUNSHIP
    P = GUNSHIP_EDGE


class TileEdges(NamedTuple):
    top: Edge = Edge.WALL
    left: Edge | ColorDoor = Edge.WALL
    right: Edge | ColorDoor = Edge.WALL
    bottom: Edge = Edge.WALL

    def __str__(self):
        return f"{self.top.value}{self.left.value}{self.right.value}{self.bottom.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def h_flip(self) -> TileEdges:
        return TileEdges(
            top=self.top,
            left=self.right,
            right=self.left,
            bottom=self.bottom,
        )

    def v_flip(self) -> TileEdges:
        return TileEdges(
            top=self.bottom,
            left=self.left,
            right=self.right,
            bottom=self.top,
        )


class TileCorners(NamedTuple):
    top_left: bool = False
    top_right: bool = False
    bottom_left: bool = False
    bottom_right: bool = False

    def __str__(self):
        def s(corner: bool) -> str:
            return "C" if corner else "x"

        return f"{s(self.top_left)}{s(self.top_right)}{s(self.bottom_left)}{s(self.bottom_right)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def h_flip(self) -> TileCorners:
        return TileCorners(
            top_left=self.top_right,
            top_right=self.top_left,
            bottom_left=self.bottom_right,
            bottom_right=self.bottom_left,
        )

    def v_flip(self) -> TileCorners:
        return TileCorners(
            top_left=self.bottom_left,
            top_right=self.bottom_right,
            bottom_left=self.top_left,
            bottom_right=self.top_right,
        )


class MapTile(NamedTuple):
    edges: TileEdges = TileEdges()
    corners: TileCorners = TileCorners()
    content: Content = Content.EMPTY

    def __str__(self) -> str:
        return f"{self.edges}_{self.corners}_{self.content.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def h_flip(self) -> MapTile:
        return MapTile(
            edges=self.edges.h_flip(),
            corners=self.corners.h_flip(),
            content=self.content,
        )

    def v_flip(self) -> MapTile:
        return MapTile(
            edges=self.edges.v_flip(),
            corners=self.corners.v_flip(),
            content=self.content,
        )


def _tile(
    top: Edge,
    left: Edge | ColorDoor,
    right: Edge | ColorDoor,
    bottom: Edge,
    top_left: bool = False,
    top_right: bool = False,
    bottom_left: bool = False,
    bottom_right: bool = False,
    content: Content = Content.EMPTY,
) -> MapTile:
    return MapTile(
        edges=TileEdges(top, left, right, bottom),
        corners=TileCorners(top_left, top_right, bottom_left, bottom_right),
        content=content,
    )


ROW_SIZE = 0x20
COLOR_PAIRS = [
    (BLUE, GREEN),
    (BLUE, RED),
    (BLUE, YELLOW),
    (GREEN, RED),
    (GREEN, YELLOW),
    (RED, YELLOW),
]
COLOR_BATCHES = [(BLUE, 0x005), (GREEN, 0x00A), (RED, 0x00F), (YELLOW, 0x014)]

COLORED_DOOR_TILES: dict[int, MapTile] = {}


def basic_color_tiles(start: int, color: ColorDoor):
    row = ROW_SIZE
    tiles = {
        row * 0 + 0: _tile(W, color, X, X),
        row * 0 + 1: _tile(D, color, X, X),
        row * 0 + 2: _tile(D, color, X, X, bottom_right=True),
        row * 0 + 3: _tile(D, color, color, D),
        row * 0 + 4: _tile(D, color, color, X),
        row * 1 + 0: _tile(X, color, X, X),
        row * 1 + 1: _tile(X, color, X, X, top_right=True, bottom_right=True),
        row * 1 + 2: _tile(D, color, W, D),
        row * 1 + 3: _tile(D, color, D, X),
        row * 1 + 4: _tile(D, color, color, W),
        row * 2 + 0: _tile(W, color, X, W),
        row * 2 + 1: _tile(D, color, X, D),
        row * 2 + 2: _tile(D, color, X, W),
        row * 2 + 3: _tile(W, color, W, W),
        row * 2 + 4: _tile(W, color, color, W),
        row * 3 + 0: _tile(D, color, W, X),
        row * 3 + 1: _tile(W, color, D, X),
        # row * 3 + 2: tile(),
        row * 3 + 3: _tile(W, color, W, X),
        row * 3 + 4: _tile(W, color, color, X),
        row * 4 + 0: _tile(D, color, W, W),
        row * 4 + 1: _tile(X, color, D, X),
        # row * 4 + 2: tile()
        row * 4 + 3: _tile(X, color, W, X),
        row * 4 + 4: _tile(X, color, color, X),
    }
    return {start + offset: tile for offset, tile in tiles.items()}


# the 5x5 blocks on the top
for color, offset in COLOR_BATCHES:
    COLORED_DOOR_TILES.update(basic_color_tiles(offset, color))

# the 6x5 block near the top right
for row, (top, bottom) in enumerate([(D, X), (D, W), (W, W), (W, X), (X, X)]):
    for col, (left, right) in enumerate(COLOR_PAIRS):
        COLORED_DOOR_TILES[0x019 + row * ROW_SIZE + col] = _tile(top, left, right, bottom)

# the 1x5 block at the very top right
for i, (left, right) in enumerate(COLOR_PAIRS[:-1]):
    COLORED_DOOR_TILES[0x01F + i * ROW_SIZE] = _tile(D, left, right, D)
# this one didn't fit in the nice grid pattern so it's in a weird spot
for left, right in COLOR_PAIRS[-1:]:
    COLORED_DOOR_TILES[0x096] = _tile(D, left, right, D)

# the few colored tiles on row 7
for color, offset in COLOR_BATCHES:
    start = ROW_SIZE * 7 + offset
    if color != BLUE:
        COLORED_DOOR_TILES[start] = _tile(D, color, X, X, bottom_right=True)
    COLORED_DOOR_TILES[start + 1] = _tile(W, D, color, W)
    COLORED_DOOR_TILES[start + 2] = _tile(D, D, color, W)
    COLORED_DOOR_TILES[start + 3] = _tile(D, D, color, D)
COLORED_DOOR_TILES[0x0F8] = _tile(W, YELLOW, X, X, bottom_right=True)
COLORED_DOOR_TILES[0x06C] = _tile(W, GREEN, X, X, bottom_right=True)


def special_room_tiles(offset: int, color: ColorDoor, content: Content):
    return {
        offset + 0: _tile(W, color, W, W, content=content),  # left door
        offset + 1: _tile(W, W, color, W, content=content),  # right door
        offset + 2: _tile(W, color, color, W, content=content),  # both doors
    }


# special rooms
for i, (color, _) in enumerate(COLOR_BATCHES):
    COLORED_DOOR_TILES.update(special_room_tiles(0x140 + i * 3, color, Content.RECHARGE))
    COLORED_DOOR_TILES.update(special_room_tiles(0x14C + i * 3, color, Content.NAVIGATION))
    COLORED_DOOR_TILES.update(special_room_tiles(0x160 + i * 3, color, Content.DATA))

# random exceptions that don't fit into any other category
COLORED_DOOR_TILES.update(
    {
        0x128: _tile(W, RED, D, W, content=Content.RECHARGE),
        0x15E: _tile(W, D, YELLOW, W, content=Content.RECHARGE),
        0x17E: _tile(W, RED, RED, W, content=Content.SAVE),
        0x17F: _tile(W, YELLOW, D, W, content=Content.SAVE),
        0x198: _tile(W, BLUE, W, W, content=Content.ITEM),
        0x199: _tile(W, BLUE, W, W, content=Content.OBTAINED_ITEM),
        0x19E: _tile(W, GREEN, W, W, content=Content.ITEM),
        0x19F: _tile(W, GREEN, W, W, content=Content.OBTAINED_ITEM),
        0x1AC: _tile(W, YELLOW, YELLOW, W, content=Content.ITEM),
        0x1AD: _tile(W, YELLOW, YELLOW, W, content=Content.OBTAINED_ITEM),
    }
)

COLORED_DOOR_TILE_IDS = {tile: idx for idx, tile in COLORED_DOOR_TILES.items()}


NORMAL_DOOR_TILE_IDS = {
    _tile(W, W, X, X): 0x000,
    _tile(W, X, X, X): 0x001,
    _tile(D, W, X, X): 0x002,
    _tile(D, X, X, X): 0x003,
    _tile(D, W, X, X, bottom_right=True): 0x004,
    _tile(X, W, X, X): 0x020,
    _tile(X, D, X, X): 0x021,
    _tile(W, X, X, X, bottom_left=True, bottom_right=True): 0x022,
    _tile(X, W, X, X, top_right=True, bottom_right=True): 0x023,
    _tile(D, W, W, D): 0x024,
    _tile(W, W, X, W): 0x040,
    _tile(W, X, X, W): 0x041,
    _tile(D, W, X, D): 0x042,
    _tile(D, W, X, W): 0x043,
    _tile(D, X, X, D): 0x044,
    _tile(D, W, W, X): 0x060,
    _tile(W, D, W, X): 0x061,
    _tile(W, D, D, X): 0x062,
    _tile(W, W, W, X): 0x063,
    _tile(D, X, X, W): 0x064,
    _tile(D, W, W, W): 0x080,
    _tile(X, D, W, X): 0x081,
    _tile(X, D, D, X): 0x082,
    _tile(X, W, W, X): 0x083,
    _tile(W, D, D, W): 0x084,
    _tile(W, W, W, W): 0x087,
    _tile(W, S, D, W, content=Content.ITEM): 0x0B4,
    _tile(W, S, D, W): 0x0B6,
    _tile(D, D, X, W): 0x0E0,
    _tile(D, D, X, D): 0x0E1,
    _tile(D, D, W, X): 0x0E2,
    _tile(D, D, D, X): 0x0E3,
    _tile(W, W, X, X, bottom_right=True): 0x0E4,
    _tile(X, W, X, X, bottom_right=True): 0x0E5,
    _tile(D, X, X, X, bottom_left=True, bottom_right=True): 0x100,
    _tile(X, D, X, X, top_right=True, bottom_right=True): 0x101,
    _tile(D, D, X, X, bottom_right=True): 0x102,
    # tile(D, W, X, X, br=True): 0x103,  # dupe of 0x004
    _tile(W, D, X, X, bottom_right=True): 0x104,
    _tile(X, D, X, X, top_right=True): 0x105,
    _tile(X, X, D, W, content=Content.BOSS): 0x108,
    _tile(W, D, X, W, content=Content.BOSS): 0x109,
    _tile(X, X, D, X, content=Content.BOSS): 0x10D,
    _tile(X, D, X, W, content=Content.BOSS): 0x10F,
    _tile(D, D, W, W): 0x120,
    _tile(D, D, D, W): 0x121,
    _tile(D, D, W, D): 0x122,
    _tile(D, D, D, D): 0x123,
    _tile(W, D, W, W): 0x124,
    _tile(W, D, X, X): 0x125,
    _tile(X, X, X, X): 0x126,
    _tile(W, X, X, X, bottom_right=True): 0x127,
    _tile(W, D, X, W, content=Content.GUNSHIP_EDGE): 0x129,
    _tile(W, X, W, W, content=Content.GUNSHIP): 0x12A,
    _tile(W, D, X, W): 0x12B,
    _tile(D, D, X, X): 0x12C,
    _tile(W, D, W, W, content=Content.HIDDEN_RECHARGE): 0x138,
    _tile(W, W, D, W, content=Content.HIDDEN_RECHARGE): 0x139,
    _tile(W, D, D, W, content=Content.HIDDEN_RECHARGE): 0x13A,
    _tile(W, D, W, W, content=Content.RECHARGE): 0x158,
    _tile(W, W, D, W, content=Content.RECHARGE): 0x159,
    _tile(W, D, D, W, content=Content.RECHARGE): 0x15A,
    _tile(W, D, W, W, content=Content.DATA): 0x15B,
    _tile(W, W, D, W, content=Content.DATA): 0x15C,
    _tile(W, D, D, W, content=Content.DATA): 0x15D,
    _tile(W, D, W, W, content=Content.NAVIGATION): 0x178,
    _tile(W, W, D, W, content=Content.NAVIGATION): 0x179,
    _tile(W, D, D, W, content=Content.NAVIGATION): 0x17A,
    _tile(W, D, W, W, content=Content.SAVE): 0x17B,
    _tile(W, W, D, W, content=Content.SAVE): 0x17C,
    _tile(W, D, D, W, content=Content.SAVE): 0x17D,
    _tile(W, D, W, W, content=Content.ITEM): 0x180,
    _tile(W, D, W, W, content=Content.OBTAINED_ITEM): 0x181,
    _tile(W, W, X, W, content=Content.ITEM): 0x182,
    _tile(W, W, X, W, content=Content.OBTAINED_ITEM): 0x183,
    _tile(W, D, D, W, content=Content.ITEM): 0x184,
    _tile(W, D, D, W, content=Content.OBTAINED_ITEM): 0x185,
    _tile(W, W, X, X, content=Content.ITEM): 0x186,
    _tile(W, W, X, X, content=Content.OBTAINED_ITEM): 0x187,
    _tile(W, D, X, W, content=Content.ITEM): 0x188,
    _tile(W, D, X, W, content=Content.OBTAINED_ITEM): 0x189,
    _tile(X, W, X, X, content=Content.ITEM): 0x18A,
    _tile(X, W, X, X, content=Content.OBTAINED_ITEM): 0x18B,
    _tile(X, D, X, X, content=Content.ITEM): 0x18C,
    _tile(X, D, X, X, content=Content.OBTAINED_ITEM): 0x18D,
    _tile(W, D, X, X, content=Content.ITEM): 0x18E,
    _tile(W, D, X, X, content=Content.OBTAINED_ITEM): 0x18F,
    _tile(W, X, X, X, content=Content.ITEM): 0x190,
    _tile(W, X, X, X, content=Content.OBTAINED_ITEM): 0x191,
    _tile(W, X, X, W, content=Content.ITEM): 0x192,
    _tile(W, X, X, W, content=Content.OBTAINED_ITEM): 0x193,
    _tile(W, W, W, X, content=Content.ITEM): 0x194,
    _tile(W, W, W, X, content=Content.OBTAINED_ITEM): 0x195,
    _tile(D, D, D, W, content=Content.ITEM): 0x196,
    _tile(D, D, D, W, content=Content.OBTAINED_ITEM): 0x197,
    _tile(X, D, D, W, content=Content.ITEM): 0x19A,
    _tile(X, D, D, W, content=Content.OBTAINED_ITEM): 0x19B,
    _tile(W, W, D, X, content=Content.ITEM): 0x19C,
    _tile(W, W, D, X, content=Content.OBTAINED_ITEM): 0x19D,
    _tile(X, W, W, D, content=Content.ITEM): 0x1A0,
    _tile(X, W, W, D, content=Content.OBTAINED_ITEM): 0x1A1,
    _tile(W, W, W, D, content=Content.ITEM): 0x1A2,
    _tile(W, W, W, D, content=Content.OBTAINED_ITEM): 0x1A3,
    _tile(X, X, X, X, content=Content.ITEM): 0x1A4,
    _tile(X, X, X, X, content=Content.OBTAINED_ITEM): 0x1A5,
    _tile(W, W, X, D, content=Content.ITEM): 0x1A6,
    _tile(W, W, X, D, content=Content.OBTAINED_ITEM): 0x1A7,
    _tile(X, W, W, X, content=Content.ITEM): 0x1A8,
    _tile(X, W, W, X, content=Content.OBTAINED_ITEM): 0x1A9,
    _tile(D, D, W, W, content=Content.ITEM): 0x1AA,
    _tile(D, D, W, W, content=Content.OBTAINED_ITEM): 0x1AB,
}

ALL_DOOR_TILE_IDS = COLORED_DOOR_TILE_IDS | NORMAL_DOOR_TILE_IDS
ALL_DOOR_TILES = {idx: tile for tile, idx in ALL_DOOR_TILE_IDS.items()}
