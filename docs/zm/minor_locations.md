# Minor Locations

## Minor Location Overview

Minor location items are items obtained by touching a block in a room that has special clipdata. Major location items are obtained by touching a sprite (such as a chozo statue). Minor location graphics are part of the room's tileset, whereas major location graphics are part of the sprite.

### Minor Location Data Structure

The minor location struct is defined in `include/structs/randomizer.h` in the decomp repo. It has the following fields:

- `u32 key`: The key used when the game searches for this location.
- `u16 bg1Value`: The BG1 block value for this location. Only used when the block is hidden.
- `RandoItemType item`: The item obtained from this location.
- `RandoItemJingle jingle`: The jingle that plays when the item is obtained. The options are default, minor, major, unknown, and fully powered.
- `u8 messageId`: An optional ID for the message that should be displayed when the item is obtained.
- `const u16 *(*customMessage)[LANGUAGE_COUNT]`: An optional pointer to an array of pointers (one for each language) to a custom message that should be displayed when the item is obtained.

To use the default message, `messageID` should be 0xFF (`UCHAR_MAX`) and `customMessage` should be `NULL`.

## How the Game Handles Minor Locations

When any tank clipdata is touched, the game performs a binary search on an array of every minor location in the game. The key for the search is based on the item's area, room, X position, and Y position. Since binary search is used, the locations need to be stored in sorted order.

Once a location is found, the data for that location will determine which item to obtain, which jingle to play, and what message to display.

A search for the minor location is also done if a hidden tank is revealed, in order to display the correct BG1 block value.

## Minor Location Graphics

At a high level, minor location item graphics are handled by creating new tilesets for each room with an item. This allows any palette to be used for each item. New item graphics aren't required for tanks, since they're already part of every tileset.

Adding item graphics to a tileset requires modifying three pieces of data in the tileset: the palette, the animated tileset, and the tilemap. For each room with items, the room's tileset needs enough space in the palette and animated tileset for each item. The patcher finds blank palette rows by checking if all colors in the row are the same. For animated tilesets, slots with a graphics ID of 0 are considered blank. For tilemaps, the four blocks after the tanks (0x4C-0x4F) are always blank. All tileset palettes in the game have at least one blank row, and all animated tilesets have at least four blank slots.

In order to save space in the ROM, the patcher fills up palettes, animated tilesets, and tilemaps until they have no more blank slots. This avoid duplicating all the data each time a room is given a new tileset.

### Patcher Algorithm Details

- Get minor locations with non-tank items and group them by room
- Find the empty slots in each palette and animated tileset used in those rooms
- Create dictionaries to track data and the items added to them
- Go through each room with minor locations
  - Get the palette list from the dictionary. See if there's a palette in the list with enough space for the items in the room. If not, make a new palette and add it to the list
  - Add items to palette and store the rows used
  - Do the same as above to get an animated tileset
  - Add items to animated tileset and store the slots used
  - Do the same as above to get a tilemap
  - Add items to tilemap using the rows and slots
  - Store the BG1 block value for each location
  - Track which palette, animated tileset, and tilemap were used for each room
- For each list of data, overwrite the first one, and create new entries for the remainder
  - Each additional animated tileset is given a new number
- For each room and the data used for it
  - Create a new tileset entry that points to the palette, animated tileset, and tilemap
  - Write the tileset's ID to the room entry
- Write all the new tileset entries and animated tileset entries
  - Append the new entries to the existing entries and repoint the arrays
- For all minor locations
  - Write to the ROM, using stored BG1 for non-tanks
