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


class EditStageTrainDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

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

        if decryptFile.game in ["CS", "RS"]:
            trainTrackNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["stageTrackName"], font=self.font2)
            trainTrackNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(trainTrackNameLabel, 0, 4)

        stageStartIdx = decryptFile.stageEditIdx
        self.trainNameList = copy.deepcopy(self.decryptFile.trainNameList)
        self.trainNameList.append(textSetting.textList["orgInfoEditor"]["noList"])
        self.trainComboList = []
        for i in range(decryptFile.stageCnt):
            info = decryptFile.stageList[stageStartIdx + i]
            # mainLayout - stageLabel
            stageLabel = QLabel(textSetting.textList["orgInfoEditor"]["stageNumLabel"].format(i + 1), font=self.font2)
            stageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(stageLabel, i + 1, 0)
            # mainLayout - train1pCombo
            train1pCombo = QComboBox(font=self.font2)
            train1pCombo.addItems(self.trainNameList)
            self.trainComboList.append(train1pCombo)
            mainLayout.addWidget(train1pCombo, i + 1, 1)
            if info[1] == -1:
                train1pCombo.setCurrentIndex(len(self.trainNameList) - 1)
            else:
                train1pCombo.setCurrentIndex(info[1])
            # mainLayout - train2pCombo
            train2pCombo = QComboBox(font=self.font2)
            train2pCombo.addItems(self.trainNameList)
            self.trainComboList.append(train2pCombo)
            mainLayout.addWidget(train2pCombo, i + 1, 2)
            if info[2] == -1:
                train2pCombo.setCurrentIndex(len(self.trainNameList) - 1)
            else:
                train2pCombo.setCurrentIndex(info[2])
            # mainLayout - train3pCombo
            train3pCombo = QComboBox(font=self.font2)
            train3pCombo.addItems(self.trainNameList)
            self.trainComboList.append(train3pCombo)
            mainLayout.addWidget(train3pCombo, i + 1, 3)
            if info[3] == -1:
                train3pCombo.setCurrentIndex(len(self.trainNameList) - 1)
            else:
                train3pCombo.setCurrentIndex(info[3])

            if decryptFile.game in ["CS", "RS"]:
                trainTrackComboList = textSetting.textList["orgInfoEditor"]["trackComboList"]
                trainTrackCombo = QComboBox(font=self.font2)
                trainTrackCombo.addItems(trainTrackComboList)
                trainTrackCombo.setCurrentIndex(info[4])
                self.trainComboList.append(trainTrackCombo)
                mainLayout.addWidget(trainTrackCombo, i + 1, 4)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I42"], icon="warning")
        if result == mb.OK:
            stageList = copy.deepcopy(self.decryptFile.stageList)

            infoCnt = 4
            if self.decryptFile.game == "BS":
                infoCnt = 3

            for i in range(self.decryptFile.stageCnt):
                train1pIndex = self.trainComboList[infoCnt * i].currentIndex()
                if train1pIndex == len(self.trainNameList) - 1:
                    train1pIndex = -1
                stageList[self.decryptFile.stageEditIdx + i][1] = train1pIndex

                train2pIndex = self.trainComboList[infoCnt * i + 1].currentIndex()
                if train2pIndex == len(self.trainNameList) - 1:
                    train2pIndex = -1
                stageList[self.decryptFile.stageEditIdx + i][2] = train2pIndex

                train3pIndex = self.trainComboList[infoCnt * i + 2].currentIndex()
                if train3pIndex == len(self.trainNameList) - 1:
                    train3pIndex = -1
                stageList[self.decryptFile.stageEditIdx + i][3] = train3pIndex

                if self.decryptFile.game in ["CS", "RS"]:
                    trainTrackIndex = self.trainComboList[infoCnt * i + 3].currentIndex()
                    stageList[self.decryptFile.stageEditIdx + i][4] = trainTrackIndex

            if not self.decryptFile.saveStageInfo(stageList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I43"])
