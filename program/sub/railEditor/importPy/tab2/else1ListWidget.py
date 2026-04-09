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


class Else1ListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.else1List = decryptFile.else1List
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        mainGroupBox = QGroupBox(textSetting.textList["railEditor"]["else1Label"])
        mainGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - QGroupBox - QVBoxLayout
        groupBoxInLayout = QVBoxLayout()
        mainGroupBox.setLayout(groupBoxInLayout)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            # mainLayout - QGroupBox - QGridLayout
            else1SingleGridLayout = QGridLayout()
            else1SingleGridLayout.setSpacing(0)
            else1SingleGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            groupBoxInLayout.addLayout(else1SingleGridLayout)
            # mainLayout - QGroupBox - QGridLayout - else1SingleLabel
            else1SingleNameLabel = QLabel("{0}".format(round(float(self.else1List[0]), 3)), font=font6)
            else1SingleNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            else1SingleNameLabel.setFixedSize(fixedWidth, fixedHeight)
            else1SingleNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else1SingleGridLayout.addWidget(else1SingleNameLabel, 0, 0)
            # mainLayout - QGroupBox - QGridLayout - else1SingleButton
            else1SingleButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            else1SingleButton.clicked.connect(partial(self.editVarList, 0, [self.else1List[0]]))
            else1SingleGridLayout.addWidget(else1SingleButton, 0, 1)

            # mainLayout - QGroupBox - QGridLayout(List)
            else1ListGridLayout = QGridLayout()
            else1ListGridLayout.setSpacing(0)
            else1ListGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            groupBoxInLayout.addLayout(else1ListGridLayout)
            for i in range(1, len(self.else1List)):
                else1Info = self.else1List[i]
                for j in range(len(else1Info)):
                    # mainLayout - QGroupBox - QGridLayout(List) - label
                    if j in [0, 1]:
                        else1Value = round(float(else1Info[j]), 3)
                    else:
                        else1Value = int(else1Info[j])
                    else1Label = QLabel("{0}".format(else1Value), font=font6)
                    else1Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                    else1Label.setFixedSize(fixedWidth, fixedHeight)
                    else1Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    else1ListGridLayout.addWidget(else1Label, i, j)
                # mainLayout - QGroupBox - QGridLayout(List) - button
                else1Button = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
                else1Button.clicked.connect(partial(self.editVarList, i, else1Info))
                else1ListGridLayout.addWidget(else1Button, i, len(else1Info))
        else:
            # mainLayout - QGroupBox - QGridLayout(List)
            else1ListGridLayout = QGridLayout()
            else1ListGridLayout.setSpacing(0)
            else1ListGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            groupBoxInLayout.addLayout(else1ListGridLayout)
            for i in range(len(self.else1List)):
                else1Value = round(float(self.else1List[i]), 5)
                # mainLayout - QGroupBox - QGridLayout(List) - label
                else1Label = QLabel("{0}".format(else1Value), font=font6)
                else1Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                else1Label.setFixedSize(fixedWidth, fixedHeight)
                else1Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else1ListGridLayout.addWidget(else1Label, 0, i)
            # mainLayout - QGroupBox - QGridLayout(List) - button
            else1Button = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            else1Button.clicked.connect(self.editVarLsElse1List)
            else1ListGridLayout.addWidget(else1Button, 0, len(self.else1List))

    def editVarList(self, i, valList):
        editElse1ListWidget = EditElse1ListWidget(self, textSetting.textList["railEditor"]["editElse1Label"], self.decryptFile, valList)
        if editElse1ListWidget.exec() == QDialog.Accepted:
            if i == 0:
                self.else1List[i] = editElse1ListWidget.resultValueList[0]
            else:
                self.else1List[i] = editElse1ListWidget.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I75"])
            self.reloadFunc()

    def editVarLsElse1List(self):
        editLsElse1ListWidget = EditLsElse1ListWidget(self, textSetting.textList["railEditor"]["editElse1Label"], self.decryptFile)
        if editLsElse1ListWidget.exec() == QDialog.Accepted:
            self.else1List = editLsElse1ListWidget.resultValueList
            if not self.decryptFile.saveElse1List(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I75"])
            self.reloadFunc()


class EditElse1ListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, valList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.valList = valList
        self.resultValueList = []

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.else1ListGridLayout = QGridLayout()
        layout.addLayout(self.else1ListGridLayout)
        self.lineEditList = []
        for i, val in enumerate(self.valList):
            if i < 2:
                labelValue = textSetting.textList["railEditor"]["editElse1F1Label"].format(i + 1)
                lineEditValue = round(float(val), 3)
            else:
                labelValue = textSetting.textList["railEditor"]["editElse1B1Label"].format(i - 1)
                lineEditValue = val
            # layout - QGridLayout - else1Label
            eles1Label = QLabel(labelValue, font=font2)
            self.else1ListGridLayout.addWidget(eles1Label, i, 0)
            # layout - QGridLayout - else1LineEdit
            else1LineEdit = QLineEdit(font=font2)
            else1LineEdit.setText("{0}".format(lineEditValue))
            if i < 2:
                else1LineEdit.setValidator(numberValidator)
            else:
                else1LineEdit.setValidator(integerValidator)
            self.lineEditList.append(else1LineEdit)
            self.else1ListGridLayout.addWidget(else1LineEdit, i, 1)

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
            if i < 2:
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


class EditLsElse1ListWidget(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.else1List = decryptFile.else1List
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.else1ListGridLayout = QGridLayout()
        layout.addLayout(self.else1ListGridLayout)
        self.lineEditList = []
        for i, else1Value in enumerate(self.else1List):
            # layout - QGridLayout - else1Label
            labelValue = textSetting.textList["railEditor"]["editElse1F1Label"].format(i + 1)
            eles1Label = QLabel(labelValue, font=font2)
            self.else1ListGridLayout.addWidget(eles1Label, i, 0)
            # layout - QGridLayout - else1LineEdit
            else1LineEdit = QLineEdit(font=font2)
            else1LineEdit.setText("{0}".format(round(float(else1Value), 5)))
            else1LineEdit.setValidator(numberValidator)
            self.lineEditList.append(else1LineEdit)
            self.else1ListGridLayout.addWidget(else1LineEdit, i, 1)

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
            self.resultValueList.append(float(lineEdit.text()))
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
