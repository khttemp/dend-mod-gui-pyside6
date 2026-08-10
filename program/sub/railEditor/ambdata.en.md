*[日本語](ambdata.md)*

# AMB Data Elements (RS)

## 1. index

The rail number. When overwriting with CSV in RS, this information is not read.

## 2. type

Unknown.

## 3. length

Distance to the AMB. Displayed when the distance is within the specified range.

1000 is normal.

## 4. rail_no

The reference rail number where the AMB is placed.

## 5. rail_pos

Offsets by a number of bones from the reference rail number where the AMB is placed.

## 6. base_pos_x

Translates along the x-axis based on the starting point set by 4 and 5. See the diagram below.

| Default | base_pos_x (+10) | base_pos_x (-10) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_pos_x_10](/program/sub/railEditor/image/amb_base_pos_x_10.png) | ![base_pos_x_-10](/program/sub/railEditor/image/amb_base_pos_x_-10.png) |

## 7. base_pos_y

Translates along the y-axis based on the starting point set by 4 and 5. See the diagram below.

| Default | base_pos_y (+10) | base_pos_y (-5) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_pos_y_10](/program/sub/railEditor/image/amb_base_pos_y_10.png) | ![base_pos_y_-5](/program/sub/railEditor/image/amb_base_pos_y_-5.png) |

## 8. base_pos_z

Translates along the z-axis based on the starting point set by 4 and 5. See the diagram below.

| Default | base_pos_z (+10) | base_pos_z (-10) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_pos_z_10](/program/sub/railEditor/image/amb_base_pos_z_10.png) | ![base_pos_z_-10](/program/sub/railEditor/image/amb_base_pos_z_-10.png) |

## 9. base_dir_x

Rotates the entire model up/down based on the starting point set by 4 and 5. See the diagram below.

| Default | base_dir_x (+10) | base_dir_x (-10) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_dir_x_10](/program/sub/railEditor/image/amb_base_dir_x_10.png) | ![base_dir_x_-10](/program/sub/railEditor/image/amb_base_dir_x_-10.png) |

## 10. base_dir_y

Rotates the entire model left/right based on the starting point set by 4 and 5. See the diagram below.

| Default | base_dir_y (+10) | base_dir_y (-10) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_dir_y_10](/program/sub/railEditor/image/amb_base_dir_y_10.png) | ![base_dir_y_-10](/program/sub/railEditor/image/amb_base_dir_y_-10.png) |

## 11. base_dir_z

Rotates the entire model so it tilts sideways, based on the starting point set by 4 and 5.

See the diagram below.

| Default | base_dir_z (+10) | base_dir_z (-10) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![base_dir_z_10](/program/sub/railEditor/image/amb_base_dir_z_10.png) | ![base_dir_z_-10](/program/sub/railEditor/image/amb_base_dir_z_-10.png) |

## 12. priority

Unknown.

## 13. fog|child

fog → Unknown.

child → number of child models.

## 14. mdl_no

The model number in the "smf info" list.

## 15. pos_x

Based on the coordinates and orientation set in fields 6-11,

translates along the x-axis.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| base_dir_z(-10) | base_dir_z(-10)<br>pos_x(+10) | base_dir_z (-10)<br>pos_x(-10) |
| --- | --- | --- | 
| ![base_dir_z_-10](/program/sub/railEditor/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_x_10](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_x_10.png) | ![base_dir_z_-10_pos_x_-10](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_x_-10.png) |

## 16. pos_y

Based on the coordinates and orientation set in fields 6-11,

translates along the y-axis.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| base_dir_z(-10) | base_dir_z(-10)<br>pos_y(+10) | base_dir_z (-10)<br>pos_y(-5) |
| --- | --- | --- | 
| ![base_dir_z_-10](/program/sub/railEditor/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_y_10](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_y_10.png) | ![base_dir_z_-10_pos_y_-5](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_y_-5.png) |

## 17. pos_z

Based on the coordinates and orientation set in fields 6-11,

translates along the z-axis.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| base_dir_z(-10) | base_dir_z(-10)<br>pos_z(+10) | base_dir_z (-10)<br>pos_z(-10) |
| --- | --- | --- | 
| ![base_dir_z_-10](/program/sub/railEditor/image/amb_base_dir_z_-10.png) | ![base_dir_z_-10_pos_z_10](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_z_10.png) | ![base_dir_z_-10_pos_z_-10](/program/sub/railEditor/image/amb_base_dir_z_-10_pos_z_-10.png) |

## 18. dir_x

Based on the coordinates and orientation set in fields 6-11,

bends the model up/down.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| Default | dir_x (+5) | dir_x (-5) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![dir_x_5](/program/sub/railEditor/image/amb_dir_x_5.png) | ![dir_x_-5](/program/sub/railEditor/image/amb_dir_x_-5.png) |

## 19. dir_y

Based on the coordinates and orientation set in fields 6-11,

bends the model left/right.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| Default | dir_y (+5) | dir_y (-5) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![dir_y_5](/program/sub/railEditor/image/amb_dir_y_5.png) | ![dir_y_-5](/program/sub/railEditor/image/amb_dir_y_-5.png) |

## 20. dir_z

Based on the coordinates and orientation set in fields 6-11,

sets the model's cant.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below.

| Default | dir_z (+2) | dir_z (-2) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![dir_z_2](/program/sub/railEditor/image/amb_dir_z_2.png) | ![dir_z_-2](/program/sub/railEditor/image/amb_dir_z_-2.png) |

## 21. dir_x2

Based on the coordinates and orientation set in fields 6-20,

rotates the entire model up/down.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below (applied to a child model).

| Child model<br>Default | Child model<br>dir_x2 (+5) | Child model<br>dir_x2 (-5) |
| --- | --- | --- | 
| ![child_default](/program/sub/railEditor/image/amb_child_default.png) | ![dir_x2_5](/program/sub/railEditor/image/amb_dir_x2_5.png) | ![dir_x2_-5](/program/sub/railEditor/image/amb_dir_x2_-5.png) |

## 22. dir_y2

Based on the coordinates and orientation set in fields 6-20,

rotates the entire model left/right.

For the 1st entry in the sheet, this is the parent model's setting;

from the 2nd entry onward, it's the child model's setting.

See the diagram below (applied to a child model).

| Child model<br>Default | Child model<br>dir_y2 (+5) | Child model<br>dir_y2 (-5) |
| --- | --- | --- | 
| ![child_default](/program/sub/railEditor/image/amb_child_default.png) | ![dir_y2_5](/program/sub/railEditor/image/amb_dir_y2_5.png) | ![dir_y2_-5](/program/sub/railEditor/image/amb_dir_y2_-5.png) |

## 22. dir_z2

Based on the coordinates and orientation set in fields 6-20,

rotates the entire model so it tilts sideways.

See the diagram below (applied to a child model).

| Child model<br>Default | Child model<br>dir_z2 (+5) | Child model<br>dir_z2 (-5) |
| --- | --- | --- | 
| ![child_default](/program/sub/railEditor/image/amb_child_default.png) | ![dir_z2_5](/program/sub/railEditor/image/amb_dir_z2_5.png) | ![dir_z2_-5](/program/sub/railEditor/image/amb_dir_z2_-5.png) |

## 23. per

Sets the model's per value.

See the diagram below.

| Default | per(1.5) | per (0.7) |
| --- | --- | --- | 
| ![default](/program/sub/railEditor/image/amb_default.png) | ![amb_per_1.5](/program/sub/railEditor/image/amb_per_1.5.png) | ![amb_per_0.7](/program/sub/railEditor/image/amb_per_0.7.png) |
