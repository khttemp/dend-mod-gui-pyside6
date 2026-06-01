import os
import shutil
import copy
import traceback

import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from program.sub.smf.dendDecrypt.decrypt import SmfDecrypt
import program.sub.smf.smfProcess as smfProcess
from program.sub.smf.importPy.importFbx import ImportFbxObject
from program.sub.smf.importPy.extractGlb import GlbObject
from program.sub.smf.importPy.extractFbx import FbxObject
from program.sub.smf.importPy.extractX import XObject

from PySide6.QtWidgets import (
    QApplication, QWidget, QProgressBar, QTreeWidget, QTreeWidgetItem,
    QLabel, QListWidget, QLineEdit, QFrame, QGroupBox,
    QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QDialog, QDialogButtonBox, QGridLayout, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()
errObj = ErrorLogObj()


class SmfWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.noTexList = []

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        buttonWidth = 200
        buttonHeight = 28

        mainLayout = QHBoxLayout(self)
        # leftLayout
        leftLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout, 1)
        # leftLayout - progressBar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        leftLayout.addWidget(self.progressBar)
        # leftLayout - groupBox
        treeGroupBox = QGroupBox(textSetting.textList["smf"]["scriptLabel"])
        leftLayout.addWidget(treeGroupBox)
        # leftLayout - groupBox - QVBoxLayout
        treeLayout = QVBoxLayout()
        treeLayout.setContentsMargins(0, 3, 0, 0)
        treeGroupBox.setLayout(treeLayout)
        # leftLayout - groupBox - QVBoxLayout - treeWidget
        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels([""])
        self.treeWidget.itemSelectionChanged.connect(self.onSelectionChanged)
        self.treeWidget.header().setDefaultAlignment(Qt.AlignCenter)
        self.treeWidget.header().setStretchLastSection(False)
        self.treeWidget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        treeLayout.addWidget(self.treeWidget)

        # rightLayout
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(20, 0, 20, 0)
        mainLayout.addLayout(rightLayout, 1)

        # allButtonLayout
        allButtonLayout = QVBoxLayout()
        rightLayout.addLayout(allButtonLayout)

        # buttonLayout1
        buttonLayout1 = QHBoxLayout()
        allButtonLayout.addLayout(buttonLayout1)
        # buttonLayout - copyAndPasteFrameButton
        self.copyAndPasteFrameButton = QPushButton(textSetting.textList["smf"]["copyAndPasteFrameLabel"])
        self.copyAndPasteFrameButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyAndPasteFrameButton.setEnabled(False)
        self.copyAndPasteFrameButton.clicked.connect(self.copyAndPasteFrameFunc)
        buttonLayout1.addWidget(self.copyAndPasteFrameButton)
        # stretch
        buttonLayout1.addStretch(1)
        # buttonLayout - deleteFrameButton
        self.deleteFrameButton = QPushButton(textSetting.textList["smf"]["deleteFrameLabel"])
        self.deleteFrameButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteFrameButton.setEnabled(False)
        self.deleteFrameButton.clicked.connect(self.deleteFrameFunc)
        buttonLayout1.addWidget(self.deleteFrameButton)

        # space
        allButtonLayout.addSpacing(5)

        # buttonLayout2
        buttonLayout2 = QHBoxLayout()
        allButtonLayout.addLayout(buttonLayout2)
        # buttonLayout2 - modifyFrameInfoButton
        self.modifyFrameInfoButton = QPushButton(textSetting.textList["smf"]["editInfoFrameLabel"])
        self.modifyFrameInfoButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifyFrameInfoButton.setEnabled(False)
        self.modifyFrameInfoButton.clicked.connect(self.modifyFrameInfoFunc)
        buttonLayout2.addWidget(self.modifyFrameInfoButton)
        # stretch
        buttonLayout2.addStretch(1)
        # buttonLayout - swapFrameButton
        self.swapFrameButton = QPushButton(textSetting.textList["smf"]["swapFrameLabel"])
        self.swapFrameButton.setFixedSize(buttonWidth, buttonHeight)
        self.swapFrameButton.setEnabled(False)
        self.swapFrameButton.clicked.connect(self.swapFrameFunc)
        buttonLayout2.addWidget(self.swapFrameButton)

        # space
        allButtonLayout.addSpacing(25)

        # buttonLayout3
        buttonLayout3 = QHBoxLayout()
        allButtonLayout.addLayout(buttonLayout3)
        # buttonLayout3 - turnModelMeshButton
        self.turnModelMeshButton = QPushButton(textSetting.textList["smf"]["turnModelMeshLabel"])
        self.turnModelMeshButton.setFixedSize(buttonWidth, buttonHeight)
        self.turnModelMeshButton.setEnabled(False)
        self.turnModelMeshButton.clicked.connect(self.turnModelMeshFunc)
        buttonLayout3.addWidget(self.turnModelMeshButton)
        # stretch
        buttonLayout3.addStretch(1)
        # buttonLayout3 - swapModelMeshButton
        self.swapModelMeshButton = QPushButton(textSetting.textList["smf"]["swapModelMeshLabel"])
        self.swapModelMeshButton.setFixedSize(buttonWidth, buttonHeight)
        self.swapModelMeshButton.setEnabled(False)
        self.swapModelMeshButton.clicked.connect(self.swapModelMeshFunc)
        buttonLayout3.addWidget(self.swapModelMeshButton)

        # space
        allButtonLayout.addSpacing(5)

        # buttonLayout4
        buttonLayout4 = QHBoxLayout()
        allButtonLayout.addLayout(buttonLayout4)
        # buttonLayout4 - meshMaterialCsvSaveButton
        self.meshMaterialCsvSaveButton = QPushButton(textSetting.textList["smf"]["meshMaterialCsvSaveLabel"])
        self.meshMaterialCsvSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.meshMaterialCsvSaveButton.setEnabled(False)
        self.meshMaterialCsvSaveButton.clicked.connect(self.meshMaterialCsvSaveFunc)
        buttonLayout4.addWidget(self.meshMaterialCsvSaveButton)
        # stretch
        buttonLayout4.addStretch(1)
        # buttonLayout4 - meshMaterialCsvLoadButton
        self.meshMaterialCsvLoadButton = QPushButton(textSetting.textList["smf"]["meshMaterialCsvLoadLabel"])
        self.meshMaterialCsvLoadButton.setFixedSize(buttonWidth, buttonHeight)
        self.meshMaterialCsvLoadButton.setEnabled(False)
        self.meshMaterialCsvLoadButton.clicked.connect(self.meshMaterialCsvLoadFunc)
        buttonLayout4.addWidget(self.meshMaterialCsvLoadButton)

        # space
        allButtonLayout.addSpacing(25)

        # buttonLayout5
        buttonLayout5 = QHBoxLayout()
        allButtonLayout.addLayout(buttonLayout5)
        # buttonLayout5 - standardButton
        self.standardButton = QPushButton(textSetting.textList["smf"]["createStandardLabel"])
        self.standardButton.setFixedSize(buttonWidth, buttonHeight)
        self.standardButton.setEnabled(False)
        self.standardButton.clicked.connect(self.createStandardGaugeFunc)
        buttonLayout5.addWidget(self.standardButton)
        # stretch
        buttonLayout5.addStretch(1)
        # buttonLayout5 - extract3dObjButton
        self.extract3dObjButton = QPushButton(textSetting.textList["smf"]["extract3dLabel"])
        self.extract3dObjButton.setFixedSize(buttonWidth, buttonHeight)
        self.extract3dObjButton.setEnabled(False)
        self.extract3dObjButton.clicked.connect(self.extract3dFunc)
        buttonLayout5.addWidget(self.extract3dObjButton)

        # frameTransformLayout
        frameTransformLayout = QVBoxLayout()
        rightLayout.addLayout(frameTransformLayout)
        # framePositionGroupBox
        framePositionGroupBox = QGroupBox(textSetting.textList["smf"]["framePosInfoLabel"])
        frameTransformLayout.addWidget(framePositionGroupBox)
        # leftLayout - groupBox - QHBoxLayout
        framePositionLayout = QHBoxLayout()
        framePositionGroupBox.setLayout(framePositionLayout)
        # leftLayout - groupBox - QHBoxLayout - framePosXLabel
        self.framePosXLabel = QLabel("0.0", font=font2)
        self.framePosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.framePosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        framePositionLayout.addWidget(self.framePosXLabel)
        # leftLayout - groupBox - QHBoxLayout - framePosYLabel
        self.framePosYLabel = QLabel("0.0", font=font2)
        self.framePosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.framePosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        framePositionLayout.addWidget(self.framePosYLabel)
        # leftLayout - groupBox - QHBoxLayout - framePosZLabel
        self.framePosZLabel = QLabel("0.0", font=font2)
        self.framePosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.framePosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        framePositionLayout.addWidget(self.framePosZLabel)

        # frameRotationGroupBox
        frameRotationGroupBox = QGroupBox(textSetting.textList["smf"]["frameRotInfoLabel"])
        frameTransformLayout.addWidget(frameRotationGroupBox)
        # leftLayout - groupBox - QHBoxLayout
        frameRotationLayout = QHBoxLayout()
        frameRotationGroupBox.setLayout(frameRotationLayout)
        # leftLayout - groupBox - QHBoxLayout - frameRotXLabel
        self.frameRotXLabel = QLabel("0.0", font=font2)
        self.frameRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.frameRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frameRotationLayout.addWidget(self.frameRotXLabel)
        # leftLayout - groupBox - QHBoxLayout - frameRotYLabel
        self.frameRotYLabel = QLabel("0.0", font=font2)
        self.frameRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.frameRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frameRotationLayout.addWidget(self.frameRotYLabel)
        # leftLayout - groupBox - QHBoxLayout - frameRotZLabel
        self.frameRotZLabel = QLabel("0.0", font=font2)
        self.frameRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.frameRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frameRotationLayout.addWidget(self.frameRotZLabel)

        # space
        rightLayout.addSpacing(5)
        # horizentalLine
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        rightLayout.addWidget(horizentalLine)
        # space
        rightLayout.addSpacing(5)

        scanImageLayout = QVBoxLayout()
        rightLayout.addLayout(scanImageLayout)

        # scanImageLayout - scanSmfImageButton
        self.scanSmfImageButton = QPushButton(textSetting.textList["smf"]["scanSmfImageLabel"])
        self.scanSmfImageButton.clicked.connect(self.scanSmfImageFunc)
        scanImageLayout.addWidget(self.scanSmfImageButton)
        # space
        scanImageLayout.addSpacing(15)
        # scanImageLayout - countLabel
        self.countLabel = QLabel("")
        self.countLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.countLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scanImageLayout.addWidget(self.countLabel)

        # scanImageLayout - QListWidget
        self.scanImageListWidget = QListWidget(font=font2)
        scanImageLayout.addWidget(self.scanImageListWidget)

        # scanImageLayout - scanModelPathLabel
        self.scanModelPathLabel = QLabel("")
        self.scanModelPathLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.scanModelPathLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scanImageLayout.addWidget(self.scanModelPathLabel)
        # scanImageLayout - copyImageButton
        self.copyImageButton = QPushButton(textSetting.textList["smf"]["copyImageLabel"])
        self.copyImageButton.clicked.connect(self.copyImageFunc)
        self.copyImageButton.setEnabled(False)
        scanImageLayout.addWidget(self.copyImageButton)

        # space
        scanImageLayout.addSpacing(15)

    def progressBarUpdate(self, value, flag=False):
        if flag:
            self.progressBar.setValue(round(self.progressBar.value() + value))
        else:
            self.progressBar.setValue(int(value))

    def deleteWidget(self):
        self.treeWidget.clear()

        self.copyAndPasteFrameButton.setEnabled(False)
        self.deleteFrameButton.setEnabled(False)
        self.modifyFrameInfoButton.setEnabled(False)
        self.swapFrameButton.setEnabled(False)
        self.turnModelMeshButton.setEnabled(False)
        self.swapModelMeshButton.setEnabled(False)
        self.meshMaterialCsvSaveButton.setEnabled(False)
        self.meshMaterialCsvLoadButton.setEnabled(False)

        self.framePosXLabel.setText("{0}".format(float(0)))
        self.framePosYLabel.setText("{0}".format(float(0)))
        self.framePosZLabel.setText("{0}".format(float(0)))
        self.frameRotXLabel.setText("{0}".format(float(0)))
        self.frameRotYLabel.setText("{0}".format(float(0)))
        self.frameRotZLabel.setText("{0}".format(float(0)))

    def createWidget(self):
        self.createTreeWidget()

        self.standardButton.setEnabled(True)
        self.extract3dObjButton.setEnabled(True)

    def createTreeWidget(self):
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["{0}".format(self.decryptFile.filename)])

        itemDict = {}
        for frameNo, frameObj in enumerate(self.decryptFile.frameList):
            fName = frameObj["name"]
            meshNo = frameObj["meshNo"]
            name = fName
            if meshNo != -1:
                name = fName + textSetting.textList["smf"]["treeMeshNumFormat"].format(meshNo)
            item = QTreeWidgetItem()
            item.setData(0, Qt.UserRole, frameObj)
            item.setText(0, name)
            itemDict[frameNo] = item

        for frameNo, frameObj in enumerate(self.decryptFile.frameList):
            parentFrameNo = frameObj["parentFrameNo"]
            item = itemDict[frameNo]
            if parentFrameNo == -1:
                self.treeWidget.addTopLevelItem(item)
            else:
                itemDict[parentFrameNo].addChild(item)
        self.treeWidget.expandAll()

    def onSelectionChanged(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        matrix = frameObj["matrix"]
        pos = self.decryptFile.matrixToPosInfo(matrix)
        self.framePosXLabel.setText("{0}".format(round(pos[0], 5)))
        self.framePosYLabel.setText("{0}".format(round(pos[1], 5)))
        self.framePosZLabel.setText("{0}".format(round(pos[2], 5)))
        q = self.decryptFile.matrixToEulerAngleInfo(matrix)
        self.frameRotXLabel.setText("{0}".format(round(q[0], 5)))
        self.frameRotYLabel.setText("{0}".format(round(q[1], 5)))
        self.frameRotZLabel.setText("{0}".format(round(q[2], 5)))

        parentFrameNo = frameObj["parentFrameNo"]
        if parentFrameNo != -1:
            self.copyAndPasteFrameButton.setEnabled(True)
            self.deleteFrameButton.setEnabled(True)
            self.modifyFrameInfoButton.setEnabled(True)
            self.swapFrameButton.setEnabled(True)
        else:
            self.copyAndPasteFrameButton.setEnabled(False)
            self.deleteFrameButton.setEnabled(False)
            self.modifyFrameInfoButton.setEnabled(False)
            self.swapFrameButton.setEnabled(False)

        meshNo = frameObj["meshNo"]
        if meshNo != -1:
            self.turnModelMeshButton.setEnabled(True)
            self.swapModelMeshButton.setEnabled(True)
            self.meshMaterialCsvSaveButton.setEnabled(True)
            self.meshMaterialCsvLoadButton.setEnabled(True)
        else:
            self.turnModelMeshButton.setEnabled(False)
            self.swapModelMeshButton.setEnabled(False)
            self.meshMaterialCsvSaveButton.setEnabled(False)
            self.meshMaterialCsvLoadButton.setEnabled(False)

    def openFile(self):
        fileType = "{0} ({1})".format(textSetting.textList["smf"]["fileType"], "*.SMF")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )
        if not file_path:
            return

        flagList = smfProcess.getSmfFlagOption(self.importDict["configPath"])
        self.decryptFile = SmfDecrypt(file_path, flagList, self.progressBarUpdate)
        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return
        self.deleteWidget()
        self.createWidget()

    def reloadWidget(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            if not self.decryptFile.open():
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
                return
            self.deleteWidget()
            self.createWidget()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])

    def copyAndPasteFrameFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        frameName = frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I127"].format(frameName)
        frameIdx = frameObj["frameNo"]
        parentIdx = frameObj["parentFrameNo"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.addFrame(frameIdx, parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def deleteFrameFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        frameName = frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I109"].format(frameName)
        frameIdx = frameObj["frameNo"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.deleteFrame(frameIdx, -1):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def modifyFrameInfoFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        editFrameInfoDialog = EditFrameInfoDialog(self, textSetting.textList["smf"]["editInfoFrame"], frameObj, self.decryptFile)
        if editFrameInfoDialog.exec() == QDialog.Accepted:
            frameIdx = frameObj["frameNo"]
            if not self.decryptFile.updateFrameInfo(frameIdx, editFrameInfoDialog.resultValueList, editFrameInfoDialog.meshDeleteFlag):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I131"])
            self.reloadWidget()

    def swapFrameFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        swapFrameDialog = SwapFrameDialog(self, textSetting.textList["smf"]["swapFrame"], frameObj, self.decryptFile)
        if swapFrameDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveSwap(swapFrameDialog.frameIdx, swapFrameDialog.parentIdx):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
            self.reloadWidget()

    def turnModelMeshFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        meshNo = frameObj["meshNo"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I124"], icon="warning")
        if result == mb.OK:
            if not self.decryptFile.turnModelMesh(meshNo):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I125"])
            self.reloadWidget()

    def swapModelMeshFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        meshNo = frameObj["meshNo"]

        fileType = "{0} ({1});;{2} ({3})".format(
            textSetting.textList["smf"]["fileType"],
            "*.SMF",
            textSetting.textList["smf"]["fbxFile"],
            "*.fbx"
        )
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )
        if not file_path:
            return

        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".smf":
            swapDecryptFile = SmfDecrypt(file_path)
            if not swapDecryptFile.open():
                swapDecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return

            swapMeshDialog = SwapMeshDialog(self, textSetting.textList["smf"]["swapFrame"], swapDecryptFile)
            if swapMeshDialog.exec() == QDialog.Accepted:
                processResult, obj = smfProcess.getSwapMeshByteArr(swapMeshDialog.swapMeshNo, swapDecryptFile)
                if not processResult:
                    mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                    return

                if not self.decryptFile.saveSwapMesh(meshNo, obj["data"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
                self.reloadWidget()
        elif ext == ".fbx":
            swapFbxMeshDialog = SwapFbxMeshDialog(self, textSetting.textList["smf"]["swapMesh"], file_path)
            if swapFbxMeshDialog.exec() == QDialog.Accepted:
                result, obj = swapFbxMeshDialog.importFbxObj.makeMeshObj(swapFbxMeshDialog.swapMeshNode)
                swapFbxMeshDialog.importFbxObj.destroyFbxObj()
                if not result:
                    mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                    return

                if not self.decryptFile.saveSwapFbxMesh(meshNo, obj["data"], obj["flag"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I104"])
                self.reloadWidget()

    def meshMaterialCsvSaveFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        meshNo = frameObj["meshNo"]
        saveName = os.path.splitext(os.path.basename(self.decryptFile.filename))[0]
        saveName += "_mesh{0}".format(meshNo)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            saveName,
            "{0} ({1})".format(textSetting.textList["smf"]["csvFile"], "*.csv")
        )
        if not file_path:
            return

        try:
            mtrlList = self.decryptFile.meshList[meshNo]["mtrlList"]
            smfProcess.writeMaterialCsv(file_path, mtrlList)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])

    def meshMaterialCsvLoadFunc(self):
        selectedItems = self.treeWidget.selectedItems()
        if not selectedItems:
            return

        item = selectedItems[0]
        frameObj = item.data(0, Qt.UserRole)
        meshNo = frameObj["meshNo"]

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            "{0} ({1})".format(textSetting.textList["smf"]["csvFile"], "*.csv")
        )
        if not file_path:
            return

        try:
            originMtrlList = self.decryptFile.meshList[meshNo]["mtrlList"]
            processResult, obj = smfProcess.loadCsvData(file_path, originMtrlList)
            if not processResult:
                mb.showerror(title=textSetting.textList["error"], message=obj["message"])
                return

            warnMsg = textSetting.textList["infoList"]["I136"]
            if obj["noTexcInputFlag"]:
                warnMsg = textSetting.textList["infoList"]["I138"] + warnMsg
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result == mb.OK:
                if not self.decryptFile.modifyMaterial(meshNo, obj["data"]):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I137"])
                self.reloadWidget()
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def createStandardGaugeFunc(self):
        if not self.decryptFile.detectGauge():
            msg = textSetting.textList["infoList"]["I105"]
            for model in self.decryptFile.standardGuageList:
                msg += "\n" + model
            mb.showerror(title=textSetting.textList["error"], message=msg)
            return

        modelIndex = self.decryptFile.standardGuageList.index(self.decryptFile.filename)
        if self.decryptFile.detectMuTrack():
            if not self.decryptFile.createStandardGauge(None):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        else:
            modelName = self.decryptFile.d4NarrowGuageList[modelIndex]
            msg = textSetting.textList["infoList"]["I106"].format(modelName)
            mb.showinfo(title=textSetting.textList["smf"]["smfFile"], message=msg)

            fileType = "{0} ({1})".format(textSetting.textList["smf"]["fileType"], "*.SMF")
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileType
            )
            if not file_path:
                return

            filename = os.path.basename(file_path)
            if filename.upper() != modelName:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I107"])
                return

            d4DecryptFile = SmfDecrypt(file_path)
            if not d4DecryptFile.open():
                d4DecryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E74"])
                return

            if not self.decryptFile.createStandardGauge(d4DecryptFile):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I108"])
        self.reloadWidget()

    def extract3dFunc(self):
        saveName = os.path.splitext(os.path.basename(self.decryptFile.filename))[0]
        fileTypeList = [
            (textSetting.textList["smf"]["fbxFile"], "*.fbx"),
            (textSetting.textList["smf"]["glbFile"], "*.glb"),
            (textSetting.textList["smf"]["xFile"], "*.x")
        ]
        fileTypes = ";;".join(["{0} ({1})".format(x[0], x[1]) for x in fileTypeList])
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            saveName,
            fileTypes
        )

        if not file_path:
            return

        ext = os.path.splitext(os.path.basename(file_path))[1].lower()
        if ext == ".fbx":
            fbxObj = FbxObject(file_path, self.decryptFile)
            if not fbxObj.makeFbxFile():
                fbxObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I123"])
        elif ext == ".glb":
            glbObj = GlbObject(file_path, self.decryptFile, self.importDict["configPath"])
            if not glbObj.makeGlbFile():
                glbObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I121"])
        elif ext == ".x":
            xObj = XObject(file_path, self.decryptFile)
            if not xObj.makeXFile():
                xObj.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I122"])

    def scanSmfImageFunc(self):
        fileType = "{0} ({1})".format(textSetting.textList["smf"]["fileListType"], "*.SMF")
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "",
            "",
            fileType
        )


        if not file_paths:
            return
        
        dirPath = os.path.dirname(file_paths[0])
        self.scanModelPathLabel.setText("{0}".format(dirPath))
        modelCountFormat = "{0}/{1}"
        allTexSet = set()

        for idx, file in enumerate(file_paths):
            self.countLabel.setText(modelCountFormat.format(idx + 1, len(file_paths)))
            QApplication.processEvents()

            decryptScanFile = SmfDecrypt(file)
            if not decryptScanFile.open():
                decryptScanFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
                return
            allTexSet |= decryptScanFile.texList
        allTexList = list(allTexSet)
        self.noTexList = []

        self.scanImageListWidget.clear()
        for tex in allTexList:
            if not os.path.exists(os.path.join(dirPath, tex)):
                self.noTexList.append(tex)
                self.scanImageListWidget.addItem("「{0}」がありません".format(tex))

        if len(self.noTexList) > 0:
            self.copyImageButton.setEnabled(True)
        else:
            self.copyImageButton.setEnabled(False)

    def copyImageFunc(self):
        scanModelPath = self.scanModelPathLabel.text()
        folderPath = QFileDialog.getExistingDirectory(
            self,
            "",
            scanModelPath
        )

        if not folderPath:
            return

        newNoTexList = []
        self.scanImageListWidget.clear()
        QApplication.processEvents()

        modelCountFormat = "{0}/{1}"
        for idx, tex in enumerate(self.noTexList):
            self.countLabel.setText(modelCountFormat.format(idx + 1, len(self.noTexList)))
            imagePath = os.path.join(folderPath, tex)
            if os.path.exists(imagePath):
                shutil.copy(imagePath, scanModelPath)
                self.scanImageListWidget.addItem("{0}をコピーしました".format(tex))
            else:
                newNoTexList.append(tex)
                self.scanImageListWidget.insertItem(0, "「{0}」が存在しません".format(tex))
            QApplication.processEvents()
        self.noTexList = copy.deepcopy(newNoTexList)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I118"])

        if len(self.noTexList) > 0:
            self.copyImageButton.setEnabled(True)
        else:
            self.copyImageButton.setEnabled(False)


