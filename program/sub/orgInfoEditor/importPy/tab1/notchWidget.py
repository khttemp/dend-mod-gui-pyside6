from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel,
    QPushButton, QDialog, QLineEdit, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QPalette, QColor, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class NotchWidget(QWidget):
    def __init__(self, notchIndex, decryptFile, notchCnt, speed, defaultData):
        super().__init__()
        self.notchIndex = notchIndex
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        rowSpanNum = self.notchContentCnt
        # notchLabel
        notchText = textSetting.textList["orgInfoEditor"]["notchLabel"] + str(notchIndex + 1)
        notchLabel = QLabel(notchText, font=font6)
        notchLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        notchLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(notchLabel, 0, 0, rowSpanNum, 1)

        self.speedValue = speed[notchIndex]
        if notchIndex >= len(defaultData["notch"]):
            speedDefaultValue = None
        else:
            speedDefaultValue = defaultData["notch"][notchIndex]
        # speedNameLabel
        self.speedNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchSpeed"], font=font6)
        self.speedNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.speedNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.speedNameLabel, 0, 1)
        # speedLabel
        self.speedLabel = QLabel("{0}".format(self.speedValue), font=font6)
        self.speedLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.speedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.speedLabel, 0, 2)
        # editSpeedButton
        editSpeedButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editSpeedButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        editSpeedButton.clicked.connect(partial(self.editSpeedVar, speedDefaultValue, numberValidator))
        mainLayout.addWidget(editSpeedButton, 0, 3)
        self.setLabelColor(self.speedNameLabel, self.speedLabel, self.speedValue, speedDefaultValue)

        self.tlkValue = speed[notchCnt + notchIndex]
        if notchIndex >= len(defaultData["tlk"]):
            tlkDefaultValue = None
        else:
            tlkDefaultValue = defaultData["tlk"][notchIndex]
        # tlkNameLabel
        self.tlkNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchTlk"], font=font6)
        self.tlkNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.tlkNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.tlkNameLabel, 1, 1)
        # tlkLabel
        self.tlkLabel = QLabel("{0}".format(self.tlkValue), font=font6)
        self.tlkLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.tlkLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.tlkLabel, 1, 2)
        # editTlkButton
        editTlkButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editTlkButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        editTlkButton.clicked.connect(partial(self.editTlkVar, tlkDefaultValue, numberValidator))
        mainLayout.addWidget(editTlkButton, 1, 3)
        self.setLabelColor(self.tlkNameLabel, self.tlkLabel, self.tlkValue, tlkDefaultValue)

        if self.notchContentCnt > 2:
            self.soundValue = speed[notchCnt*2 + notchIndex]
            if notchIndex >= len(defaultData["soundNum"]):
                soundDefaultValue = None
            else:
                soundDefaultValue = defaultData["soundNum"][notchIndex]
            # soundNameLabel
            self.soundNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchSound"], font=font6)
            self.soundNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.soundNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(self.soundNameLabel, 2, 1)
            # soundLabel
            self.soundLabel = QLabel("{0}".format(self.soundValue), font=font6)
            self.soundLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.soundLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(self.soundLabel, 2, 2)
            # editSoundButton
            editSoundButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            editSoundButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            editSoundButton.clicked.connect(partial(self.editSoundVar, soundDefaultValue, integerValidator))
            mainLayout.addWidget(editSoundButton, 2, 3)
            self.setLabelColor(self.soundNameLabel, self.soundLabel, self.soundValue, soundDefaultValue)

            self.addValue = speed[notchCnt*3 + notchIndex]
            if notchIndex >= len(defaultData["add"]):
                addDefaultValue = None
            else:
                addDefaultValue = defaultData["add"][notchIndex]
            # addNameLabel
            self.addNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchAdd"], font=font6)
            self.addNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.addNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(self.addNameLabel, 3, 1)
            # addLabel
            self.addLabel = QLabel("{0}".format(self.addValue), font=font6)
            self.addLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.addLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(self.addLabel, 3, 2)
            # editAddButton
            editAddButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            editAddButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            editAddButton.clicked.connect(partial(self.editAddVar, addDefaultValue, numberValidator))
            mainLayout.addWidget(editAddButton, 3, 3)
            self.setLabelColor(self.addNameLabel, self.addLabel, self.addValue, addDefaultValue)

    def setLabelColor(self, nameLabel, label, value, defaultValue):
        if defaultValue is None:
            color = QColor("green")
        else:
            if value > defaultValue:
                color = QColor("red")
            elif value < defaultValue:
                color = QColor("blue")
            else:
                color = QPalette().color(QPalette.WindowText)
        nameLabelPalette = nameLabel.palette()
        nameLabelPalette.setColor(QPalette.WindowText, color)
        nameLabel.setPalette(nameLabelPalette)
        labelPalette = label.palette()
        labelPalette.setColor(QPalette.WindowText, color)
        label.setPalette(labelPalette)

    def editSpeedVar(self, defaultValue, validator):
        editNotchVarDialog = EditNotchVarDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.notchIndex, self.speedValue, defaultValue, validator)
        if editNotchVarDialog.exec() == QDialog.Accepted:
            editValue = float(editNotchVarDialog.lineEdit.text())
            self.speedValue = editValue
            self.speedLabel.setText("{0}".format(self.speedValue))
            self.setLabelColor(self.speedNameLabel, self.speedLabel, self.speedValue, defaultValue)

    def editTlkVar(self, defaultValue, validator):
        root = self.window()
        noneTlkWidget = root.findChild(QWidget, "NoneTlkWidget")
        noneTlkValue = noneTlkWidget.perfValue
        weightWidget = root.findChild(QWidget, "WeightWidget")
        weightValue = weightWidget.perfValue
        editNotchVarDialog = EditNotchVarDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.notchIndex, self.tlkValue, defaultValue, validator, True, noneTlkValue, weightValue)
        if editNotchVarDialog.exec() == QDialog.Accepted:
            editValue = float(editNotchVarDialog.lineEdit.text())
            self.tlkValue = editValue
            self.tlkLabel.setText("{0}".format(self.tlkValue))
            self.setLabelColor(self.tlkNameLabel, self.tlkLabel, self.tlkValue, defaultValue)

    def editSoundVar(self, defaultValue, validator):
        editNotchVarDialog = EditNotchVarDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.notchIndex, self.soundValue, defaultValue, validator)
        if editNotchVarDialog.exec() == QDialog.Accepted:
            editValue = int(editNotchVarDialog.lineEdit.text())
            self.soundValue = editValue
            self.soundLabel.setText("{0}".format(self.soundValue))
            self.setLabelColor(self.soundNameLabel, self.soundLabel, self.soundValue, defaultValue)

    def editAddVar(self, defaultValue, validator):
        editNotchVarDialog = EditNotchVarDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.notchIndex, self.addValue, defaultValue, validator)
        if editNotchVarDialog.exec() == QDialog.Accepted:
            editValue = float(editNotchVarDialog.lineEdit.text())
            self.addValue = editValue
            self.addLabel.setText("{0}".format(self.addValue))
            self.setLabelColor(self.addNameLabel, self.addLabel, self.addValue, defaultValue)


