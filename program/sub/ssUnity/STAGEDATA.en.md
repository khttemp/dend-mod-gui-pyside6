*[日本語](STAGEDATA.md)*

# Elements of stagedata

This explains the SS stage data.

This does not include explanations of rail data or AMB, so

for rail data, see the link [【here】](/program/sub/ssUnity/RAILCNT.md)

for AMB, see the link [【here】](/program/sub/ssUnity/AMBCNT.md)

## Story:

As the comment says, this determines the BGM to load.

Normally you don't need to touch this.

## Dir:

As the comment says, this determines the base direction.

"1" is the default, and moves in the direction the rail was laid.

"-1" moves in the opposite direction.

However, this is often overwritten again by the Comic Script,

so normally you don't need to touch it.

By the way, you don't necessarily need to write this item;

if it doesn't exist, it's internally set to 1.

## Track:

As the comment says, this determines the bogie model.

"0" is standard gauge,

"1" is set as narrow gauge, and narrow gauge is the default.

By the way, you don't necessarily need to write this item;

if it doesn't exist, it's internally set to 1.

## COMIC_DATA

Note that this doesn't have a colon.

The number to load is determined tab-separated, and the string right below it is loaded.

Determines the folder of Comic Script to load.

## COMIC_IMAGE

Note that this doesn't have a colon.

The number to load is determined tab-separated, and the string right below it is loaded.

Determines the folder of images to load.

## COMIC_SE

Note that this doesn't have a colon.

The number to load is determined tab-separated, and the string right below it is loaded.

Determines the folder of SE (sound effects) to load.

## RailPos:

As the comment says, this determines the initial position of the train selected in "Story Mode".

The number to load is determined tab-separated, and the string right below it is loaded.

Determines the rail number, bone number, and distance from the bone number respectively.

The 3rd element is usually 0 in most cases.

However, this is often overwritten again by the Comic Script,

so unless you're modding Story Mode, normally you don't need to touch it.

## ~~FreeRun:~~

As the comment says, this determines the initial position of the train selected in "Test Run Mode".

...that's what it says, but in reality it's only loaded and not actually used.

Everything is processed by "RailPos:".

## ~~VSPos:~~

As the comment says, this determines the initial position of the train selected in "Battle Mode".

...that's what it says, but in reality it's only loaded and not actually used.

Everything is processed by "RailPos:".

## ~~VSStation:~~

It says "station judgment start"... but...

it is loaded by the internal code, but...

it's actually unused dummy data.

## ~~VSMusic:~~

It says "battle BGM change rail", but...

it's dummy data that isn't even loaded by the internal code in the first place.

## FadeImage:

The loading screen shown after selecting a stage,

and it determines the loading screen shown from reaching the goal until returning to the menu.

The number to load is determined tab-separated, and the string right below it is loaded.

The 1st element loads the den file,

and the 2nd element loads the image file within the den file.

## StageRes:

Image data by line

This is used by "SetTexInfo:", explained later.

The 2nd element loads the den file,

and the 3rd element loads the image file within the den file.

## SetTexInfo:

Image setting info

This is for setting the image of the model configured in AMB.

For a detailed explanation, see the link [【here】](/program/sub/ssUnity/TEXINFO.md)

## STCnt:

Station name info

Sets the station name displayed in the upper right.

The 2nd element is the station index used in the internal code.

The 3rd element is the rail position.

The 4th element is the offset for how far to shift from the specified rail position.

From the 5th onward, it's in the order of station name, furigana, and English notation,

but it doesn't need to be written. (Doing so displays nothing at all.)

## CPU:

Story Mode CPU switching info

The 2nd element is the rail position.

The 3rd element is the train index, a fixed value of "1".

From the 4th onward, it's almost the same as CPU_MODE in the Comic Script.

Unless you're modding Story Mode, normally you don't need to touch it.

## ComicScript:

Comic Script info to be loaded

The 2nd is the Comic Script number.

