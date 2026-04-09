from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QFrame, QLabel, QLineEdit, QPushButton,
    QDialog, QDialogButtonBox
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class Else2ListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.else2List = decryptFile.else2List
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)

        # mainLayout - QGridLayout
        else2CountGridLayout = QGridLayout()
        else2CountGridLayout.setSpacing(0)
        else2CountGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        mainLayout.addLayout(else2CountGridLayout)
        # mainLayout - QGridLayout - else2CountNameLabel
        else2CountNameLabel = QLabel(textSetting.textList["railEditor"]["else2CntLabel"], font=font6)
        else2CountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        else2CountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        else2CountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else2CountGridLayout.addWidget(else2CountNameLabel, 0, 0)
        # mainLayout - QGridLayout - else2CountLabel
        else2CountLabel = QLabel("{0}".format(len(self.else2List)), font=font6)
        else2CountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        else2CountLabel.setFixedSize(fixedWidth, fixedHeight)
        else2CountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else2CountGridLayout.addWidget(else2CountLabel, 0, 1)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            # mainLayout - QGridLayout - else2CountButton
            else2CountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            else2CountButton.clicked.connect(self.editElse2Count)
            else2CountGridLayout.addWidget(else2CountButton, 0, 2)

        # mainLayout - QGridLayout(List)
        else2ListGridLayout = QGridLayout()
        else2ListGridLayout.setSpacing(0)
        else2ListGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        mainLayout.addLayout(else2ListGridLayout)
        for i, else2Info in enumerate(self.else2List):
            for j in range(len(else2Info)):
                # mainLayout - QGroupBox - QGridLayout(List) - label
                if j in [2, 3, 4]:
                    else1Value = round(float(else2Info[j]), 3)
                else:
                    else1Value = int(else2Info[j])
                else2Label = QLabel("{0}".format(else1Value), font=font6)
                else2Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                else2Label.setFixedSize(fixedWidth, fixedHeight)
                else2Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else2ListGridLayout.addWidget(else2Label, i, j)
            # mainLayout - QGridLayout(List) - button
            else2Button = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            else2Button.clicked.connect(partial(self.editElse2List, i, else2Info))
            else2ListGridLayout.addWidget(else2Button, i, len(else2Info))

    def editElse2Count(self):
        editElse2CountWidget = EditElse2CountWidget(self, textSetting.textList["railEditor"]["modifyElse2CntLabel"], self.decryptFile)
        if editElse2CountWidget.exec() == QDialog.Accepted:
            resultValue = int(editElse2CountWidget.lineEdit.text())
            if not self.decryptFile.saveElse2Cnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I82"])
            self.reloadFunc()

    def editElse2List(self, i, valList):
        editElse2ListWidget = EditElse2ListWidget(self, textSetting.textList["railEditor"]["modifyElse2InfoLabel"], self.decryptFile, valList)
        if editElse2ListWidget.exec() == QDialog.Accepted:
            self.else2List[i] = editElse2ListWidget.resultValueList
            if not self.decryptFile.saveElse2List(self.else2List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I83"])
            self.reloadFunc()


class EditElse2CountWidget(QDialog):
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
        self.lineEdit.setText("{0}".format(len(decryptFile.else2List)))
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
        if resultValue < len(self.decryptFile.else2List):
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


class EditElse2ListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, else2Info):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.else2Info = else2Info
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.else2InfoGridLayout = QGridLayout()
        layout.addLayout(self.else2InfoGridLayout)
        self.lineEditList = []
        else2InfoLabelList = textSetting.textList["railEditor"]["editElse2LabelList"]
        for i, else2InfoLabel in enumerate(else2InfoLabelList):
            # layout - QGridLayout - else2InfoLabel
            else2Label = QLabel(else2InfoLabel, font=font2)
            self.else2InfoGridLayout.addWidget(else2Label, i, 0)
            # layout - QGridLayout - railLineEdit
            else2LineEdit = QLineEdit(font=font2)
            if i in [2, 3, 4]:
                lineEditValue = round(float(self.else2Info[i]), 3)
                else2LineEdit.setValidator(numberValidator)
            else:
                lineEditValue = int(self.else2Info[i])
                else2LineEdit.setValidator(integerValidator)
            else2LineEdit.setText("{0}".format(lineEditValue))
            self.lineEditList.append(else2LineEdit)
            self.else2InfoGridLayout.addWidget(else2LineEdit, i, 1)

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
            if i in [2, 3, 4]:
                self.resultValueList.append(float(lineEdit.text()))
            else:
                self.resultValueList.append(int(lineEdit.text()))
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
