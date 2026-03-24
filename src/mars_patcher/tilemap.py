from mars_patcher.compress import comp_lz77, decomp_lz77
from mars_patcher.convert_array import u8_to_u16, u16_to_u8
from mars_patcher.rom import Rom


class Tilemap:
    def __init__(self, rom: Rom, ptr: int, compressed: bool):
        self.rom = rom
        self.pointer = ptr
        self.compressed = compressed
        # Get data
        addr = rom.read_ptr(ptr)
        self.data: list[int] = []
        if compressed:
            data, self.data_size = decomp_lz77(rom.data, addr)
            self.data = u8_to_u16(data)
        else:
            addr += 2
            while True:
                val = rom.read_16(addr)
                if val == 0:
                    if len(self.data) % 4 != 0:
                        raise ValueError("Tilemap length should be a multiple of 4")
                    break
                if len(self.data) >= 1024 * 4:
                    raise ValueError("Tilemap is too long")
                self.data.append(val)
                addr += 2
            self.data_size = len(self.data) * 2 + 4

    def byte_data(self) -> bytes:
        if self.compressed:
            data = comp_lz77(u16_to_u8(self.data))
            return bytes(data)
        else:
            return bytes([2, 0]) + u16_to_u8(self.data) + bytes([0, 0])

    def write(self, copy: bool) -> None:
        data = self.byte_data()
        if copy:
            self.rom.write_data_with_pointers(data, [self.pointer])
        else:
            addr = self.rom.read_ptr(self.pointer)
            self.rom.write_repointable_data(addr, self.data_size, data, [self.pointer])
