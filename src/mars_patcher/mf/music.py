from enum import IntEnum

from mars_patcher.constants.game_data import sound_data_entries
from mars_patcher.mf.auto_generated_types import MarsschemamfMusicreplacement
from mars_patcher.rom import Rom


# In-between spaces are null values
class MusicLibrary(IntEnum):
    SECTOR_1 = 0x4

    SECTOR_2 = 0x6
    SECTOR_3 = 0x7
    SECTOR_5 = 0x8
    SECTOR_4 = 0x9
    SECTOR_6 = 0xA
    NAVIGATION_ROOM = 0xB

    ITEM_FANFARE = 0x10

    SA_X_CHASE = 0x17
    BOSS_TENSION = 0x18
    ARACHNUS_BATTLE = 0x19
    ZAZABI_BATTLE = 0x1A
    BOX_BATTLE = 0x1B

    OPERATIONS_DECK_ELEVATOR_OFFLINE = 0x33
    OPERATIONS_DECK_ELEVATOR_OFFLINE_AMBIENCE = 0x34
    MAIN_BOILER_COOLDOWN_MISSION = 0x35

    ORBIT_CHANGE = 0x38

    OBJECTIVE_COMPLETE = 0x3B

    SERRIS_YAKUZA_BATTLE = 0x3F
    VARIA_CORE_X_BATTLE = 0x40
    NIGHTMARE_BATTLE = 0x41
    NEO_RIDLEY_BATTLE = 0x42
    CHOZO_STATUE_CORE_X_BATTLE = 0x43
    NETTORI_BATTLE = 0x44

    TITLE = 0x4A

    SA_X_BATTLE = 0x51


def set_sounds(rom: Rom, data: MarsschemamfMusicreplacement) -> None:
    read_SoundData = []

    # Read new data
    for New in data.values():
        read_location = sound_data_entries(rom) + 8 * MusicLibrary[New].value
        read_SoundData.append(rom.read_bytes(read_location, 8))

    # Write to rom
    for Original, SoundDatum in zip(data.keys(), read_SoundData):
        write_location = sound_data_entries(rom) + 8 * MusicLibrary[Original].value
        rom.write_bytes(write_location, SoundDatum)
