import os
import sys
import copy
import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QFileDialog, QDialog
)
from PySide6.QtGui import QFont

import program.sub.orgInfoEditor.orgInfoEditorProcess as orgInfoEditorProcess
from program.sub.orgInfoEditor.dendDecrypt import LSdecrypt as dendLs
from program.sub.orgInfoEditor.dendDecrypt import BSdecrypt as dendBs
from program.sub.orgInfoEditor.dendDecrypt import CSdecrypt as dendCs
from program.sub.orgInfoEditor.dendDecrypt import RSdecrypt as dendRs
from program.sub.orgInfoEditor.dendDecrypt import SSdecrypt as dendSs

from program.sub.orgInfoEditor.importPy.editStageTrainWidget import EditStageTrainDialog
from program.sub.orgInfoEditor.importPy.tabWidget import (
    tab1AllWidget, tab2AllWidget, tab3AllWidget
)

mb = customMessageBoxWidget.CustomMessageBox()


class OrgInfoEditorWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.defaultData = []
        self.allLoadFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        gameList = [
            "Shining Stage",
            "Rising Stage",
            "Climax Stage",
            "Burning Stage",
            "Lightning Stage",
        ]
        self.editStageTrainList = [
            "Rising Stage",
            "Climax Stage",
            "Burning Stage"
        ]
        self.oldGameList = ["RS", "CS", "BS", "LS"]

        mainLayout = QVBoxLayout(self)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 1)
        # space
        headerLayout.addSpacing(20)
        # gameCombo
        self.gameCombo = QComboBox(font=font2)
        self.gameCombo.setObjectName("gameCombo")
        self.gameCombo.addItems(gameList)
        self.gameCombo.setCurrentIndex(-1)
        self.gameCombo.currentIndexChanged.connect(self.selectGame)
        headerLayout.addWidget(self.gameCombo)
        # space
        headerLayout.addSpacing(30)
        # trainCombo
        self.trainCombo = QComboBox(font=font2)
        self.trainCombo.setObjectName("trainCombo")
        self.trainCombo.setFixedWidth(200)
        self.trainCombo.setEnabled(False)
        self.trainCombo.currentIndexChanged.connect(self.selectTrain)
        headerLayout.addWidget(self.trainCombo)
        # space
        headerLayout.addSpacing(30)
        # menuCombo
        self.menuCombo = QComboBox(font=font2)
        self.menuCombo.setObjectName("menuCombo")
        self.menuCombo.setFixedWidth(200)
        self.menuCombo.setEnabled(False)
        self.menuCombo.currentIndexChanged.connect(self.selectMenu)
        headerLayout.addWidget(self.menuCombo)
        # space
        headerLayout.addSpacing(30)
        self.editStageTrainButton = QPushButton(textSetting.textList["orgInfoEditor"]["editStageDefaultTrain"], font=font2)
        self.editStageTrainButton.setObjectName("editStageTrainButton")
        self.editStageTrainButton.setEnabled(False)
        self.editStageTrainButton.clicked.connect(self.editStageTrain)
        headerLayout.addWidget(self.editStageTrainButton)
        # stretch
        headerLayout.addStretch()

        # contentFrame
        contentFrame = QFrame()
        contentFrame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        mainLayout.addWidget(contentFrame, 14)
        # mainLayout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        contentFrame.setLayout(self.mainLayout)

        self.gameCombo.setCurrentIndex(0)

    def clearContent(self):
        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def selectGame(self, index):
        self.clearContent()
        self.allLoadFlag = False
        self.trainCombo.setEnabled(False)
        self.trainCombo.clear()

        self.menuCombo.setEnabled(False)
        self.menuCombo.clear()

        if self.gameCombo.currentText() in self.editStageTrainList:
            self.editStageTrainButton.show()
            self.editStageTrainButton.setEnabled(False)
        else:
            self.editStageTrainButton.hide()

    def selectTrain(self, index):
        if not self.allLoadFlag:
            return
        self.selectInfo(index, self.menuCombo.currentIndex())

    def selectMenu(self, index):
        if not self.allLoadFlag:
            return
        self.selectInfo(self.trainCombo.currentIndex(), index)

    def selectInfo(self, trainIndex, menuIndex):
        self.clearContent()

        if menuIndex == 0:
            tab1AllWidget(self.mainLayout, self.decryptFile, trainIndex, self.defaultData, self.reloadWidget)
        elif menuIndex == 1:
            tab2AllWidget(self.mainLayout, self.decryptFile, trainIndex, self.defaultData, self.reloadWidget)
        elif menuIndex == 2:
            tab3AllWidget(self.mainLayout, self.decryptFile, trainIndex, self.reloadWidget)

    def editStageTrain(self):
        editStageTrainDialog = EditStageTrainDialog(self, textSetting.textList["orgInfoEditor"]["editStageLabel"], self.decryptFile)
        if editStageTrainDialog.exec() == QDialog.Accepted:
            self.reloadWidget()

    def modifiedTrainNameList(self):
        copyTrainNameList = copy.deepcopy(self.decryptFile.trainNameList)
        for index, trainName in enumerate(copyTrainNameList):
            trainOrgInfo = self.decryptFile.trainInfoList[index]
            if trainOrgInfo is None:
                copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["dataCorrupted"]
                continue
            editFlag = False

            speedList = trainOrgInfo[0]
            notchCnt = len(speedList) // self.decryptFile.notchContentCnt
            defNotchCnt = len(self.defaultData[index]["notch"])
            if notchCnt != defNotchCnt:
                editFlag = True
            else:
                for i in range(len(speedList)):
                    speed = speedList[i]
                    if i >= 0 and i < notchCnt:
                        defSpeed = self.defaultData[index]["notch"][i]
                    elif i >= notchCnt and i < notchCnt*2:
                        defSpeed = self.defaultData[index]["tlk"][i - notchCnt]
                    elif i >= notchCnt*2 and i < notchCnt*3:
                        defSpeed = self.defaultData[index]["soundNum"][i - notchCnt*2]
                    elif i >= notchCnt*3 and i < notchCnt*4:
                        defSpeed = self.defaultData[index]["add"][i - notchCnt*3]
                    if speed != defSpeed:
                        editFlag = True
                        break

            perfList = trainOrgInfo[1]
            for i in range(len(perfList)):
                perf = perfList[i]
                defPerf = self.defaultData[index]["att"][i]
                if perf != defPerf:
                    editFlag = True
                    break

            if self.decryptFile.game in ["CS", "RS"]:
                hurikoList = trainOrgInfo[2]
                for i in range(len(hurikoList)):
                    huriko = hurikoList[i]
                    defHuriko = self.defaultData[index]["huriko"][i]
                    if huriko != defHuriko:
                        editFlag = True
                        break

            if self.decryptFile.game == "SS":
                rainList = trainOrgInfo[2]
                for i in range(len(rainList)):
                    rain = rainList[i]
                    defRain = self.defaultData[index]["rain"][i]
                    if rain != defRain:
                        editFlag = True
                        break

                carbList = trainOrgInfo[3]
                for i in range(len(carbList)):
                    carb = carbList[i]
                    defCarb = self.defaultData[index]["carb"][i]
                    if carb != defCarb:
                        editFlag = True
                        break

                otherList = trainOrgInfo[4]
                for i in range(len(otherList)):
                    other = otherList[i]
                    defOther = self.defaultData[index]["other"][i]
                    if other != defOther:
                        editFlag = True
                        break

                hurikoList = trainOrgInfo[5]
                if hurikoList is not None:
                    if self.defaultData[index]["huriko"] is not None:
                        for i in range(len(hurikoList)):
                            huriko = hurikoList[i]
                            defHuriko = self.defaultData[index]["huriko"][i]
                            if huriko != defHuriko:
                                editFlag = True
                                break
                    else:
                        editFlag = True
                else:
                    if self.defaultData[index]["huriko"] is not None:
                        editFlag = True

                oneWheelList = trainOrgInfo[6]
                if oneWheelList is not None:
                    if self.defaultData[index]["oneWheel"] is not None:
                        for i in range(len(oneWheelList)):
                            oneWheel = oneWheelList[i]
                            defOneWheel = self.defaultData[index]["oneWheel"][i]
                            if oneWheel != defOneWheel:
                                editFlag = True
                                break
                else:
                    if self.defaultData[index]["oneWheel"] is not None:
                        editFlag = True

            if editFlag:
                copyTrainNameList[index] = trainName + textSetting.textList["orgInfoEditor"]["modified"]

        return copyTrainNameList

    def initSelect(self):
        self.trainCombo.clear()
        self.trainCombo.addItems(self.modifiedTrainNameList())
        self.trainCombo.setEnabled(True)

        self.menuCombo.clear()
        if self.decryptFile.game in self.oldGameList:
            self.menuCombo.addItems(textSetting.textList["orgInfoEditor"]["menuComboValues"])
        else:
            self.menuCombo.addItems(textSetting.textList["orgInfoEditor"]["menuComboSSValues"])
        self.menuCombo.setEnabled(True)
        self.allLoadFlag = True
        self.selectInfo(self.trainCombo.currentIndex(), self.menuCombo.currentIndex())
        self.editStageTrainButton.setEnabled(True)

    def openFile(self):
        fileTypes = "{0} ({1})"
        if self.gameCombo.currentText() == "Shining Stage":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes.format(textSetting.textList["orgInfoEditor"]["fileType"], "train_org_data.den")
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendSs.SSdecrypt(file_path)
        elif self.gameCombo.currentText() == "Rising Stage":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes.format(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA4TH.BIN")
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendRs.RSdecrypt(file_path)
        elif self.gameCombo.currentText() == "Climax Stage":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes.format(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA3RD.BIN")
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendCs.CSdecrypt(file_path)
        elif self.gameCombo.currentText() == "Burning Stage":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes.format(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA2ND.BIN")
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendBs.BSdecrypt(file_path)
        elif self.gameCombo.currentText() == "Lightning Stage":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes.format(textSetting.textList["orgInfoEditor"]["fileType"], "TRAIN_DATA.BIN")
            )
            if not file_path:
                return
            del self.decryptFile
            self.decryptFile = dendLs.LSdecrypt(file_path)
        else:
            return

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
            return

        result, obj = orgInfoEditorProcess.readDefaultData(self.decryptFile.game)
        if not result:
            mb.showerror(title=textSetting.textList["error"], message=obj["message"])
            return

        self.allLoadFlag = False
        self.defaultData = obj["data"]
        self.initSelect()

    def reloadWidget(self):
        self.decryptFile = self.decryptFile.reload()
        trainIndex = self.trainCombo.currentIndex()
        self.allLoadFlag = False

        self.trainCombo.clear()
        self.trainCombo.addItems(self.modifiedTrainNameList())
        self.trainCombo.setCurrentIndex(-1)
        self.allLoadFlag = True
        self.trainCombo.setCurrentIndex(trainIndex)
