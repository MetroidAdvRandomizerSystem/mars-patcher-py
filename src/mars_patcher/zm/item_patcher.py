from mars_patcher.color_spaces import RgbBitSize, RgbColor
from mars_patcher.constants.game_data import (
    anim_graphics_count,
    anim_tileset_count,
    anim_tileset_entries,
    tileset_count,
    tileset_entries,
)
from mars_patcher.convert_array import ptr_to_u8, u8_to_u16
from mars_patcher.item_messages import ItemMessages, ItemMessagesKind
from mars_patcher.palette import Palette
from mars_patcher.rom import Rom
from mars_patcher.room_entry import RoomEntry
from mars_patcher.text import Language, MessageType, encode_text
from mars_patcher.tilemap import Tilemap
from mars_patcher.tileset import ANIM_TILESET_SIZE, TILESET_SIZE, Tileset
from mars_patcher.zm.auto_generated_types import MarsschemazmTankIncrements
from mars_patcher.zm.constants.game_data import (
    chozo_statue_targets_addr,
    major_locations_addr,
    minor_locations_addr,
    tank_increase_amounts_addr,
)
from mars_patcher.zm.constants.items import ITEM_TO_SPRITE, ItemSprite, get_sprite_palette
from mars_patcher.zm.constants.reserved_space import ReservedPointersZM
from mars_patcher.zm.locations import HintLocation, LocationSettings


class TilesetData:
    """Class for creating copies of tilesets with added item graphics."""

    def __init__(self, rom: Rom, id: int):
        self.rom = rom
        self.id = id
        self.meta = Tileset(rom, id)
        # Load tilemap
        self.tilemap = Tilemap(rom, self.meta.tilemap_ptr(), False)
        # Load palette
        self.palette = Palette(14, rom, self.meta.palette_addr())
        # Load animated tileset
        ats_addr = self.meta.anim_tileset_addr()
        self.anim_tileset = rom.read_bytes(ats_addr, 0x30)

    def add_item_graphics(self, sprite: ItemSprite) -> int:
        """Adds item graphics to the tileset and returns the block number. This function
        should be called for anything that isn't one of the 4 original tank types."""
        assert sprite not in {
            ItemSprite.ENERGY_TANK,
            ItemSprite.MISSILE_TANK,
            ItemSprite.SUPER_MISSILE_TANK,
            ItemSprite.POWER_BOMB_TANK,
        }, "This function should not be called for tanks"

        # Find blank row in palette (a row is considered blank if all colors
        # except the first one are the same)
        pal_colors = self.palette.colors
        pal_row = -1
        for row in range(1, 14):
            index = row * 16
            color = pal_colors[index + 1]
            if all(pal_colors[index + i] == color for i in range(2, 16)):
                # Get sprite palette and convert to RgbColor
                item_pal = get_sprite_palette(sprite)
                colors = [RgbColor.from_rgb(rgb, RgbBitSize.Rgb5) for rgb in u8_to_u16(item_pal)]
                assert len(colors) == 16, "Item palette should have 16 colors"
                pal_colors[index : index + 16] = colors
                pal_row = row + 2
                break
        if pal_row == -1:
            raise ValueError(f"No blank palette row found ({self.id:X})")

        # Find blank entry in animated tileset
        anim_gfx_idx = -1
        for i in range(16):
            if self.anim_tileset[i * 3] == 0:
                offset = sprite.value - ItemSprite.EMPTY.value
                anim_gfx_num = anim_graphics_count(self.rom) + offset
                self.anim_tileset[i * 3] = anim_gfx_num
                anim_gfx_idx = i
                break
        if anim_gfx_idx == -1:
            raise ValueError("No blank entry found in animated tileset")

        # Find blank tiles in tilemap
        tile_val = -1
        block_num = -1
        for i in range(0x4C, 0x50):
            offset = i * 4
            if all(self.tilemap.data[offset + t] == 0x40 for t in range(4)):
                tile_val = (pal_row << 12) | (anim_gfx_idx * 4)
                for t in range(4):
                    self.tilemap.data[offset + t] = tile_val + t
                block_num = i
                break
        if tile_val == -1 or block_num == -1:
            raise ValueError("No blank tiles found in tilemap")

        return block_num

    def write_copy(self, anim_tileset_id: int) -> bytes:
        """Writes the palette and tilemap to a new location, and returns the
        data for a new tileset entry."""
        data = bytearray()
        # Copy block BG graphics pointer
        data += self.rom.read_bytes(self.meta.block_bg_gfx_ptr(), 4)
        # Write palette
        pal_addr = self.rom.write_data_with_pointers(self.palette.byte_data(), [])
        data += ptr_to_u8(pal_addr)
        # Copy tiled BG graphics pointer
        data += self.rom.read_bytes(self.meta.tiled_bg_gfx_ptr(), 4)
        # Write tilemap
        tm_addr = self.rom.write_data_with_pointers(self.tilemap.byte_data(), [])
        data += ptr_to_u8(tm_addr)
        # Write animated tileset number
        data.append(anim_tileset_id)
        # Copy animated palette number
        data.append(self.meta.anim_palette())
        # Padding
        data.append(0)
        data.append(0)
        return data


