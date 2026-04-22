import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QDialogButtonBox, QComboBox,
    QCheckBox, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()


class SetDefaultEditDialog(QDialog):
    def __init__(self, parent, title, trainIndex, decryptFile, defaultData):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.font2 = QFont(textSetting.textList["font6"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - mainLayout
        mainLayout = QHBoxLayout()
        layout.addLayout(mainLayout)
        # layout - targetTrainListCombo
        self.targetTrainListCombo = QComboBox(font=self.font2)
        self.targetTrainListCombo.addItems(decryptFile.trainNameList)
        self.targetTrainListCombo.setCurrentIndex(-1)
        if decryptFile.game in ["SS"]:
            self.targetTrainListCombo.currentIndexChanged.connect(self.selectTrain)
        mainLayout.addWidget(self.targetTrainListCombo, alignment=Qt.AlignmentFlag.AlignTop)
        # layout - QVBoxLayout
        checkboxLayout = QVBoxLayout()
        mainLayout.addLayout(checkboxLayout)
        # layout - QVBoxLayout - notchCheckBox
        self.notchCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["notchLabel"], font=self.font2)
        checkboxLayout.addWidget(self.notchCheckBox)
        # layout - QVBoxLayout - perfCheckBox
        self.perfCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["perfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.perfCheckBox)
        if decryptFile.game in ["SS"]:
            self.addNewGameCheckBox(checkboxLayout)
        checkboxLayout.addStretch()

        defaultTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["setDefaultLabel"], font=self.font2)
        mainLayout.addWidget(defaultTextLabel, alignment=Qt.AlignmentFlag.AlignTop)

        self.targetTrainListCombo.setCurrentIndex(trainIndex)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def addNewGameCheckBox(self, checkboxLayout):
        # layout - QVBoxLayout - rainCheckBox
        self.rainCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["SSRainLfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.rainCheckBox)
        # layout - QVBoxLayout - carbCheckBox
        self.carbCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.carbCheckBox)
        # layout - QVBoxLayout - otherCheckBox
        self.otherCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.otherCheckBox)
        # layout - QVBoxLayout - hurikoCheckBox
        self.hurikoCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.hurikoCheckBox)
        # layout - QVBoxLayout - oneWheelCheckBox
        self.oneWheelCheckBox = QCheckBox(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"], font=self.font2)
        checkboxLayout.addWidget(self.oneWheelCheckBox)

    def selectTrain(self, index):
        # Mu2000, JR2000, H2300
        if self.targetTrainListCombo.currentIndex() in [12, 19, 25]:
            self.hurikoCheckBox.setText(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
        else:
            self.hurikoCheckBox.setText(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

        # K800, K80
        if self.targetTrainListCombo.currentIndex() in [27, 29]:
            self.oneWheelCheckBox.setText(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        else:
            self.oneWheelCheckBox.setText(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"] + textSetting.textList["orgInfoEditor"]["setDeleteLabel"])

    def validate(self):
        if self.decryptFile.game in ["RS", "CS", "BS", "LS"]:
            checkStatusList = [
                self.notchCheckBox.isChecked(),
                self.perfCheckBox.isChecked()
            ]
            ret = False
            for checkStatus in checkStatusList:
                ret |= checkStatus
            if not ret:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E62"])
                return False

            srcIdx = self.targetTrainListCombo.currentIndex()
            srcIndex = self.decryptFile.indexList[srcIdx]
            srcNotchNum = self.decryptFile.byteArr[srcIndex]
            distData = self.defaultData[srcIdx]
            distNotchNum = len(distData["notch"])

            srcSpeed = None
            srcPerf = None
            srcHuriko = None

            trainOrgInfo = self.decryptFile.trainInfoList[srcIdx]
            srcSpeed = trainOrgInfo[0]
            srcPerf = trainOrgInfo[1]
            if len(trainOrgInfo) > 2:
                srcHuriko = trainOrgInfo[2]
            srcList = [srcIndex, srcNotchNum, srcSpeed, srcPerf, srcHuriko]
        else:
            checkStatusList = [
                self.notchCheckBox.isChecked(),
                self.perfCheckBox.isChecked(),
                self.rainCheckBox.isChecked(),
                self.carbCheckBox.isChecked(),
                self.otherCheckBox.isChecked(),
                self.hurikoCheckBox.isChecked(),
                self.oneWheelCheckBox.isChecked(),
            ]
            ret = False
            for checkStatus in checkStatusList:
                ret |= checkStatus
            if not ret:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E62"])
                return False

            srcIdx = self.targetTrainListCombo.currentIndex()
            trainOrgInfo = self.decryptFile.trainInfoList[srcIdx]
            srcSpeed = trainOrgInfo[0]
            srcNotchNum = len(srcSpeed) // self.decryptFile.notchContentCnt

            distData = self.defaultData[srcIdx]
            distNotchNum = len(distData["notch"])

            srcList = [
                srcIdx,
                srcNotchNum,
            ]

        warnMsg = ""
        if self.notchCheckBox.isChecked():
            if srcNotchNum > distNotchNum:
                warnMsg += textSetting.textList["infoList"]["I45"].format(self.decryptFile.trainNameList[srcIdx], distNotchNum)
            elif srcNotchNum < distNotchNum:
                warnMsg += textSetting.textList["infoList"]["I45"].format(self.decryptFile.trainNameList[srcIdx], srcNotchNum)

        if self.notchCheckBox.isChecked():
            warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["notchLabel"])
        if self.perfCheckBox.isChecked():
            warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["perfLabel"])

        if self.decryptFile.game in ["SS"]:
            if self.rainCheckBox.isChecked():
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
            if self.carbCheckBox.isChecked():
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
            if self.otherCheckBox.isChecked():
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
            if self.hurikoCheckBox.isChecked():
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
            if self.oneWheelCheckBox.isChecked():
                warnMsg += "「{0}」".format(textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
        warnMsg += textSetting.textList["infoList"]["I46"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

        if result == mb.OK:
            if not self.decryptFile.setDefaultTrainInfo(srcList, distData, checkStatusList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I47"])
