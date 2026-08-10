*[日本語](TEXINFO.md)*

# Explanation of SetTexInfo (SS)

This explains SS's SetTexInfo.

![texInfo](/program/sub/ssUnity/image/texInfo.png)

Normally used when setting things like station numbers or station signs.

## amb number, amb_child number

The 2nd element specifies the amb number,

and the 3rd element identifies and applies to the model using the child number, within the amb specified by the 2nd element.

If the 2nd element is -1,

the 3rd element sets the model number (defined in MdlCnt) and applies to all models.

## Line-specific Image Data Number

The 4th element specifies, by the texture index number set in StageRes,

the value applied to the identified model.

## tex_type, change_index, mat_index, f1, f2

### Applying to the Model as a Whole

When the amb number is -1 and the setting applies to the model as a whole,

only tex_type 10 and 11 are applied.

![TqLEDBord](/program/sub/ssUnity/image/TqLEDBord.png)

【10】: Time display sign

Applied if the AMB model has "mTqLEDBord".

Among the model list defined in "mTqLEDBord",

it retrieves the LED model set by change_index,

and changes it using the line-specific image data number (res_data_index).

The AMBs that have mTqLEDBord are as follows.

| Model Name | change_index Count |
| --- | --- |
| AMB_Ichigao | 2 |
| AMB_TQ_TimeBord | 1 |
| Aobadai | 4 |
| sibuya_hashira | 1 |
| ST_IronHashira | 2 |
| takatu_st | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 1 |


![HQLEDBord](/program/sub/ssUnity/image/HQLEDBord.png)

【11】: Hankyu LED

Applied if the AMB model has "mHqLEDBord".

Among the model list defined in "mHqLEDBord",

it retrieves the LED model set by change_index,

and changes it using the line-specific image data number (res_data_index).

The AMBs that have mHqLEDBord are as follows.

| Model Name | change_index Count |
| --- | --- |
| AMB_HQ_YANE0 | 1 |
| AMB_HQ_YANE1 | 1 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |


### Applying to Part of the Model within an AMB

In this case,

only tex_type "0, 1, 2, 20, 30, 31, 32" are applied.

![Ekihyo](/program/sub/ssUnity/image/Ekihyo.png)

【0】: Station sign, front

【1】: Station sign, back

【2】: Local Y-axis flip

Applied if the AMB model has "mEkihyo".

Among the model list defined in "mEkihyo",

it retrieves the station sign model set by change_index,

and among the material list defined for that model,

it retrieves the material set by mat_index,

and changes it using the line-specific image data number (res_data_index).

Local Y-axis flip means flipping the sign 180 degrees.

The AMBs that have mEkihyo are as follows.

| Model Name | change_index Count |
| --- | --- |
| AMB_DenWall | 1 |
| AMB_Ekihyo | 1 |
| AMB_Ekihyo_Reg | 1 |
| AMB_Ekihyo_Tate | 1 |
| AMB_HQ_YANE0 | 2 |
| AMB_HQ_YANE1 | 2 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |
| AMB_MINA_ST_WALL | 1 |
| AMB_Mina_Wall | 1 |
| AMB_MM_Ekihyo | 1 |
| AMB_ShibuyaWall | 1 |
| AMB_ST_WALL | 1 |
| AMB_TQLight | 6 |
| Aobadai | 2 |
| basha_wall | 1 |
| HQ_Ekihyo | 2 |
| ST_IronHashira | 2 |
| ST_IronHashira2 | 2 |
| takatu_st | 1 |
| takatu_st_none | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Obj1 | 2 |
| tq_st_wall2 | 1 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 2 |
| Yane_W2 | 2 |


<br><br>

【20】: Platform

![HomeNo](/program/sub/ssUnity/image/HomeNo.png)

Applied if the AMB model has "mHomeNo".

Among the model list defined in "mHomeNo",

it retrieves the platform model set by change_index,

and among the material list defined for that model,

it retrieves the material set by mat_index,

and changes it using the line-specific image data number (res_data_index).

The AMBs that have mHomeNo are as follows.

| Model Name | change_index Count |
| --- | --- |
| AMB_HQ_YANE0 | 1 |
| AMB_HQ_YANE1 | 1 |
| AMB_HQ_YANE2 | 2 |
| AMB_HQ_YANE3 | 2 |
| AMB_Ichigao | 2 |
| AMB_TQ_HomeNo | 1 |
| AMB_TQLight | 3 |
| Aobadai | 4 |
| HQ_LEDBORD | 1 |
| takatu_st | 1 |
| tq_hutako | 2 |
| tq_hutako2 | 2 |
| TQ_Yane_Big | 1 |
| TQ_Yane00 | 1 |
| Yane_W | 2 |

<br><br>

![TexUV](/program/sub/ssUnity/image/TexUV.png)

【30】: Texture change

【31】: UV change

【32】: Mesh display toggle

Applied if the AMB model has "mTexUV".

Among the model list defined in "mTexUV",

it retrieves the UV model set by change_index,

and among the material list defined for that model,

it retrieves the material set by mat_index.


1. 【30】: For texture (material) change, it simply changes the texture as-is.

2. 【31】: For UV change, using the two parameters (f1, f2),

    it further fine-tunes the value as a Vector's (x, y).

3. 【32】: For mesh display toggle,

    if the line-specific image data number (res_data_index) is greater than 0, it is shown,

    and otherwise it is hidden.

The AMBs that have mTexUV are as follows.

| Model Name | change_index Count |
| --- | --- |
| AMB_SHIBU_YANE | 2 |
| sibuya_hashira | 4 |
| sibuya_hashira_only | 4 |
