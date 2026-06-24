# Changelog

## Unreleased - 2025-??-??

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