The 3rd is the Comic Script type.

The 4th is the rail position,

the 5th is the offset for how far to shift.

When you want to call it via GOTO_SCRIPT in a Comic Script,

set the rail position to -1 so it doesn't trigger on its own.

For more detailed specs, see the link [【here】](/program/sub/ssUnity/COMICSCRIPT.md)

## RainChecker:

![RainChecker](/program/sub/ssUnity/image/RainChecker.png)

This looks like it's only rain event info...

but in reality, in addition to rain events and wiper events,

it's also responsible for setting the position of the outside night view.

### Event Type

【0】：Rain stop

【3】：Wiper stop

The events look separate,

but in reality, wiper stop also performs the rain stop event simultaneously.

No parameters needed.

<br>

【1】：Rain start

【2】：Wiper start

Likewise, the events look separate,

but in reality, wiper start also performs the rain start event simultaneously.

No parameters needed.

<br>

~~【4】：Sound only stop~~

~~【5】：Sound only start~~

Dummy data

<br>

【10】：Enter underground

Hides the outside night view. No parameters needed.

【11】：Emerge from underground

Shows the outside night view. No parameters needed.

<br>

【100】：CityPos

Requires 6 parameters; adjusts the Y axis of the night view buildings.

・The 1st and 6th adjust the Y axis of City.

・The 2nd and 6th adjust the Y axis of BillMdl1, and the 3rd and 6th adjust the Y axis of BillMdl1.

・The 4th and 6th adjust the Y axis of Bill0, and the 5th and 6th adjust the Y axis of Bill1.

<br>

【101】：CityScale

Requires 2 parameters; adjusts the Scale of the night view.

・The 1st and 2nd adjust the Scale of City.

<br>

【102】：MountPos

Requires 2 parameters; adjusts the position of the outside mountains.

・The 1st and 2nd adjust the position of the mountains.

## DosanInfo:

![DosanInfo](/program/sub/ssUnity/image/DosanInfo.png)

It says "Dosan Line special area"...

but as it currently stands, the SS spec only does a high jump as-is.

### Event Prerequisites

For event_type, only 10 cannot be set.

Set the jump-triggering speed as the 1st parameter,

and if the current speed is lower than the parameter's speed, the jump event will not trigger.

### When the jump value is defined higher than 0 via (SET_LV_JUMP) in the Comic Script

To the elements of the 3rd (jump height) and 4th (how far to jump),

the jump is set by applying a multiplier equal to the value defined in SET_LV_JUMP.

### When undefined, or defined as 0 or less

The following formula is calculated.

```
num2 = (current speed - parameter 1) / (parameter 2 - parameter 1)
```

To the elements of the 3rd (jump height) and 4th (how far to jump),

the jump is set by applying a multiplier to the result value from the formula above.

However, if the result value is higher than 1.25, it's set to 1.25.


## MdlCnt:

Model info to be loaded

Everything for rail and AMB starts from here.

The 2nd element is the name of the model to load.

The 3rd and 4th elements are the flags of the model itself.

This flag is later linked with the rail's flag.

For a detailed explanation, see the link [【here】](/program/sub/ssUnity/FLAG.md)

The 5th element is the default overhead wire pole number.

It's determined from the index of MdlCnt, forming a self-referencing structure.

Overhead wire poles, regardless of upper or lower case,

can be placed as long as the name contains "kasenchu".

## RailPri:

Priority rail setting

However, this is for branch tracks connected via matching default values,

such as next_no being 0 and prev_no being 7,

and determines which way to go;

for rails connected with different next_no or prev_no numbers,

the priority rail is not applied.

## BtlPri:

Applies only in Battle Mode.

Changes the "prev" element of a given rail

entirely to the specified rail number.

Doesn't need to be written.

## NoDriftRail:

Applies only to rails that make other rails drift targets as well,

as a measure to prevent drifting on the rail specified there.

Doesn't need to be written.
