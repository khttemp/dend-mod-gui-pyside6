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


class BinAnimeListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.binAnimeList = decryptFile.binAnimeList
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        mainGroupBox = QGroupBox(textSetting.textList["railEditor"]["editBaseBinAnimeLabel"])
        mainGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - QGroupBox - QVBoxLayout
        binAnimeQVBoxLayout = QVBoxLayout()
        mainGroupBox.setLayout(binAnimeQVBoxLayout)
        # mainLayout - QGroupBox - QVBoxLayout - binAnimeCountGridLayout
        binAnimeCountGridLayout = QGridLayout()
        binAnimeCountGridLayout.setSpacing(0)
        binAnimeCountGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        binAnimeQVBoxLayout.addLayout(binAnimeCountGridLayout)
        # mainLayout - QGroupBox - QVBoxLayout - binAnimeCountGridLayout - binAnimeCountNameLabel
        binAnimeCountNameLabel = QLabel(textSetting.textList["railEditor"]["animeCntLabel"], font=font6)
        binAnimeCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        binAnimeCountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        binAnimeCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        binAnimeCountGridLayout.addWidget(binAnimeCountNameLabel, 0, 0)
        # mainLayout - QGroupBox - QVBoxLayout - binAnimeCountGridLayout - binAnimeCountLabel
        binAnimeCountLabel = QLabel("{0}".format(len(self.binAnimeList)), font=font6)
        binAnimeCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        binAnimeCountLabel.setFixedSize(fixedWidth, fixedHeight)
        binAnimeCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        binAnimeCountGridLayout.addWidget(binAnimeCountLabel, 0, 1)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            # mainLayout - QGroupBox - QVBoxLayout - binAnimeCountGridLayout - binAnimeCountButton
            binAnimeCountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            binAnimeCountButton.setFixedSize(fixedWidth, fixedHeight)
            binAnimeCountGridLayout.addWidget(binAnimeCountButton, 0, 2)
            binAnimeCountButton.clicked.connect(self.editBinAnimeCount)

        if len(self.binAnimeList) > 0:
            # mainLayout - QGroupBox - QVBoxLayout - binAnimeGridLayout
            binAnimeGridLayout = QGridLayout()
            binAnimeGridLayout.setSpacing(0)
            binAnimeGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            binAnimeQVBoxLayout.addLayout(binAnimeGridLayout)
            # mainLayout - QGroupBox - QVBoxLayout - binAnimeGridLayout - binAnimeHeaderLabel
            binAnimeHeaderList = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
            for i, binAnimeHeaderInfo in enumerate(binAnimeHeaderList):
                headerLabel = QLabel(binAnimeHeaderInfo, font=font6)
                headerLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                headerLabel.setFixedSize(fixedWidth, fixedHeight)
                headerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                binAnimeGridLayout.addWidget(headerLabel, 0, i)

            for i, binAnimeInfo in enumerate(self.binAnimeList):
                for j, binAnimeValue in enumerate(binAnimeInfo):
                    # mainLayout - QGroupBox - QVBoxLayout - binAnimeGridLayout - label
                    binAnimeLabel = QLabel("{0}".format(binAnimeValue), font=font6)
                    binAnimeLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                    binAnimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    binAnimeGridLayout.addWidget(binAnimeLabel, i + 1, j)
                # mainLayout - QGroupBox - QVBoxLayout - binAnimeGridLayout - button
                binAnimeButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
                binAnimeButton.setFixedSize(fixedWidth, fixedHeight)
                binAnimeGridLayout.addWidget(binAnimeButton, i + 1, len(binAnimeInfo))
                binAnimeButton.clicked.connect(partial(self.editBinAnime, i, binAnimeInfo))

    def editBinAnimeCount(self):
        editBinAnimeCountWidget = EditBinAnimeCountWidget(self, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile)
        if editBinAnimeCountWidget.exec() == QDialog.Accepted:
            resultValue = int(editBinAnimeCountWidget.lineEdit.text())
            if not self.decryptFile.saveBinAnimeCnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I73"])
            self.reloadFunc()

    def editBinAnime(self, i, binAnimeInfo):
        editBinAnimeWidget = EditBinAnimeWidget(self, textSetting.textList["railEditor"]["editAnimeCntLabel"], self.decryptFile, binAnimeInfo)
        if editBinAnimeWidget.exec() == QDialog.Accepted:
            self.binAnimeList[i] = editBinAnimeWidget.resultValueList
            if not self.decryptFile.saveBinAnime(self.binAnimeList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I74"])
            self.reloadFunc()


class EditBinAnimeCountWidget(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
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
        self.lineEdit.setText("{0}".format(len(decryptFile.binAnimeList)))
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
        if resultValue < len(self.decryptFile.binAnimeList):
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


class EditBinAnimeWidget(QDialog):
    def __init__(self, parent, title, decryptFile, binAnimeInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.binAnimeInfo = binAnimeInfo
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.binAnimeGridLayout = QGridLayout()
        layout.addLayout(self.binAnimeGridLayout)
        self.lineEditList = []
        binAnimeInfoLabelList = textSetting.textList["railEditor"]["editBinAnimeHeaderList"]
        for i, binAnimeInfoLabel in enumerate(binAnimeInfoLabelList):
            # layout - QGridLayout - binAnimeLabel
            binAnimeLabel = QLabel(binAnimeInfoLabel, font=font2)
            self.binAnimeGridLayout.addWidget(binAnimeLabel, i, 0)
            # layout - QGridLayout - binAnimeLineEdit
            binAnimeLineEdit = QLineEdit(font=font2)
            binAnimeLineEdit.setText("{0}".format(self.binAnimeInfo[i]))
            binAnimeLineEdit.setValidator(integerValidator)
            self.lineEditList.append(binAnimeLineEdit)
            self.binAnimeGridLayout.addWidget(binAnimeLineEdit, i, 1)

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
