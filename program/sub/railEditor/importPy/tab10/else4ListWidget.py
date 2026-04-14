from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QScrollArea, QGridLayout,
    QFrame, QLabel, QLineEdit, QPushButton,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class Else4ListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.else4List = decryptFile.else4List
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        if self.decryptFile.game == "LSTrial":
            return

        if self.decryptFile.game == "LS" and self.decryptFile.ver != "DEND_MAP_VER0101":
            return

        # else4InfoLayout
        else4InfoLayout = QVBoxLayout(self)
        # else4InfoLayout - else4CountGridLayout
        else4CountGridLayout = QGridLayout()
        else4CountGridLayout.setSpacing(0)
        else4CountGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        else4InfoLayout.addLayout(else4CountGridLayout)
        # else4InfoLayout - else4CountGridLayout - else4CountNameLabel
        else4CountNameLabel = QLabel(textSetting.textList["railEditor"]["else4CntLabel"], font=font6)
        else4CountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        else4CountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        else4CountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else4CountGridLayout.addWidget(else4CountNameLabel, 0, 0)
        # else4InfoLayout - else4CountGridLayout - else4CountLabel
        else4CountLabel = QLabel("{0}".format(len(self.else4List)), font=font6)
        else4CountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        else4CountLabel.setFixedSize(fixedWidth, fixedHeight)
        else4CountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else4CountGridLayout.addWidget(else4CountLabel, 0, 1)
        if self.decryptFile.game == "RS":
            # else4InfoLayout - else4CountGridLayout - eles4CountButton
            eles4CountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            eles4CountButton.clicked.connect(self.editElse4Count)
            else4CountGridLayout.addWidget(eles4CountButton, 0, 2)

        for i, else4Info in enumerate(self.else4List):
            # else4InfoLayout - else4InfoGridLayout
            else4InfoGridLayout = QGridLayout()
            else4InfoGridLayout.setSpacing(0)
            else4InfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            else4InfoLayout.addLayout(else4InfoGridLayout)
            # else4InfoLayout - else4InfoGridLayout - eles4InfoModifyButton
            eles4InfoModifyButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            eles4InfoModifyButton.setEnabled(True)
            eles4InfoModifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            eles4InfoModifyButton.clicked.connect(partial(self.editElse4Info, i, else4Info))
            else4InfoGridLayout.addWidget(eles4InfoModifyButton, 0, 0)
            # else4InfoLayout - else4InfoGridLayout - railNoLabel
            railNoLabel = QLabel("{0}".format(else4Info[0]), font=font6)
            railNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            railNoLabel.setFixedSize(fixedWidth * 2, fixedHeight)
            railNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else4InfoGridLayout.addWidget(railNoLabel, 0, 1)
            # else4InfoLayout - else4InfoGridLayout - prevRailNoLabel
            prevRailNoLabel = QLabel("{0}".format(else4Info[1]), font=font6)
            prevRailNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            prevRailNoLabel.setFixedSize(fixedWidth * 2, fixedHeight)
            prevRailNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else4InfoGridLayout.addWidget(prevRailNoLabel, 0, 2)

            for j in range(3):
                # else4InfoLayout - else4InfoGridLayout - posLabel
                posLabel = QLabel("{0}".format(else4Info[2 + j]), font=font6)
                posLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                posLabel.setFixedSize(fixedWidth * 2, fixedHeight)
                posLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else4InfoGridLayout.addWidget(posLabel, 1, 1 + j)
            for j in range(3):
                # else4InfoLayout - else4InfoGridLayout - rotLabel
                rotLabel = QLabel("{0}".format(else4Info[5 + j]), font=font6)
                rotLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                rotLabel.setFixedSize(fixedWidth * 2, fixedHeight)
                rotLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else4InfoGridLayout.addWidget(rotLabel, 2, 1 + j)
        else4InfoLayout.addStretch()

    def editElse4Count(self):
        editElse4CountWidget = EditElse4CountWidget(self, textSetting.textList["railEditor"]["editElse4CntLabel"], self.decryptFile)
        if editElse4CountWidget.exec() == QDialog.Accepted:
            resultValue = int(editElse4CountWidget.lineEdit.text())
            if not self.decryptFile.saveElse4Cnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I93"])
            self.reloadFunc()

    def editElse4Info(self, i, valList):
        editElse4ListWidget = EditElse4ListWidget(self, textSetting.textList["railEditor"]["editElse4Label"], self.decryptFile, valList)
        if editElse4ListWidget.exec() == QDialog.Accepted:
            self.else4List[i] = editElse4ListWidget.resultValueList
            if not self.decryptFile.saveElse4List(self.else4List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I94"])
            self.reloadFunc()


class EditElse4CountWidget(QDialog):
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
        self.lineEdit.setText("{0}".format(len(decryptFile.else4List)))
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
        if resultValue < len(self.decryptFile.else4List):
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


class EditElse4ListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, else4Info):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.else4Info = else4Info
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
        self.else4InfoGridLayout = QGridLayout()
        layout.addLayout(self.else4InfoGridLayout)
        self.lineEditList = []
        else4InfoLabelList = textSetting.textList["railEditor"]["editElse4ElementLabelList"]
        for i, else4Value in enumerate(self.else4Info):
            # layout - QGridLayout - else4Label
            else4Label = QLabel("{0}".format(else4InfoLabelList[i]), font=font2)
            self.else4InfoGridLayout.addWidget(else4Label, i, 0)
            # layout - QGridLayout - else4LineEdit
            else4LineEdit = QLineEdit(font=font2)
            if i in [0, 1]:
                else4LineEdit.setValidator(integerValidator)
            else:
                else4LineEdit.setValidator(numberValidator)
            else4LineEdit.setText("{0}".format(else4Value))
            self.lineEditList.append(else4LineEdit)
            self.else4InfoGridLayout.addWidget(else4LineEdit, i, 1)

            if self.decryptFile.game in ["BS", "CS"]:
                if i == 0:
                    else4LineEdit.setEnabled(False)
            elif self.decryptFile.game == "LS":
                if i in [0, 1]:
                    else4LineEdit.setEnabled(False)

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
            if i in [0, 1]:
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
