# Changelog

## Unreleased - 2026-??-??

## 0.16.0 - 2026-08-24

- Updated ASM patches to [0.13.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.13.0)

## 0.15.0 - 2026-06-25
### Fusion
- Updated ASM patches to [0.12.3](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.12.3)

### Zero Mission
- Added: Optional patch to reveal hidden tiles.
- Added: New item types:
  - Spring Ball
  - Wall Jump
  - Infinite Bomb Jump
  - Progressive Jump
  - Progressive Bomb
- Removed: Options to disable mid-air bomb jumps and wall jumps.

## 0.14.2 - 2026-05-15
### Fusion
- Fixed: Letter casing for Initial and Confirmation text definitions in schema.

## 0.14.1 - 2026-05-11
### Fusion
- Fixed: Minimap no longer incorrectly displays horiziontally and/or vertically flipped tiles.

## 0.14.0 - 2026-05-11
### General
- Changed: Field names in the schema have been standardized to lowercase `snake_case`.

### Zero Mission
- Added: Support for writing hint text at dedicated chozo statues.
- Fixed: The palette for the Gunship in the intro while it is landing is now randomized.
- Added: Support for writing room names. View the name of the current room on the Pause Screen by pressing the `A` button.
- Added: Support for writing text on the title screen.
- Added: Several options:
  - Skip door transitions
  - Default stereo audio
  - Disable music
  - Disable sounds
  - Remove cutscenes
  - Fast item grab
- Added: Support for writing the Seed Hash on the file select screen.
- Added: Support for writing the intro text.
- Added: Support for writing custom credits.
- Changed: Item graphics for unknown items have been replaced with custom graphics.
- Removed: Starting Location in Crateria at Door 0.
- Added: Support for changing the item that the Space Pirate in Chozodia is carrying.
- Added: Shiny items palette.
- Changed: Item graphics for the following:
  - "anonymous" item
  - charge beam
  - ice beam
  - main missiles
  - main power bombs
  - main super missiles
  - plasma beam
  - wave beam
  - ziplines
- Fixed: You can now peek the item in the caterpillar room in Norfair from the right side.


## 0.13.0 - 2026-04-17
### Fusion
- Update ASM patches to [0.12.2](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.12.2)
- Fixed: B.O.X. Minimap tile.

### Zero Mission
- Added: Support for changing item graphics at minor locations.
- Added: Support for custom messages on items.
- Added: Support for starting locations.
- Added: Support for starting items.
- Added: Support for randomized palettes.
- Added: Support for Main Missile, Main Super Missile, and Main Power Bomb items.
- Added: Support for replacing major or minor location graphics with any item sprite.

## 0.12.0 - 2026-02-26
### General
- Added: Music shuffling, this shuffles the tracks, not the assignment to a room.

### Fusion
- Update ASM patches to [0.12.1](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.12.1)
- Changed: Door transitions are no longer deleted in Door Lock Randomizer when a door is randomized as permanently locked.

## 0.11.0 - 2026-02-20
### Fusion
- Update ASM patches to [0.12.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.12.0)
- Fixed: Minimap tiles no longer display incorrectly.
- Added: Customizable environmental damage.
- Fixed: Boss icons on minimap are no longer inconsistent.

## 0.10.0 - 2026-01-16
### Fusion
- Update ASM patches to [0.11.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.11.0)
- Added: Additional item sprites for potentially new items and multiworld items.

## 0.9.0 - 2026-01-03
### Fusion
- Update ASM patches to [0.10.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.10.0)
- Added: Support for shuffling Open Hatch type in Door Lock Randomizer.
- Changed: Door Lock Randomizer now excludes certain doors in rooms where more than 6 total hatches are available.
- Changed: Door Lock Randomizer now appropriately changes the minimap.
- Fixed: Door Lock Randomizer no longer causes an export failure.
- Fixed: An error will occur when changing door locks to prevent minimap from being changed in multiple ways.

### Zero Mission
- Added: Basic item randomization.

