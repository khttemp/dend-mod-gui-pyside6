import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox,
    QComboBox, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()


class EditLsStageTrainDialog(QDialog):
    def __init__(self, parent, title, decryptFile, exeFilePath):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.stageCnt = 7
        self.exeFilePath = exeFilePath
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.trainNameList = copy.deepcopy(decryptFile.trainNameList)
        self.errorFlag = False

    def showDialog(self):
        if not self.getStageTrainInfo():
            self.errorFlag = True
            return QDialog.DialogCode.Rejected

        # layout
        layout = QVBoxLayout(self)
        # mainLayout
        mainLayout = QGridLayout()
        layout.addLayout(mainLayout)
        # mainLayout - train1pNameLabel
        train1pNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["stage1PLabel"], font=self.font2)
        train1pNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(train1pNameLabel, 0, 1)
        # mainLayout - train2pNameLabel
        train2pNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["stage2PLabel"], font=self.font2)
        train2pNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(train2pNameLabel, 0, 2)
        # mainLayout - train3pNameLabel
        train3pNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["stage3PLabel"], font=self.font2)
        train3pNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(train3pNameLabel, 0, 3)

        self.trainComboList = []

        for i in range(self.stageCnt):
            info = self.stageTrainNumList[i]
            # mainLayout - stageLabel
            stageLabel = QLabel(textSetting.textList["orgInfoEditor"]["lsStageLabelList"][i], font=self.font2)
            stageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(stageLabel, i + 1, 0)
            # mainLayout - train1pCombo
            train1pCombo = QComboBox(font=self.font2)
            train1pCombo.addItems(self.trainNameList)
            self.trainComboList.append(train1pCombo)
            mainLayout.addWidget(train1pCombo, i + 1, 1)
            train1pCombo.setCurrentIndex(info[0])
            # mainLayout - train2pCombo
            train2pCombo = QComboBox(font=self.font2)
            train2pCombo.addItems(self.trainNameList)
            self.trainComboList.append(train2pCombo)
            mainLayout.addWidget(train2pCombo, i + 1, 2)
            train2pCombo.setCurrentIndex(info[1])
            if info[2] != -1:
                # mainLayout - train3pCombo
                train3pCombo = QComboBox(font=self.font2)
                train3pCombo.addItems(self.trainNameList)
                self.trainComboList.append(train3pCombo)
                mainLayout.addWidget(train3pCombo, i + 1, 3)
                train3pCombo.setCurrentIndex(info[2])

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        return self.exec()

    def getStageTrainInfo(self):
        self.train1pAddress = [
            0x4FEB7,
            0x4FEDF,
            0x4FF15,
            0x4FF4B,
            0x4FF73,
            0x4FFA9,
            0x4FFDF
        ]
        self.train2pAddress = [
            0x4FEC5,
            0x4FEED,
            0x4FF23,
            0x4FF59,
            0x4FF81,
            0x4FFB7,
            0x4FFED
        ]
        self.train3pAddress = [
            -1,
            0x4FEFB,
            0x4FF31,
            -1,
            0x4FF8F,
            0x4FFC5,
            -1
        ]
        self.stageTrainNumList = []

        with open(self.exeFilePath, "rb") as f:
            byteArr = bytearray(f.read())

        for i in range(self.stageCnt):
            stageTrainNumInfo = []
            address = self.train1pAddress[i]
            train1pValue = byteArr[address]
            if train1pValue >= len(self.trainNameList):
                return False
            stageTrainNumInfo.append(train1pValue)

            address = self.train2pAddress[i]
            train2pValue = byteArr[address]
            if train2pValue >= len(self.trainNameList):
                return False
            stageTrainNumInfo.append(train2pValue)

            address = self.train3pAddress[i]
            if address != -1:
                train3pValue = byteArr[address]
                if train3pValue >= len(self.trainNameList):
                    return False
                stageTrainNumInfo.append(train3pValue)
            else:
                stageTrainNumInfo.append(address)
            self.stageTrainNumList.append(stageTrainNumInfo)
        return True

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I42"], icon="warning")
        if result == mb.OK:
            with open(self.exeFilePath, "rb") as f:
                byteArr = bytearray(f.read())

            try:
                trainComboCnt = 0
                for i in range(self.stageCnt):
                    address = self.train1pAddress[i]
                    train1pIndex = self.trainComboList[trainComboCnt].currentIndex()
                    byteArr[address] = train1pIndex
                    trainComboCnt += 1
                    
                    address = self.train2pAddress[i]
                    train2pIndex = self.trainComboList[trainComboCnt].currentIndex()
                    byteArr[address] = train2pIndex
                    trainComboCnt += 1

                    address = self.train3pAddress[i]
                    if address != -1:
                        train3pIndex = self.trainComboList[trainComboCnt].currentIndex()
                        byteArr[address] = train3pIndex
                        trainComboCnt += 1
                with open(self.exeFilePath, "wb") as w:
                    w.write(byteArr)
                return True
            except Exception:
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I43"])
