*[日本語](FLAG.md)*

# Rail and Model Flags (SS)

This explains the rail and model flags in SS.

## Prerequisites

Some knowledge of binary is required here.

For SS rail flags, values are expanded in binary

so that each position is judged as either 0 or 1.

![flag](/program/sub/ssUnity/image/flag.png)

In the Windows calculator, select Programmer mode,

and click the square area shown in the image to view the value in binary.

![flag2](/program/sub/ssUnity/image/flag2.png)

Within that, rail data

splits the flag into four parts like this,

and basically judges up to 32 possible states.

![flag3](/program/sub/ssUnity/image/flag3.png)

For example, when a rail data flag is defined like this,

converting it to a binary flag gives this.

### 1st flg

![flagNum1](/program/sub/ssUnity/image/flagNum1.png)

~~【8th】~~

**Unused.** In older titles this was the crossing passage sound setting, but it is already implemented inside the model itself.

【7th】(64)

When drifting on double track, it becomes unable to move under its own power while airborne.

※For other collision judgments, see the [【here】](/program/sub/ssUnity/AMBCNT.md) link.

~~【6th】~~

**Unused.**

~~【5th】~~

**Unused.**

~~【4th】~~

**Unused.**

~~【3rd】~~

**Unused.**

【2nd】(2)

Bridge passage sound setting

【1st】(1)

No drift. Makes it so the train cannot drift.

### 2nd flg

![flagNum2](/program/sub/ssUnity/image/flagNum2.png)

~~【8th】~~

**Unused.**

【7th】(64)

Makes other rails a drift target as well.

Allows drifting onto an adjacent rail with a completely different rail number.

~~【6th】~~

**Unused.**

~~【5th】~~

**Unused.**

~~【4th】~~

**Unused.**

【3rd】(4)

Undoes the CPU's one-wheel drift.

【2nd】(2)

Makes the CPU one-wheel drift to the right.

【1st】(1)

Makes the CPU one-wheel drift to the left.

### 3rd flg

![flagNum3](/program/sub/ssUnity/image/flagNum3.png)

【8th】(128)

Gets bounced off no matter which direction the one-wheel drift goes.

【7th】(64)

On the right-hand rail of double track, gets bounced off only when one-wheel drifting to the right.

【6th】(32)

On the left-hand rail of double track, gets bounced off only when one-wheel drifting to the left.

~~【5th】~~

**Unused.**

~~【4th】~~

**Unused.**

~~【3rd】~~

**Unused.**

【2nd】(2)

If a rail guard can be placed on the right side, it is placed.

【1st】(1)

If a rail guard can be placed on the left side, it is placed.

### 4th flg

![flagNum4](/program/sub/ssUnity/image/flagNum4.png)

【8th】(128)

Disabled rail. That is, it exists as data but is treated as invalid.

This is used, for example, so that if a rail data set is complete but a correction becomes necessary partway through,

the index numbers can be shifted as little as possible.

【7th】(64)

Makes the CPU switch tracks.

~~【6th】~~

**Unused.**

~~【5th】~~

**Unused.**

~~【4th】~~

**Unused.**

【3rd】(4)

Undoes the CPU's drift.

【2nd】(2)

Makes the CPU drift to the right.

【1st】(1)

Makes the CPU drift to the left.


## Model Flags

![mdlFlg](/program/sub/ssUnity/image/mdlFlg.png)

The model flag uses two elements.

### Model's 1st flg

![mdlFlagNum1](/program/sub/ssUnity/image/mdlFlagNum1.png)

【4th?】(8)

AMB setting.

It does not actually appear to be checked anywhere, so this seems to be a note rather than a functional flag.

【6th】(32)

Bridge passage sound setting (same as bit 2 of the rail flag's 1st flg)

~~【Other】~~

**Unused.**

### Model's 2nd flg

![mdlFlagNum2](/program/sub/ssUnity/image/mdlFlagNum2.png)

【8th】(128)

When drifting on double track, becomes unable to move under its own power while airborne (same as bit 7 of the rail flag's 1st flg)

【7th】(64)

On the right-hand rail of double track, gets bounced off only when one-wheel drifting to the right (same as bit 7 of the rail flag's 3rd flg)

【6th】(32)

On the left-hand rail of double track, gets bounced off only when one-wheel drifting to the left (same as bit 6 of the rail flag's 3rd flg)

【5th】(16)

Gets bounced off no matter which direction the one-wheel drift goes (same as bit 8 of the rail flag's 3rd flg)

~~【4th】~~

**Unused.**

~~【3rd】~~

**Unused.**

~~【2nd】~~

**Unused.**

【1st】(1)

No drift. (same as bit 1 of the rail flag's 1st flg)
