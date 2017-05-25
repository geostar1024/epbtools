# readepb

python 3 script to parse Empyrion's EPB format

## NOTE! For Alpha 6 only!

This python function will parse Empyrion Galactic Survival's EPB format (in which the blueprints for ships and bases are stored). Its current capabilities are detailed below.

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
* size of grid data

### Missing functionality

* complete list of block ids and names
* significance of most bytes in the header (above the steam id section)
* complete list of device groups, and their contents
* support for detecting renamed devices in groups
* all grid position data
* miscellaneous unknown bytes throughout the file

## Usage

Just put `from readepb import *` at the top of your file. Call `readepb` like so:

`readepb(filename)`