class EditFrameInfoDialog(QDialog):
    def __init__(self, parent, title, frameObj, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.frameObj = frameObj
        self.decryptFile = decryptFile
        self.resultValueList = []
        self.meshDeleteFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        frameInfoGridLayout = QGridLayout()
        layout.addLayout(frameInfoGridLayout)
        self.lineEditList = []

        # layout - QGridLayout - label
        frameNameLabel = QLabel("Name", font=font2)
        frameInfoGridLayout.addWidget(frameNameLabel, 0, 0)
        # layout - QGridLayout - lineEdit
        frameNameLineEdit = QLineEdit(font=font2)
        frameNameLineEdit.setText("{0}".format(self.frameObj["name"]))
        self.lineEditList.append(frameNameLineEdit)
        frameInfoGridLayout.addWidget(frameNameLineEdit, 0, 1)

        posLabelList = ["pos_x", "pos_y", "pos_z"]
        posInfoList = self.decryptFile.matrixToPosInfo(self.frameObj["matrix"])
        for i, posLabel in enumerate(posLabelList):
            # layout - QGridLayout - label
            posNameLabel = QLabel(posLabel, font=font2)
            frameInfoGridLayout.addWidget(posNameLabel, 1 + i, 0)
            # layout - QGridLayout - lineEdit
            posInfoLineEdit = QLineEdit(font=font2)
            posInfoLineEdit.setValidator(numberValidator)
            posInfoLineEdit.setText("{0}".format(round(posInfoList[i], 5)))
            self.lineEditList.append(posInfoLineEdit)
            frameInfoGridLayout.addWidget(posInfoLineEdit, 1 + i, 1)

        rotLabelList = ["rot_x", "rot_y", "rot_z"]
        rotInfoList = self.decryptFile.matrixToEulerAngleInfo(self.frameObj["matrix"])
        for i, rotLabel in enumerate(rotLabelList):
            # layout - QGridLayout - label
            rotNameLabel = QLabel(rotLabel, font=font2)
            frameInfoGridLayout.addWidget(rotNameLabel, 4 + i, 0)
            # layout - QGridLayout - lineEdit
            rotInfoLineEdit = QLineEdit(font=font2)
            rotInfoLineEdit.setValidator(numberValidator)
            rotInfoLineEdit.setText("{0}".format(round(rotInfoList[i], 5)))
            self.lineEditList.append(rotInfoLineEdit)
            frameInfoGridLayout.addWidget(rotInfoLineEdit, 4 + i, 1)

        # layout - QGridLayout - label
        meshNoNameLabel = QLabel("meshNo", font=font2)
        frameInfoGridLayout.addWidget(meshNoNameLabel, 7, 0)
        # layout - QGridLayout - lineEdit
        meshNoLineEdit = QLineEdit(font=font2)
        meshNoLineEdit.setValidator(integerValidator)
        meshNoLineEdit.setText("{0}".format(self.frameObj["meshNo"]))
        self.lineEditList.append(meshNoLineEdit)
        frameInfoGridLayout.addWidget(meshNoLineEdit, 7, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.meshDeleteFlag = False
        warnMsg = ""
        inputMeshNo = int(self.lineEditList[-1].text())
        if inputMeshNo < -1:
            inputMeshNo = -1
        originMeshNo = self.frameObj["meshNo"]

        if inputMeshNo == -1:
            if originMeshNo != -1:
                self.meshDeleteFlag = True
                warnMsg = textSetting.textList["infoList"]["I133"].format(originMeshNo) + textSetting.textList["infoList"]["I130"]
        else:
            if originMeshNo == -1:
                inputMeshNo = self.decryptFile.meshCount
                warnMsg = textSetting.textList["infoList"]["I134"].format(inputMeshNo) + textSetting.textList["infoList"]["I130"]
            else:
                if originMeshNo != inputMeshNo:
                    if inputMeshNo < self.decryptFile.meshCount:
                        warnMsg = textSetting.textList["infoList"]["I132"].format(inputMeshNo) + textSetting.textList["infoList"]["I130"]
                    else:
                        warnMsg = textSetting.textList["infoList"]["I135"].format(originMeshNo, inputMeshNo) + textSetting.textList["infoList"]["I130"]

        if warnMsg:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result != mb.OK:
                return

        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            if i == 0:
                if not lineEdit.text():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E138"])
                    return False

            if i == 0:
                self.resultValueList.append(lineEdit.text())
            elif i == 7:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                self.resultValueList.append(float(lineEdit.text()))
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class SwapFrameDialog(QDialog):
    def __init__(self, parent, title, frameObj, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.frameObj = frameObj
        self.decryptFile = decryptFile
        self.swapFrameList = []
        swapFrameComboList = []
        self.frameIdx = -1
        self.parentIdx = -1

        for index, fObj in enumerate(self.decryptFile.frameList):
            if index == self.frameObj["frameNo"]:
                continue
            self.swapFrameList.append([index, fObj["name"]])
            swapFrameComboList.append("%02d(%s)" % (index, fObj["name"]))

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        swapLabel = QLabel(textSetting.textList["smf"]["locationParentFrame"], font=font2)
        layout.addWidget(swapLabel)
        # layout - Combobox
        self.combobox = QComboBox(font=font2)
        self.combobox.addItems(swapFrameComboList)
        layout.addWidget(self.combobox)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        swapCbIdx = self.combobox.currentIndex()
        self.parentIdx = self.swapFrameList[swapCbIdx][0]
        parentName = self.swapFrameList[swapCbIdx][1]
        self.frameIdx = self.frameObj["frameNo"]
        frameName = self.frameObj["name"]
        warnMsg = textSetting.textList["infoList"]["I103"].format(frameName, parentName) + textSetting.textList["infoList"]["I102"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result == mb.OK:
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()


class SwapMeshDialog(QDialog):
    def __init__(self, parent, title, swapDecryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.swapMeshNo = -1
        self.swapMeshNoList = []
        swapMeshComboList = []

        for fObj in swapDecryptFile.frameList:
            if fObj["meshNo"] != -1:
                self.swapMeshNoList.append(fObj["meshNo"])
                swapMeshComboList.append("%s (Mesh No.%d)" % (fObj["name"], fObj["meshNo"]))

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        swapLabel = QLabel(textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=font2)
        layout.addWidget(swapLabel)
        # layout - Combobox
        self.combobox = QComboBox(font=font2)
        self.combobox.addItems(swapMeshComboList)
        layout.addWidget(self.combobox)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        swapCbIdx = self.combobox.currentIndex()
        self.swapMeshNo = self.swapMeshNoList[swapCbIdx]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I126"], icon="warning")
        if result == mb.OK:
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()


class SwapFbxMeshDialog(QDialog):
    def __init__(self, parent, title, fbxFilePath):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.importFbxObj = ImportFbxObject(fbxFilePath)
        self.swapMeshNameList = self.importFbxObj.meshNameList
        self.swapMeshNodeList = self.importFbxObj.meshNodeList
        self.swapMeshPathList = self.importFbxObj.meshPathList
        self.swapMeshNode = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        swapLabel = QLabel(textSetting.textList["smf"]["swapToModelMeshNoLabel"], font=font2)
        layout.addWidget(swapLabel)
        # layout - Combobox
        self.combobox = QComboBox(font=font2)
        self.combobox.addItems(self.swapMeshNameList)
        self.combobox.setCurrentIndex(-1)
        self.combobox.currentIndexChanged.connect(self.showPath)
        layout.addWidget(self.combobox)
        # layout - meshPathLineEdit
        self.pathLineEdit = QLineEdit("")
        self.pathLineEdit.setReadOnly(True)
        layout.addWidget(self.pathLineEdit)

        self.combobox.setCurrentIndex(0)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def showPath(self):
        idx = self.combobox.currentIndex()
        self.pathLineEdit.setText("{0}".format(self.swapMeshPathList[idx]))

    def validate(self):
        swapCbIdx = self.combobox.currentIndex()
        self.swapMeshNode = self.swapMeshNodeList[swapCbIdx]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I126"], icon="warning")
        if result == mb.OK:
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
