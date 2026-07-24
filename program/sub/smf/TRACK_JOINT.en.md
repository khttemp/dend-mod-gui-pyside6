*[日本語](TRACK_JOINT.md)*

# Bogie Position, Adjusting Distance Between Cars

![title](image/joint.png)

When assembling a train set, depending on the model's length,

if the cars end up overlapping like this,

you need to change the position of "F_JOINT" and "B_JOINT" in the SMF

![title](image/joint_pos.png)

Also, depending on the model, "F_JOINT_POS" and "B_JOINT_POS" may be

defined, so adjust them as needed.

You only need to adjust the "Z coordinate"

![title](image/bjoint.png)

With the current settings, the "B_JOINT" position of the lead car is here

![title](image/fjoint.png)

and since the "F_JOINT" position of car 2 is here,

![title](image/bfjoint.png)

when assembling, the cars are placed to align the "B_JOINT" and "F_JOINT" positions,

so an overlapping section like this ends up occurring

![title](image/bjoint2.png)

Therefore, adjust so the "B_JOINT" position ends up here

(change B_JOINT_POS to -20.55)

![title](image/fjoint2.png)

and adjust so the "F_JOINT" position ends up here

(change F_JOINT_POS to 18.15)

![title](image/bfjoint2.png)

and it will be arranged like this.

Adjust with appropriate values.

<br><br><br>

## Bogie Position

![title](image/track.png)

To adjust the bogie position,

adjust the position of the model's "TRACK00" and "TRACK01"

*The current Z value of TRACK00 is "15.0", and the Z value of TRACK01 is "-15.0"

![title](image/track2.png)

If you set TRACK00's value to "13.0" and TRACK01's Z value to "-17.0",

![title](image/track3.png)

it will be adjusted like this.

Likewise, adjust with appropriate values.