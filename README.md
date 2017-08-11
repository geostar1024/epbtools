# epbtools

python 3 script to parse Empyrion's EPB format

## NOTE! For Alpha 6 only!

This python function parses Empyrion Galactic Survival's EPB format (in which the blueprints for ships and bases are stored). Its current capabilities are detailed below (including a few basic operations on the block data that are not well-supported yet):

### Current state

Currently, the script can retrieve:

* blueprint type
* blueprint size
* steam id and name for original creator
* steam id and name for current blueprinter
* number of lights
* number of devices
* total number of blocks
* number of triangles
* list of devices and blocks, and how many of each
* partial list of device groups, and their contents
* decompressed grid data (from PKZIP format)
* block position, damage state, color, texture, and symbol data extracted to 3D array

#### Block operation functions

* changeAllBlockProperty(property,newValue) : replaces the value of the specified property on *all* blocks in the grid
* changeAllBlockPropertyConditional(conditionProperty,conditionValue,property,newValue) : replaces the value of the specified property only on blocks that have a property with a certain value
* listAllBlocks() : prints out the entire grid

### Missing functionality

* complete list of block ids and names
* significance of most bytes in the header (above the steam id section)
* extraction of device groups, and their contents
* extraction of signal logic
* miscellaneous unknown bytes throughout the file

## Usage

Just put `from epbtools.readepb import readepb,writeepb` at the top of your file.

Call `readepb` like so:

`blueprint=readepb(filename)`

Call `writeepb` like so:

`writeepb(filename,blueprint)`

Use the block operations like so:

`blueprint.getProp("Grid").changeAllBlockPropertyConditional("Type",147,"Type",156)`
(replaces all "L Steel" blocks with "Combat Steel" blocks)

`blueprint.getProp("Grid").listAllBlocks()`
