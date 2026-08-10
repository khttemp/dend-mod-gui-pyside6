*[日本語](RAILCNT.md)*

# Rail Data Elements (SS)

This explains the SS rail data.

## Prerequisite Knowledge

First, regarding rail models,

there's something you need to keep in mind.

![model](/program/sub/ssUnity/image/model.png)

Given a model like the one in the diagram,

![model_bone](/program/sub/ssUnity/image/model_bone.png)

this model is split into 8 sections that each move independently, like a spine.

Each of these 8 sections is called a **[bone]**.


![model_bone2](/program/sub/ssUnity/image/model_bone2.png)

The bones of single-track and double-track are structured as follows.

Starting from the leftmost side, they are numbered 0-7 from the bottom.

For double-track, moving to the right adds 100, so they are renumbered 100-107 from the bottom.

For quadruple-track, naturally the count keeps increasing by 100, becoming 200-207, then 300-307.

<br>

![xyz](/program/sub/ssUnity/image/xyz.png)

Unity's XYZ coordinate system looks like this.

![xyz2](/program/sub/ssUnity/image/xyz2.png)

Note that this is not the same XYZ as in something like Blender.

This is the most important thing, so make sure to remember it.


## index

The current index of this rail.

The numbers don't necessarily need to be in order (since numbering is assigned based on the order they're loaded internally),

but when adjusting rails, assigning an index makes it easier to make modifications.

## prev_rail

The number indicating which rail index the rail model itself is placed relative to.

If -1, it is placed from the origin.

![prev_rail](/program/sub/ssUnity/image/prev_rail.png)

In other words, if rail No. 52 is placed like this,

![prev_rail2](/program/sub/ssUnity/image/prev_rail2.png)

specifying the rail's<br>index: 53<br>prev_rail: 52<br>places it like this.

It is placed to align with the direction of the last bone pointed to by the preceding prev_rail.

## block

Can be thought of as the group number under which the rail is displayed.

Based on the block number of a rail determined from the current car position,

the current block number and the block numbers ±1 from it are displayed.

## pox_x, pox_y, pos_z

Relative to the position set by the 2nd element, prev_rail,

these are the XYZ values used to translate it.

![pos](/program/sub/ssUnity/image/pos.png)

The reason this is needed is that when placed via prev_rail,

it is always **[center-aligned]** as shown in the diagram, so pos_x needs to be adjusted.

![pos2](/program/sub/ssUnity/image/pos2.png)

The diagram shows the result after adjusting the value of pos_x.

The distance to adjust is always **[6.5]**.

If you want to connect a single-track to the left side of **prev_rail's double-track**, adjust by [-6.5].

If connecting to the right side, adjust by [6.5].

Alternatively, if you want to connect **prev_rail's single-track** to the left side of the current double-track, adjust by [6.5].

If connecting to the right side, adjust by [-6.5].

<br>

Otherwise, adjusting pos_y and pos_z is **rarely** needed.

Since these translate up/down or forward/backward relative to prev_rail,

they are used mainly when laying out a line that starts from a completely different starting point.

## dir_x, dir_y, dir_z

Relative to the position set by the 2nd element, prev_rail,

these are the XYZ values used to rotate it.

![dir](/program/sub/ssUnity/image/dir.png)

This shows the result of applying somewhat extreme values,

but keep in mind that it bends in this kind of direction.

## mdl_no

The rail model number defined in MdlCnt.

For the list of models that can be used as rails, see [【here】](/program/sub/ssUnity/RAILLIST.md).

## mdl_kasenchu

The overhead wire pole model number for the rail, defined in MdlCnt.

Regardless of case, any model whose name contains

"kasenchu" can basically be placed as an overhead wire pole.

1. If -1 or 255, it calls the model's default overhead wire pole

    as defined in MdlCnt.

    If this default overhead wire pole is also -1, there is no overhead wire pole.

2. If -2 or 254, there is no overhead wire pole.

3. For any other value, it calls that model.

## per

The scale factor for how much to stretch the model.

1.0 is the default length, and it can be adjusted finely down to decimal places.

Less than 1 shrinks it, and greater than 1 stretches it.

## flg

The flag defining what state the rail should be in.

For details on the flags, see [【here】](/program/sub/ssUnity/FLAG.md).

If you're not sure, it's fine to start with all 4 set to 0 (0x00).

## rail_data

Defines the **number** of ways the rail model can proceed.

If 1, it behaves as single-track progression,

if 2, double-track progression,

and if 4, quadruple-track progression.

Also, writing a double-track progression on a single-track rail,

or a single-track progression on a double-track rail,

can result in an error.

## next_rail, next_no, prev_rail, prev_no

Defines the specific way the rail progresses.

next_rail and next_no define which rail and bone number to proceed to next.

prev_rail and prev_no define the rail and bone number

from which the current rail was connected and reached.

Setting next_rail to **[-1]** means the current rail is the end,

and it's no longer possible to proceed from there.

(Note: if next_rail is -1, next_no can be any number, but it's normal to also set it to -1 to match.)

![raildata](/program/sub/ssUnity/image/raildata.png)

Given rail data like this,

![raildata2](/program/sub/ssUnity/image/raildata2.png)

an explanation of how double-track rail No. 40 progresses,

![raildata3](/program/sub/ssUnity/image/raildata3.png)

and an explanation of how single-track rail No. 41 progresses.