class EditNotchVarDialog(QDialog):
    def __init__(self, parent, title, notchIndex, value, defaultValue, validator, calcFlag=False, noneTlkValue=None, weightValue=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.noneTlkValue = noneTlkValue
        self.weightValue = weightValue
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # defaultLabel
        defaultText = textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(defaultValue)
        defaultLabel = QLabel(defaultText, font=font2)
        layout.addWidget(defaultLabel)
        # separator
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(horizentalLine)

        if calcFlag:
            # calcMinSpeedLabel
            calcMinSpeedNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["calcMinSpeedLabel"].format(notchIndex, notchIndex + 1), font=font2)
            layout.addWidget(calcMinSpeedNameLabel)
            # calcMinSpeedValueLabel
            self.calcMinSpeedLabel = QLabel("", font=font2)
            layout.addWidget(self.calcMinSpeedLabel, alignment=Qt.AlignmentFlag.AlignCenter)
            # separator
            horizentalLine = QFrame()
            horizentalLine.setFrameShape(QFrame.Shape.HLine)
            horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
            layout.addWidget(horizentalLine)

        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        self.lineEdit.setValidator(validator)
        if calcFlag:
            self.lineEdit.textChanged.connect(self.calcMinSpeed)
        self.lineEdit.setText("{0}".format(value))
        layout.addWidget(self.lineEdit)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def calcMinSpeed(self):
        inputTlk = float(self.lineEdit.text())
        minSpeed = (self.weightValue - inputTlk) / self.noneTlkValue
        if minSpeed < 0:
            minSpeed = 0
        minSpeed = round(minSpeed * 60 / 1.11, 3)
        self.calcMinSpeedLabel.setText("{0}".format(minSpeed))

    def validate(self):
        if not self.lineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
