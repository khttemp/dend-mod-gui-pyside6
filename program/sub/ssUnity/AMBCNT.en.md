*[日本語](AMBCNT.md)*

# AMB Elements (SS)

This explains SS's AMB.

## Note

Before looking at the AMB items, first make sure you understand rail data.

## AMB Flags

Looking at the AmbCnt: item, there is another number next to the actual AMB index count.

This is a flag for applying the last element, kasenchu_per,

and it is applied when set to 1 or higher.

If set to 0, it is not applied, and kasenchu_per becomes a fixed value of 1.

This flag should normally be left at 1 and not touched.

## index

The current index of this AMB.

The numbers don't necessarily need to stay in matching order (since indexes are assigned in the order they are read internally),

but assigning an index makes it easier to make corrections when adjusting AMB.

## rail

Sets which rail number's reference point the first AMB to be placed is positioned against.

In other words, to place an AMB, the rail must be completed first.

It is placed based on the very first point (bone 0) of the specified rail.

## length

The AMB model is displayed when the distance from the model's center to the vehicle's position

is within the specified distance range.

It's normally fine to leave this fixed at 1000.

## amb_data

The number of actual models one AMB holds.

<br>

Since this is a 【count】, it must ALWAYS be 1 or more.

If specified as "0 or less", the AMB will "technically" not be displayed at all,

and no serious error that would freeze the game will occur (though it will show as an error in the log),

but since it causes an error when exporting to Excel,

anything specified as 0 or less must always be removed.

<br>

After placing a model for one AMB, specifying the next AMB model

places it in accordance with the direction the preceding AMB points to, following the parentIndex described below.

## mdl_no

The AMB model number defined in MdlCnt.

For the list of models that can be used as AMB, see the [【here】](/program/sub/ssUnity/AMBLIST.md) link.

## parentIndex

![parentIndex](/program/sub/ssUnity/image/parentIndex.png)

Among the models one AMB holds, this is the AMB_index of its own parent.

In other words, it forms a hierarchy across however many models are defined in amb_data,

and the very first model to be placed has parentIndex -1.

Since the internal AMB_index is defined based on this information,

the ordering must be preserved starting from -1.

## pox_x, pox_y, pos_z

![AMB_pos](/program/sub/ssUnity/image/AMB_pos.png)

Same as the rail's pos_x, pos_y, pos_z,

this translates the model in parallel.

## dir_x, dir_y, dir_z

![AMB_dir](/program/sub/ssUnity/image/AMB_dir.png)

The naming is a bit confusing, but

**this is different from the rail's dir_x, dir_y, dir_z.**

Unlike a partial rotation used to bend something,

this means rotation of the entire model itself.

## joint_dir_x, joint_dir_y, joint_dir_z

![AMB_joint_dir](/program/sub/ssUnity/image/AMB_joint_dir.png)

This one

is the same as the rail's dir_x, dir_y, dir_z.

## per

Same as the rail's per,

this is the multiplier for how much to stretch the model.

1.0x is the default length, and it can be fine-tuned down to decimal places.

Less than 1 shrinks it, and greater than 1 stretches it.

## kasenchu_per

Unless the flag described above in "AMB Flags" is set to 1 or higher,

this one cannot be finely configured.

Also, kasenchu_per is only applied to models where the AMB object has

an item called 【mKasenChu】 defined,

and like per, it is the multiplier for how much to stretch it.

![kasenchu_per](/program/sub/ssUnity/image/kasenchu_per.png)

Models that have this item include

the model AMB_Kasenchu_Short, for example.

![kasenchu_per2](/program/sub/ssUnity/image/kasenchu_per2.png)

Setting per greater than 1.0 causes it to stretch sideways.

The AMBs that have mKasenChu are as follows.

| Model Name |
| --- |
| AMB_BLACK_CHU |
| AMB_BlackCube |
| AMB_HQ_KasenLong0 |
| AMB_Kaidan2 |
| AMB_Kasenchu_Center |
| AMB_Kasenchu_Left |
| AMB_Kasenchu_Long0 |
| AMB_Kasenchu_Long1 |
| AMB_Kasenchu_Long2 |
| AMB_Kasenchu_Short |
| AMB_Mina_Wall2 |
| AMB_SAKU |
| AMB_Toyo_Kasenchu |
| AMB_TQ_Kaidan3 |
| TQ_Eda_Iron |
| TQ_Eda_Yane |

## ※ AMB Models with Collision Detection

### Unable to Move Under Its Own Power if Drifted Into

| Model Name |
| --- |
| AMB_Bridgh_W_Hashira |
| AMB_CHIKA_IN |
| AMB_MetalBox |
| AMB_MetalBox_50 |
| AMB_UNDER_HASHIRA |
| AMB_UNDER_HASHIRA2 |
| AMB_UNDER_HASHIRA4 |
| AMB_UNDER_IN |
| TQ_Obj0 |

### Unable to Move Under Its Own Power if Crashed Into, Regardless of Drift

| Model Name |
| --- |
| AMB_3300Body |
| AMB_Stop |
| RailEnd |
| UmedaStop |

### Becomes Airborne if Drifted Into (Cancelled in the Case of One-Wheel Drift)

| Model Name |
| --- |
| AMB_1RAIL_UNDER_IN |
| AMB_DriftBlock |
| AMB_TQ_Wall0 |
| AMB_TrackMdl |
