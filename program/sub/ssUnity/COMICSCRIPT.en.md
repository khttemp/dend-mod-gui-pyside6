*[日本語](COMICSCRIPT.md)*

# Explanation of ComicScript Loading (SS)

This explains the loading of SS's Comic Script.

## Explanation

### index

The current index of this script.

Since this isn't loaded, the numbers don't need to be in exact order (because numbering is assigned internally in load order),

you can assign it arbitrarily, but it's not really recommended.

### comic_bin

The 2nd element is the numeric number of the Comic Script to load.

The Comic Script file must always be named "comicXXXX.bin".

### event_type

The 3rd element is a number used to adjust whether it's loaded or skipped depending on the situation.

  * Story

    Calls scripts of type "0, 1, 2, 3, 4", and always executes the Comic Script of type "0" that was called first.

  * Battle Mode

    Calls scripts of type "3, 6", and always executes the Comic Script of type "6" that was called first.

  * Test Run

    Calls scripts of type "3, 5", and always executes the Comic Script of type "5" that was called first.

<hr>

  * Type 0 (Player)

  Story-only script. Based on the player, it runs automatically when the set rail is reached.<br>
  Setting the rail position to "-1" prevents it from running automatically, and this is used when you want to call it with "GOTO_SCRIPT"

  * Type 1 (CPU)

  Story-only script.<br>Based on the CPU, it runs automatically when the set rail is reached.

  * Type 2 (Fast)

  Story-only script.<br>It runs automatically when either the Player or the CPU reaches the set rail.

  * Type 3 (Goal)

  A script used in Story, Test Run, and Battle alike.<br>Used for things like which rail to place the goal at.<br>Normally this script is "comic2990"

  * Type 4 (GoalEvent)

  Story-only script.<br>A script that runs when the Goal event occurs in Story and the goal is reached.<br>The rail position is normally "-1".

  * Type 5 (FreeRunFastEvent)

  Test-Run-only script.<br>Called first.

  * Type 6 (BtlFastEvent)

  Battle-only script.<br>Called first.

### Rail

The 4th element determines on which rail the loaded Comic Script triggers when reached.

Scripts excluding rail number "-1" 【in load order】

keep waiting until the specified rail number is passed. The instant it's passed, the script executes.

### Offset

The 5th element is the offset for how far to shift, based on the rail position.

## Internally Set Fixed-Number Scripts

### Common

| Number | Description |
| --- | --- |
| comic2900 |・Script loaded unconditionally<br>・Script that counts down and starts |
| comic2990 |・Script loaded unconditionally<br>・Script used for event type "Goal" |
| comic2991 |・Script loaded unconditionally<br>・Called via GOTO_SCRIPT upon reaching the goal<br>・Script used to display the 【Finish】 text |
| comic2992 |・Script loaded unconditionally<br>・Script used to determine, during Battle Mode, whether a train has become unable to move under its own power
| comic2993 |・Script loaded unconditionally, Battle Mode only<br>・Script that displays 【Unable to move under own power】 and awards victory to P2 when P1 becomes unable to move under its own power |
| comic2994 |・Script loaded unconditionally, Battle Mode only<br>・Script that displays 【Unable to move under own power】 and awards victory to P1 when P2 becomes unable to move under its own power |

<hr>

### JR2000-Exclusive Event Scripts

Loaded unconditionally if there is a train with JR2000 selected.

| Number | Description |
| --- | --- |
| comic3997 | Turbine event for Story and Test Run |
| comic46020 | Turbine event for P1 in Battle Mode |
| comic46021 | Turbine event for P2 in Battle Mode |

<hr>

### KQ2199/KQ21XX-Exclusive Event Scripts

Loaded unconditionally if there is a train with KQ2199 or KQ21XX selected.

| Number | Description |
| --- | --- |
| comic21990, comic21991 | Supercharge start for Test Run Mode |
| comic21992, comic21993 | Supercharge start for Story Mode |
| comic46050, comic46052 | Supercharge start for P1 in Battle Mode |
| comic46051, comic46053 | Supercharge start for P2 in Battle Mode |

<hr>

### H4050-Exclusive Event Scripts

Loaded unconditionally if there is a train with H4050 selected.

| Number | Description |
| --- | --- |
| comic36996 | H4050 door-open event |
| comic36997 | H4050 door-open event + camera event |
| comic36999 | Exclusive event for changing to H920 |
| comic46010 | Exclusive event for P1 changing to H920 in Battle Mode |
| comic46011 | Exclusive event for P2 changing to H920 in Battle Mode |
| comic46012 | P1's H4050 door-open event + camera event in Battle Mode |
| comic46013 | P2's H4050 door-open event + camera event in Battle Mode |

<hr>

