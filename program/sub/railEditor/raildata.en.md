*[日本語](raildata.md)*

# Rail Data Elements (RS)

## 1. index

The rail's number. When overwriting via CSV in RS, this info is not read in.

## 2. prev_rail

The number of the reference rail for the initial position.

If -1, it is placed from the origin;

otherwise, it is placed relative to the "end" of that rail number.

Also, if -1, it becomes a rail that can be used for Element 4.

## 3. block

The group of rails to display (treated as a block).

Roughly, all rails belonging to a block number within

±1 of the current position's block number are displayed.

## 4. dir_x

Bends the rail up or down. See the diagram below.


| Default | dir_x (+3) | dir_x (-3) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/rail_default.png) | ![dir_x_3](/program/sub/railEditor/image/rail_dir_x_3.png) | ![dir_x_-3](/program/sub/railEditor/image/rail_dir_x_-3.png) |

## 5. dir_y

Bends the rail left or right. See the diagram below.

| Default | dir_y (+3) | dir_y (-3) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/rail_default.png) | ![dir_y_3](/program/sub/railEditor/image/rail_dir_y_3.png) | ![dir_y_-3](/program/sub/railEditor/image/rail_dir_y_-3.png) |

## 6. dir_z

Sets the rail's cant. See the diagram below.

| Default | dir_z (+3) | dir_z (-3) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/rail_default.png) | ![dir_z_3](/program/sub/railEditor/image/rail_dir_z_3.png) | ![dir_z_-3](/program/sub/railEditor/image/rail_dir_z_-3.png) |

## 7. mdl_no

The model number from the "smf Info" list.

## 8. mdl_kasen

The rail's overhead wire info.

Places a model number loaded from the "smf Info" list as the overhead wire.

If -1, sets the overhead wire of the model configured in "smf Info".

If -2, no overhead wire model is placed.

## 9. mdl_kasenchu

The rail's overhead wire pole info.

Places a model number loaded from the "smf Info" list as the overhead wire pole.

If -1, sets the overhead wire pole of the model configured in "smf Info".

If -2, no overhead wire pole model is placed.

## 10. per

The rail's length multiplier. Default is 1.0x.

## 11-14. flg

The rail's flag info.

## 15. rail_data

The number of data entries that determine the rail's direction of travel.

Based on this, the amount of following data also changes.

## 16~. next_rail, next_no, prev_rail, prev_no

next_rail is the next rail number from the current rail.

next_no is the bone number of the next rail number.

prev_rail is the previous rail number from the current rail.

prev_no is the bone number of the previous rail number.

If the rail number or bone number is -1, it is treated as an end point and not connected.

The bone number depends on the length defined in "smf Info".

See the diagram below for how connections work in detail.

![rail_data](/program/sub/railEditor/image/rail_data.png)

# Element 4

![else4_1](/program/sub/railEditor/image/else4_1.png)

An additional element that can only be applied when No. 2, prev_rail, is -1.

Applies "translation and rotation" relative to the "start point" of a given rail.

However, no case of this being used in RS has been observed.

## 1. railNo

The rail number to apply this to.

## 2. prevRail

The reference rail number. The reference point is the start point of that rail number.

## 3. f1~f3

Translates along the x, y, and z axes respectively.

## 4. f4~f6

Rotates along the x, y, and z axes respectively.
