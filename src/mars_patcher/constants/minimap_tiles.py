from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from typing_extensions import Self

# String Format
# <top><left><right><bottom>_<top-left><top-right><bottom-left><bottom-right>_<content>

# Chunk 1 (tile edges)
# - see Edge and ColoredDoor for values

# Chunk 2 (tile corners)
# - C: corner pixel
# - x: none

# Chunk 3 (tile content)
# - see Content for values


class Edge(Enum):
    EMPTY = "x"
    WALL = "W"
    SHORTCUT = "S"
    DOOR = "D"

    @property
    def is_door(self) -> bool:
        return self == Edge.DOOR


class ColoredDoor(Enum):
    BLUE = "B"
    GREEN = "G"
    YELLOW = "Y"
    RED = "R"

    @property
    def is_door(self) -> bool:
        return True

    # Aliases
    L1 = BLUE
    L2 = GREEN
    L3 = YELLOW
    L4 = RED


class TileEdges(NamedTuple):
    top: Edge = Edge.WALL
    left: Edge | ColoredDoor = Edge.WALL
    right: Edge | ColoredDoor = Edge.WALL
    bottom: Edge = Edge.WALL

    @property
    def as_str(self) -> str:
        return f"{self.top.value}{self.left.value}{self.right.value}{self.bottom.value}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        if len(value) != 4:
            raise ValueError(f"'{value}' is not a valid TileEdges string")
        top, left, right, bottom = tuple(value)

        def any_edge_from_value(v: str) -> Edge | ColoredDoor:
            try:
                return Edge(v)
            except ValueError:
                pass

            try:
                return ColoredDoor(v)
            except ValueError:
                raise ValueError(f"{repr(v)} is not a valid Edge or ColoredDoor")

        return cls(
            top=Edge(top),
            left=any_edge_from_value(left),
            right=any_edge_from_value(right),
            bottom=Edge(bottom),
        )

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

    @property
    def as_str(self) -> str:
        def s(corner: bool) -> str:
            return "C" if corner else "x"

        return f"{s(self.top_left)}{s(self.top_right)}{s(self.bottom_left)}{s(self.bottom_right)}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        if len(value) != 4:
            raise ValueError(f"'{value}' is not a valid TileCorners string")
        tl, tr, bl, br = tuple(value)
        return cls(
            top_left=(tl == "C"),
            top_right=(tr == "C"),
            bottom_left=(bl == "C"),
            bottom_right=(br == "C"),
        )

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


class Content(Enum):
    EMPTY = "x"
    EMPTY_RED_WALLS = "w"
    NAVIGATION = "N"
    SAVE = "S"
    RECHARGE = "R"
    HIDDEN_RECHARGE = "H"
    DATA = "D"
    ITEM = "I"
    OBTAINED_ITEM = "O"
    BOSS_RIGHT_DOWNLOADED = "B-R-D"  # Serris skeleton
    BOSS_BOTTOM_LEFT_EXPLORED = "B-BL-E"  # Serris
    BOSS_TOP_LEFT_DOWNLOADED = "B-TL-D"  # BOX 1
    BOSS_LEFT_EXPLORED = "B-L-E"  # Mega-X
    BOSS_TOP_RIGHT_BOTH = "B-TR-B"  # Nightmare
    BOSS_TOP_RIGHT_EXPLORED = "B-TR-E"  # BOX 2
    GUNSHIP = "G"
    GUNSHIP_EDGE = "P"
    SECURITY = "K"
    AUXILLARY_POWER = "Y"
    ANIMALS = "A"
    TUNNEL = "T"
    BOILER_PAD = "L"

    @property
    def can_h_flip(self) -> bool:
        exclude = {
            Content.NAVIGATION,
            Content.SAVE,
            Content.RECHARGE,
            Content.HIDDEN_RECHARGE,
            Content.DATA,
            Content.GUNSHIP,
            Content.GUNSHIP_EDGE,
            Content.SECURITY,
            Content.AUXILLARY_POWER,
            Content.BOILER_PAD,
        }
        return self not in exclude

    @property
    def can_v_flip(self) -> bool:
        exclude = {
            Content.NAVIGATION,
            Content.SAVE,
            Content.RECHARGE,
            Content.HIDDEN_RECHARGE,
            Content.BOSS_RIGHT_DOWNLOADED,
            Content.BOSS_BOTTOM_LEFT_EXPLORED,
            Content.BOSS_TOP_LEFT_DOWNLOADED,
            Content.BOSS_LEFT_EXPLORED,
            Content.BOSS_TOP_RIGHT_BOTH,
            Content.BOSS_TOP_RIGHT_EXPLORED,
            Content.GUNSHIP,
            Content.GUNSHIP_EDGE,
            Content.SECURITY,
            Content.AUXILLARY_POWER,
            Content.TUNNEL,
            Content.BOILER_PAD,
        }
        return self not in exclude


class MapTile(NamedTuple):
    edges: TileEdges = TileEdges()
    corners: TileCorners = TileCorners()
    content: Content = Content.EMPTY
    transparent: bool = False

    @property
    def as_str(self) -> str:
        return f"{self.edges.as_str}_{self.corners.as_str}_{self.content.value}"

    @classmethod
    def from_str(cls, value: str) -> Self:
        edges, corners, content = value.split("_")
        return cls(
            edges=TileEdges.from_str(edges),
            corners=TileCorners.from_str(corners),
            content=Content(content),
            transparent=False,
        )

    def h_flip(self) -> MapTile:
        if not self.content.can_h_flip:
            raise ValueError(f"Cannot h_flip tile with contents {self.content}")

        return MapTile(
            edges=self.edges.h_flip(),
            corners=self.corners.h_flip(),
            content=self.content,
            transparent=self.transparent,
        )

    def v_flip(self) -> MapTile:
        if not self.content.can_v_flip:
            raise ValueError(f"Cannot v_flip tile with contents {self.content}")

        return MapTile(
            edges=self.edges.v_flip(),
            corners=self.corners.v_flip(),
            content=self.content,
            transparent=self.transparent,
        )