### Mu2000-Exclusive Event Scripts

Loaded unconditionally if there is a train with Mu2000 selected.

| Number | Description |
| --- | --- |
| comic36993 | Mu2000 door-close event |
| comic36994 | Mu2000 door-open event |
| comic36995 | Mu2000 door-open event + camera event |
| comic46015 | P1's Mu2000 door-open event in Battle Mode |
| comic46016 | P2's Mu2000 door-open event in Battle Mode |
| comic46017 | P2's Mu2000 door-close event |

<hr>

### Urban-Exclusive Event Scripts

Loaded unconditionally if there is a train with Urban selected.

| Number | Description |
| --- | --- |
| comic21000 | 1st RB26 event in Test Run Mode |
| comic21001 | TrackBomb event in Test Run Mode |
| comic21002 | 1st RB26 cooling event in Test Run Mode |
| comic21003 | 2nd RB26 event in Test Run Mode |
| comic21004 | 2nd RB26 cooling event in Test Run Mode |
| comic21005 | 3rd RB26 event in Test Run Mode |
| comic21006 | 1st RB26 event in Story Mode |
| comic21007 | 1st RB26 cooling event in Story Mode |
| comic21008 | 2nd RB26 event in Story Mode |
| comic21009 | 2nd RB26 cooling event in Story Mode |
| comic21010 | 3rd RB26 event in Story Mode |
| comic21011 | TrackBomb event in Story Mode |
| comic46030 | P1's 1st RB26 event in Battle Mode |
| comic46031 | P2's 1st RB26 event in Battle Mode |
| comic46032 | P1's 2nd RB26 event in Battle Mode |
| comic46033 | P2's 2nd RB26 event in Battle Mode |
| comic46034 | P1's 3rd RB26 event in Battle Mode |
| comic46035 | P2's 3rd RB26 event in Battle Mode |
| comic46036 | P1's 1st RB26 cooling event in Battle Mode |
| comic46037 | P2's 1st RB26 cooling event in Battle Mode |
| comic46038 | P1's 2nd RB26 cooling event in Battle Mode |
| comic46039 | P2's 2nd RB26 cooling event in Battle Mode |
| comic46040 | P1's TrackBomb event in Battle Mode |
| comic46041 | P2's TrackBomb event in Battle Mode |

<hr>

### Deki-Exclusive Event Scripts

Loaded unconditionally if there is a train with Deki selected.

| Number | Description |
| --- | --- |
| comic37000 | Rising Form event in Test Run Mode |
| comic37001 | Takumi version Rising Form event in Story Mode |
| comic37002 | Keisuke version Rising Form event in Story Mode |
| comic37005 | Peak Form event in Test Run Mode |
| comic37006 | Takumi version Peak Form event in Story Mode |
| comic37007 | Keisuke version Peak Form event in Story Mode |
| comic37010 | Peak Form end event in Test Run Mode |
| comic37011 | Takumi version Peak Form end event in Story Mode |
| comic37012 | Keisuke version Peak Form end event in Story Mode |
| comic37015 | Rising Form end event in Test Run Mode |
| comic37016 | Takumi version Rising Form end event in Story Mode |
| comic37017 | Keisuke version Rising Form end event in Story Mode |
| comic37020 | 2nd-and-later Peak Form event in Story/Test Run Mode |
| comic37021 | 2nd-and-later Peak Form end event in Story/Test Run Mode |
| comic37022 | 2nd-and-later Rising Form event in Story/Test Run Mode |
| comic37023 | 2nd-and-later Rising Form end event in Story/Test Run Mode |
| comic46060 | P1's Rising Form event in Battle Mode |
| comic46061 | P2's Rising Form event in Battle Mode |
| comic46062 | P1's Peak Form event in Battle Mode |
| comic46063 | P2's Peak Form event in Battle Mode |
| comic46064 | P1's Peak Form end event in Battle Mode |
| comic46065 | P2's Peak Form end event in Battle Mode |
| comic46066 | P1's Rising Form end event in Battle Mode |
| comic46067 | P2's Rising Form end event in Battle Mode |
| comic46068 | P1's 2nd-and-later Peak Form event in Battle Mode |
| comic46069 | P2's 2nd-and-later Peak Form event in Battle Mode |
| comic46070 | P1's 2nd-and-later Rising Form event in Battle Mode |
| comic46071 | P2's 2nd-and-later Rising Form event in Battle Mode |
| comic46072 | P1's 2nd-and-later Peak Form end event in Battle Mode |
| comic46073 | P2's 2nd-and-later Peak Form end event in Battle Mode |
| comic46074 | P1's 2nd-and-later Rising Form end event in Battle Mode |
| comic46075 | P2's 2nd-and-later Rising Form end event in Battle Mode |
