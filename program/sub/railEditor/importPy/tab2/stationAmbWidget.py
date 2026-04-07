from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QGridLayout,
    QFrame, QLabel, QLineEdit, QPushButton,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class StationAmbWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.stationList = decryptFile.stationList
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        mainGroupBox = QGroupBox(textSetting.textList["railEditor"]["stationInfoLabel"])
        mainGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - QGroupBox - QVBoxLayout
        stationAmbQVBoxLayout = QVBoxLayout()
        mainGroupBox.setLayout(stationAmbQVBoxLayout)
        # mainLayout - QGroupBox - QVBoxLayout - stationAmbCountGridLayout
        stationAmbCountGridLayout = QGridLayout()
        stationAmbCountGridLayout.setSpacing(0)
        stationAmbCountGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        stationAmbQVBoxLayout.addLayout(stationAmbCountGridLayout)
        # mainLayout - QGroupBox - QVBoxLayout - stationAmbCountGridLayout - stationAmbCountNameLabel
        stationAmbCountNameLabel = QLabel(textSetting.textList["railEditor"]["stationInfoCntLabel"], font=font6)
        stationAmbCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        stationAmbCountNameLabel.setFixedSize(fixedWidth * 2, fixedHeight)
        stationAmbCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stationAmbCountGridLayout.addWidget(stationAmbCountNameLabel, 0, 0)
        # mainLayout - QGroupBox - QVBoxLayout - stationAmbCountGridLayout - stationAmbCountLabel
        stationAmbCountLabel = QLabel("{0}".format(len(self.decryptFile.stationList)), font=font6)
        stationAmbCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        stationAmbCountLabel.setFixedSize(fixedWidth, fixedHeight)
        stationAmbCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stationAmbCountGridLayout.addWidget(stationAmbCountLabel, 0, 1)
        # mainLayout - QGroupBox - QVBoxLayout - stationAmbCountGridLayout - stationAmbCountButton
        stationAmbCountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
        stationAmbCountButton.setFixedSize(fixedWidth, fixedHeight)
        stationAmbCountGridLayout.addWidget(stationAmbCountButton, 0, 2)
        stationAmbCountButton.clicked.connect(self.editStationAmbCount)

        if len(self.decryptFile.stationList) > 0:
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout
            stationAmbGridLayout = QGridLayout()
            stationAmbGridLayout.setSpacing(0)
            stationAmbGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            stationAmbQVBoxLayout.addLayout(stationAmbGridLayout)
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - constHeaderLabel
            constHeaderLabel = QLabel(textSetting.textList["railEditor"]["stationConst0Label"], font=font6)
            constHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            constHeaderLabel.setFixedSize(fixedWidth, fixedHeight)
            constHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stationAmbGridLayout.addWidget(constHeaderLabel, 0, 0)
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - ambHeaderLabel
            ambHeaderLabel = QLabel(textSetting.textList["railEditor"]["stationAmbNoLabel"], font=font6)
            ambHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            ambHeaderLabel.setFixedSize(fixedWidth * 2, fixedHeight)
            ambHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stationAmbGridLayout.addWidget(ambHeaderLabel, 0, 1)
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - ambChildHeaderLabel
            ambChildHeaderLabel = QLabel(textSetting.textList["railEditor"]["stationAmbChildNoLabel"], font=font6)
            ambChildHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            ambChildHeaderLabel.setFixedSize(fixedWidth * 2, fixedHeight)
            ambChildHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stationAmbGridLayout.addWidget(ambChildHeaderLabel, 0, 2)
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - elementHeaderLabel
            elementHeaderLabel = QLabel(textSetting.textList["railEditor"]["stationElementLabel"], font=font6)
            elementHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            elementHeaderLabel.setFixedSize(fixedWidth, fixedHeight)
            elementHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stationAmbGridLayout.addWidget(elementHeaderLabel, 0, 3)
            # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - pngNumberHeaderLabel
            pngNumberHeaderLabel = QLabel(textSetting.textList["railEditor"]["stationImgNoLabel"], font=font6)
            pngNumberHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            pngNumberHeaderLabel.setFixedSize(fixedWidth * 2, fixedHeight)
            pngNumberHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stationAmbGridLayout.addWidget(pngNumberHeaderLabel, 0, 4)

            for i, stationInfo in enumerate(self.decryptFile.stationList):
                for j, stationValue in enumerate(stationInfo):
                    # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - label
                    stationAmbLabel = QLabel("{0}".format(stationValue), font=font6)
                    stationAmbLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                    stationAmbLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    stationAmbGridLayout.addWidget(stationAmbLabel, i + 1, j)
                # mainLayout - QGroupBox - QVBoxLayout - stationAmbGridLayout - button
                stationAmbButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
                stationAmbButton.setFixedSize(fixedWidth, fixedHeight)
                stationAmbGridLayout.addWidget(stationAmbButton, i + 1, len(stationInfo))
                stationAmbButton.clicked.connect(partial(self.editStation, i, stationInfo))

    def editStationAmbCount(self):
        editStationAmbCntWidget = EditStationAmbCntWidget(self, textSetting.textList["railEditor"]["editStationCntLabel"], self.decryptFile)
        if editStationAmbCntWidget.exec() == QDialog.Accepted:
            resultValue = int(editStationAmbCntWidget.lineEdit.text())
            if not self.decryptFile.saveStationCnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I77"])
            self.reloadFunc()

    def editStation(self, i, stationInfo):
        editStationAmbWidget = EditStationAmbWidget(self, textSetting.textList["railEditor"]["editStationInfoLabel"], self.decryptFile, stationInfo)
        if editStationAmbWidget.exec() == QDialog.Accepted:
            self.stationList[i] = editStationAmbWidget.resultValueList
            if not self.decryptFile.saveStation(self.stationList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I78"])
            self.reloadFunc()


class EditStationAmbCntWidget(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.val = len(decryptFile.stationList)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        validator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.lineEdit.setValidator(validator)
        self.lineEdit.setText("{0}".format(self.val))
        layout.addWidget(self.lineEdit)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if not self.lineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E60"])
            return

        resultValue = int(self.lineEdit.text())
        if resultValue < len(self.decryptFile.stationList):
            msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
            if result != mb.OK:
                return
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditStationAmbWidget(QDialog):
    def __init__(self, parent, title, decryptFile, stationInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.stationInfo = stationInfo
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.stationAmbGridLayout = QGridLayout()
        layout.addLayout(self.stationAmbGridLayout)
        self.lineEditList = []
        stationInfoLabelList = textSetting.textList["railEditor"]["editStationInfoLabelList"]
        for i, stationInfoLabel in enumerate(stationInfoLabelList):
            # layout - QGridLayout - stationLabel
            stationLabel = QLabel(stationInfoLabel, font=font2)
            self.stationAmbGridLayout.addWidget(stationLabel, i, 0)
            # layout - QGridLayout - railLineEdit
            stationLineEdit = QLineEdit(font=font2)
            stationLineEdit.setText("{0}".format(self.stationInfo[i]))
            stationLineEdit.setValidator(integerValidator)
            self.lineEditList.append(stationLineEdit)
            self.stationAmbGridLayout.addWidget(stationLineEdit, i, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            self.resultValueList.append(int(lineEdit.text()))
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
