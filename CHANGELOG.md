# Changelog

## Unreleased - 2026-??-??

## 0.14.2 - 2026-05-15
### Fusion
- Fixed: Letter casing for Initial and Confirmation text definitions in schema.

## 0.14.1 - 2026-05-11
### Fusion
- Fixed: Minimap no longer incorrectly displays horiziontally and/or vertically flipped tiles.

## 0.14.0 - 2026-05-11
### Zero Mission
- Added: Support for writing hint text.
- Fixed: Gunship palette
- Added: Support for writing room names.
- Added: Support for writing text on the title screen.
- Added: Several optional patches
  - Skip door transitions
  - Default stereo audio
  - Disable music
  - Disable sounds
  - Remove cutscenes
  - Fast item grab
- Added: Support for writing the Seed Hash.
- Added: Support for writing the intro text.
- Added: Support for writing custom credits.
- Changed: Item graphics for unknown items.
- Removed: Starting Location in Crateria at Door 0
- Added: Support for changing the item that the Space Pirate in Chozodia is carrying.
- Changed: Item graphics for the following
  - "anonymous" item
  - charge beam
  - ice beam
  - main missiles
  - main power bombs
  - main super missiles
  - plasma beam
  - wave beam
  - ziplines


## 0.13.0 - 2026-04-17
### Fusion
- Fixed: B.O.X. Minimap tile

### Zero Mission
- Added: Support for changing item graphics at minor locations.
- Added: Support for custom messages on items.
- Added: Support for starting locations.
- Added: Support for starting items.
- Added: Support for randomized palettes.
- Added: Support for Main Missile, Main Super Missile, and Main Power Bomb items.
- Added: Support for replacing major location graphics with any item sprite.

## 0.12.0 - 2026-02-26
### General
- Added: Music shuffling

### Fusion
- Changed: Door transitions are no longer deleted in Door Lock Randomizer when a door is randomized as permanently locked.

## 0.11.0 - 2026-02-20
### General
- Notable mention to Archipelago APworld

### Fusion
- Fixed: Minimap tiles no longer display incorrectly token when talking to the computer or in the intro cutscene.
- Added: Customizable environmental damage.
- Fixed: Boss icons on minimap are no longer inconsistent.

## 0.10.0 - 2026-01-16
### Fusion
- Added: Additional Item types for potentially new items and multiworld items

## 0.9.0 - 2026-01-03
### General
- Added: Minimap tile creator for use with the patcher
- Changed: Free space is now better tracked and managed when patching games.

### Fusion
- Added: Support for shuffling Open Hatch type in Door Lock Randomizer
- Changed: Excludes Doors in Cathedral to C. Save Access to prevent more than 6 total hatches.
- Fixed: Doors deleted by MAGE or ASM changes no longer cause patching failure.
- Fixed: Validation for changing door locks to prevent minimap from being changed in multiple ways.

### Zero Mission
- Added: Basic item randomization

## 0.8.3 - 2025-09-26
### Fusion
- Updated ASM patches

## 0.8.2 - 2025-09-23
### Fusion
- Changed: Instant morph removed as an optional patch, and instead changes an in-ROM byte to toggle enablement.

## 0.8.1 - 2025-09-22
### General
- Split game data in project package setup configuration.

## 0.8.0 - 2025-09-19
### Fusion
- Changed: Metroid Fusion Stereo default IPS patch has been ported into ASM. Instead a flag in ROM will set the default speaker setup to stereo.
- Fixed: Text now properly follows the currently speaking character. E.G. Adam, Federation, Samus
- Added: Optional patch for Instant Morph by pressing Select button in-game.

### Zero Mission
- Begin implementation

## 0.7.3 - 2025-08-29
- Updated ASM patches

## 0.7.2 - 2025-08-26
- Updated ASM patches

## 0.7.1 - 2025-08-25
- Changed: Patcher no longer hard-codes its version number to the first line.

## 0.7.0 - 2025-08-25
- Added: Ability to write text to the title screen.
- Removed: Anti-Softlock option.

## 0.6.2 - 2025-07-15
- Updated ASM patches

## 0.6.1 - 2025-07-15
- Changed: The minimap showing a connection in Sector 5 between Flooded Tower and Ruined Break Room has been changed to indicate an impassible wall.

## 0.6.0 - 2025-07-11
- Added: Optional accessibility patches can now be applied to aid users with gameplay.
- Added: Major and Minor Item Jingles can now be applied to any collectable.

## 0.5.0 - 2025-06-20
- Changed: Palette randomization updated to use a random sine wave for additional color rotation.
- Changed: MARS team credits and RDV team credits are now applied via the patcher.
- Fixed: Quarntine Bay palettes now have the alternate tank palette properly applied.
- Changed: Minimaps now show sector connections between sectors.
- Added: Main Explosive weapons ammo increments.

## 0.4.1 - 2025-05-22

### Visual
- Changed: Base Minimap Edits has been updated to reflect new events, boss tiles, and security rooms.

## 0.4.0 - 2025-05-15
- Changelog Created
- Added: 6 new Item Locations. 3 Major/Events: Boiler, Animals, Auxiliary Power. 3 Minor/Tanks: Subzero Containment, Quarantine Bay, Northeast Stabilizer
- Added: Infrastructure to define base minimap edits that will always apply.
