*[日本語](MESH_READ_FILE.md)*

# Basic method

## 0. Terminology

[About frames and meshes](FRAME_MESH.md)

## 1. Prepare an FBX

Prepare the FBX file to swap in.

## 2. Prepare the file to be loaded by the old game

![title](image/tobu50k_0.png)

Here, we'll use "TOBU50K_0.SMF" as the example.

First, figure out specifically which mesh you want to rewrite.

![title](image/unityIn.png)

Here's a method for figuring it out using Unity.

Export the SMF as a different 3D file format (FBX is fine), load it into Unity,

and check which one is the outer model.

![title](image/unityMeshRenderer.png)

"Mesh Renderer" is displayed on the right,

![title](image/unityMeshRenderer2.png)

and unchecking it makes it invisible.

The frame that specifies this mesh is "In".

![title](image/meshIn.png)

In other words, mesh number 10 of "TOBU50K_0.SMF" is the target to swap.

![title](image/modelTest.png)

Here, since all mesh frames other than In are unneeded, we delete them.

You don't have to delete them, so handle this as needed.

## 3. When the loaded file is an SMF

![title](image/smfS300.png)

For example, when you load LS's Shinkansen model "S300_00.SMF",

![title](image/smfSearchMesh.png)

a list of mesh info obtained from the SMF appears.

Select whichever one is appropriate and swap it in.

## 4. When the loaded file is an FBX

![title](image/fbxModel.png)

For example, when you load SS's Tokyu 8500 series model "TQ8500Mdl00.fbx",

![title](image/fbxSearchMesh.png)

a list of mesh info obtained from the FBX appears.

Look at the mesh paths and select whichever one is appropriate to swap it in.

## 5. Load the SMF in MDLINFO

Once you're done editing the SMF, next comes handling it in MDLINFO.

Press the "Add model with SMF info" button

and load the corresponding SMF file.

![title](image/mdlinfo2.png)

Once loaded, it's added at the very bottom.

![title](image/mdlinfoMdlBin.png)

In MDLINFO, prepare an appropriate model binary to link with this model.

![title](image/mdlinfoDetail.png)

Modify the SMF's detailed elements (mesh-related) as needed.

## 6. Prepare the model binary file

If there's nothing in particular you need the model binary to do

(such as moving the wipers or rotating the rearmost model 180 degrees),

you can just copy and paste "HX200_1.bin".

For more on model binaries, see [【here】](/program/sub/mdlBin/README.md).

## 7. Load the model in the train performance settings

![title](image/trainData.png)

In the train performance train set info, swap in the model to be loaded.

## 8. Check in the game

![title](image/readS300.png)

The Shinkansen model loaded.

![title](image/readTQ8500.png)

SS's Tokyu 8500 series loaded.

<hr>

The reason it's glowing is due to

the "DIFF" or "EMIS" elements loaded in MDLINFO.

![title](image/readTQ8500_2.png)

Modifying these appropriately results in this. (Only part of it modified.)

## 9. If you want to add a mesh

![title](image/addFrame.png)

First, select an appropriate frame and copy-paste it.

Here, we copy-paste the "In" frame.

![title](image/addMesh.png)

Using the "Modify frame info" button,

enter an appropriate number in the meshNo field.

![title](image/addMesh2.png)

Entering a number larger than the current mesh count automatically appends it as the last mesh number.

However, a mesh added this way is an "empty mesh",

so be sure to swap it out for a mesh that actually has data.

## 10. If you only want to delete a mesh

![title](image/deleteMesh.png)

Enter -1 in the meshNo field.

This lets you delete only the mesh.

![title](image/deleteMesh2.png)

Only the remaining mesh numbers that shift are re-adjusted.

<br><br><br>

## What about the pantograph model?

![title](image/panta.png)

Since the pantograph doesn't need a model binary,

you can skip steps 5 and 6.

![title](image/panta2.png)

However, if left as-is, the position of the pantograph's "spark (arc)"

will be misaligned at this location,

so adjust it as needed.