## 0.8.3 - 2025-09-26
### Fusion
- Update ASM patches to [0.9.2](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.9.2)

## 0.8.2 - 2025-09-23
### Fusion
- Update ASM patches to [0.9.1](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.9.1)

## 0.8.1 - 2025-09-22
### General
- Fixed: Fusion no longer has export failures due to missing assembly patches and other missing data.

## 0.8.0 - 2025-09-19
### Fusion
- Update ASM patches to [0.9.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.9.0)
- Fixed: Text now properly follows the currently speaking character. E.G. Adam, Federation, Samus
- Fixed: Text wrapping behavior is now more consistent.
- Added: Option for adding Instant Morph by pressing Select button in-game.
- Changed: Randovania credits header moved down to make it visually distinct from other credits groupings.

### Zero Mission
- Begin implementation.

---

> [!NOTE]
> Prior to version 0.8.0, only Metroid Fusion existed as a supported game in the patcher. All updates below can be considered exclusively for Metroid Fusion. Future changelog entries will distinguish between the changes for each game or if the changes affect the patcher in general.

## 0.7.3 - 2025-08-29
- Update ASM patches to [0.8.2](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.8.2)

## 0.7.2 - 2025-08-26
- Update ASM patches to [0.8.1](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.8.1)

## 0.7.1 - 2025-08-25
- Removed: Patcher version number is no longer reserved as the first position on the title screen.

## 0.7.0 - 2025-08-25
- Update ASM patches to [0.8.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.8.0)
- Added: Ability to write text to the title screen.
  - Default text written to the title screen includes the versions of Randovania and the patcher.
- Removed: Anti-Softlock option.
- Fixed: Exporting changes that involve Minimap tiles and tunnels no longer cause an error and export failure.

## 0.6.2 - 2025-07-15
- Update ASM patches to [0.7.2](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.7.2)

## 0.6.1 - 2025-07-15
- Update ASM patches to [0.7.1](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.7.1)
- Changed: The minimap showing a connection in Sector 5 between Flooded Tower and Ruined Break Room has been changed to indicate an impassible wall.

## 0.6.0 - 2025-07-11
- Update ASM patches to [0.7.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.7.0)
- Added: Optional accessibility patches can now be applied to aid users with gameplay.
- Added: Major and Minor Item Jingles can now be applied to any collectable.

## 0.5.0 - 2025-06-20
- Update ASM patches to [0.6.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.6.0)
- Changed: Palette randomization updated to use a random sine wave for additional color rotation.
- Changed: MARS team credits and RDV team credits are now applied via the patcher.
- Fixed: All items now have the correct palette applied in Quarantine Bay.
- Changed: Minimaps now show sector connections between sectors.
- Added: Ability to specify the increments of ammo for Missile Data and Power Bomb Data.

## 0.4.1 - 2025-05-22

### Visual
- Changed: Minimap has been updated to reflect new events, boss tiles, and security rooms.

## 0.4.0 - 2025-05-15
- Update ASM patches to [0.5.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.5.0)

## 0.3.2 - 2025-04-28
- Update ASM patches to [0.4.2](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.4.2)

## 0.3.1 - 2025-04-22
- Update ASM patches to [0.4.1](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.4.1)

## 0.3.0 - 2025-04-18
- Changed: Navigation text can now be provided as an arbitrary length instead of being confined to a maximum length.

## 0.2.0 - 2025-03-15
- Update ASM patches to [0.3.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.3.0)
- Fixed: Samus color palettes during navigation conversations are the same color as in-game randomized palettes when using palette randomizer.
- Changed: Added the ability when revealing the hidden map with door lock randomization enabled to hide the colors of the doors on the minimap until they are revealed.

## 0.1.0 - 2025-03-01
- Update ASM patches to [0.2.0](https://github.com/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tag/0.2.0)
- Changed: Description of Starting Location properties `BlockX` and `BlockY` updated for clarification.

## 0.0.1 - 2025-02-24
- Initial release with support for Metroid Fusion.