class ItemPatcher:
    """Class for writing item assignments to a ROM."""

    def __init__(self, rom: Rom, settings: LocationSettings):
        self.rom = rom
        self.settings = settings

    def write_items(self) -> None:
        rom = self.rom
        hint_targets_addr = chozo_statue_targets_addr(rom)
        seen_messages: dict[str, int] = {}

        # Handle minor locations
        # Locations need to be written in order so that binary search works
        minor_locs = sorted(self.settings.minor_locs, key=lambda x: x.key)
        minor_loc_addr = minor_locations_addr(rom)
        new_tilesets: list[TilesetData] = []
        room_tilesets: dict[tuple[int, int], TilesetData] = {}
        orig_tileset_count = tileset_count(rom)

        for min_loc in minor_locs:
            # Get BG1 block value
            sprite = min_loc.item_sprite
            if sprite == ItemSprite.DEFAULT:
                sprite = ITEM_TO_SPRITE[min_loc.new_item]
            match sprite:
                case ItemSprite.ENERGY_TANK:
                    bg1_val = 0x49
                case ItemSprite.MISSILE_TANK:
                    bg1_val = 0x48
                case ItemSprite.SUPER_MISSILE_TANK:
                    bg1_val = 0x4B
                case ItemSprite.POWER_BOMB_TANK:
                    bg1_val = 0x4A
                case _:
                    # Update tileset
                    key = (min_loc.area, min_loc.room)
                    tileset = room_tilesets.get(key)
                    if tileset is None:
                        room = RoomEntry(rom, min_loc.area, min_loc.room)
                        tileset = TilesetData(rom, room.tileset())
                        ts_num = orig_tileset_count + len(new_tilesets)
                        rom.write_8(room.addr, ts_num)
                        new_tilesets.append(tileset)
                        room_tilesets[key] = tileset
                    bg1_val = tileset.add_item_graphics(sprite)

            # Overwrite BG1 if not hidden
            if not min_loc.hidden:
                room = RoomEntry(rom, min_loc.area, min_loc.room)
                with room.load_bg1() as bg1:
                    bg1.set_block_value(min_loc.block_x, min_loc.block_y, bg1_val)

            # See struct MinorLocation in include/structs/randomizer.h
            rom.write_32(minor_loc_addr, min_loc.key)
            rom.write_16(minor_loc_addr + 4, bg1_val)
            rom.write_8(minor_loc_addr + 6, min_loc.new_item.value)
            rom.write_8(minor_loc_addr + 7, min_loc.item_jingle.value)
            rom.write_8(minor_loc_addr + 8, min_loc.hint_value)
            self.write_item_messages(seen_messages, min_loc.item_messages, minor_loc_addr, False)
            minor_loc_addr += 0x10

            if min_loc.hinted_by != HintLocation.NONE:
                room = RoomEntry(rom, min_loc.area, min_loc.room)
                map_x, map_y = room.map_coords_at_block(min_loc.block_x, min_loc.block_y)
                target_addr = hint_targets_addr + (min_loc.hinted_by.value * 0xC)
                rom.write_8(target_addr + 6, min_loc.area)
                rom.write_8(target_addr + 7, map_x)
                rom.write_8(target_addr + 8, map_y)

        self.write_new_tilesets(new_tilesets)

        # Handle major locations
        major_locs_addr = major_locations_addr(rom)
        for maj_loc in self.settings.major_locs:
            addr = major_locs_addr + (maj_loc.major_src.value * 8)
            rom.write_8(addr, maj_loc.new_item.value)
            rom.write_8(addr + 1, maj_loc.item_jingle.value)
            rom.write_8(addr + 2, maj_loc.hint_value)
            self.write_item_messages(seen_messages, maj_loc.item_messages, addr, True)

            if maj_loc.hinted_by != HintLocation.NONE:
                target_addr = hint_targets_addr + (maj_loc.hinted_by.value * 0xC)
                rom.write_8(target_addr + 6, maj_loc.area)
                rom.write_8(target_addr + 7, maj_loc.map_x)
                rom.write_8(target_addr + 8, maj_loc.map_y)

    def write_new_tilesets(self, new_tilesets: list[TilesetData]) -> None:
        rom = self.rom

        # Get existing tileset data
        tileset_addr = tileset_entries(rom)
        orig_tileset_size = tileset_count(rom) * TILESET_SIZE
        tileset_data = rom.read_bytes(tileset_addr, orig_tileset_size)

        # Get existing animated tileset data
        anim_tileset_addr = anim_tileset_entries(rom)
        orig_anim_tileset_count = anim_tileset_count(rom)
        orig_anim_tileset_size = orig_anim_tileset_count * ANIM_TILESET_SIZE
        anim_tileset_data = rom.read_bytes(anim_tileset_addr, orig_anim_tileset_size)

        # Append data for each new tileset and animated tileset
        for i, tileset in enumerate(new_tilesets):
            tileset_data += tileset.write_copy(orig_anim_tileset_count + i)
            anim_tileset_data += tileset.anim_tileset

        # Write data to ROM and repoint
        rom.write_repointable_data(
            tileset_addr,
            orig_tileset_size,
            tileset_data,
            [ReservedPointersZM.TILESET_ENTRIES_PTR.value],
        )
        rom.write_repointable_data(
            anim_tileset_addr,
            orig_anim_tileset_size,
            anim_tileset_data,
            [ReservedPointersZM.ANIM_TILESET_ENTRIES_PTR.value],
        )

    def write_item_messages(
        self,
        seen_messages: dict[str, int],
        messages: ItemMessages | None,
        loc_addr: int,
        is_major: bool,
    ) -> None:
        rom = self.rom
        id_offset = 3 if is_major else 9
        custom_offset = 4 if is_major else 0xC

        if messages is None:
            rom.write_8(loc_addr + id_offset, 0xFF)
            rom.write_32(loc_addr + custom_offset, 0)  # NULL
        elif messages.kind == ItemMessagesKind.MESSAGE_ID:
            rom.write_8(loc_addr + id_offset, messages.message_id)
            rom.write_32(loc_addr + custom_offset, 0)  # NULL
        elif messages.kind == ItemMessagesKind.CUSTOM_MESSAGE:
            # Reserve space for pointers for each language
            table_addr = rom.reserve_free_space(len(Language) * 4)
            for lang in Language:
                # English is required to be set - use English as the fallback value
                msg_text = (
                    messages.item_messages[lang]
                    if lang in messages.item_messages
                    else messages.item_messages[Language.ENGLISH]
                )
                text_ptr = table_addr + (lang.value * 4)
                # Check if text has been seen before
                text_addr = seen_messages.get(msg_text)
                if text_addr is None:
                    encoded_text = encode_text(
                        rom, MessageType.TWO_LINE, msg_text, centered=messages.centered
                    )
                    text_addr = rom.write_data_with_pointers(encoded_text, [text_ptr])
                    seen_messages[msg_text] = text_addr
                rom.write_ptr(text_ptr, text_addr)
            rom.write_8(loc_addr + id_offset, 0xFF)
            rom.write_ptr(loc_addr + custom_offset, table_addr)


def set_tank_increments(rom: Rom, data: MarsschemazmTankIncrements) -> None:
    addr = tank_increase_amounts_addr(rom)
    rom.write_16(addr, data["energy_tank"])
    rom.write_16(addr + 2, data["missile_tank"])
    rom.write_8(addr + 4, data["super_missile_tank"])
    rom.write_8(addr + 5, data["power_bomb_tank"])
