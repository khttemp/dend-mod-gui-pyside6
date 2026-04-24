from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QGroupBox, QGridLayout,
    QLabel, QLineEdit, QPushButton, QDialog,
    QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class FixedList2Widget(QWidget):
    def __init__(self, trainIndex, decryptFile, groupBoxTitle, elseList, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.reloadWidget = reloadWidget

        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 140

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - mainGroupBox
        mainGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - mainGroupBox - QVBoxLayout
        mainInLayout = QGridLayout()
        mainInLayout.setContentsMargins(0, 0, 0, 0)
        mainInLayout.setSpacing(0)
        mainGroupBox.setLayout(mainInLayout)

        for i, elseValue in enumerate(self.elseList):
            # mainInLayout - numValueLabel
            numValueLabel = QLabel("{0}".format(elseValue[0]), font=font6)
            numValueLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            numValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            numValueLabel.setFixedWidth(fixedWidth / 2)
            mainInLayout.addWidget(numValueLabel, i, 0)
            # mainInLayout - textValueLabel
            textValueLabel = QLabel("{0}".format(elseValue[1]), font=font6)
            textValueLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            textValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            textValueLabel.setFixedWidth(fixedWidth)
            mainInLayout.addWidget(textValueLabel, i, 1)
            # mainInLayout - elseButton
            elseButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            elseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            elseButton.clicked.connect(partial(self.editVar, i))
            mainInLayout.addWidget(elseButton, i, 2)

    def editVar(self, i):
        editFixedList2Widget = EditFixedList2Widget(self, textSetting.textList["orgInfoEditor"]["fixedList2ModifyLabel"], self.elseList[i])
        if editFixedList2Widget.exec() == QDialog.Accepted:
            self.elseList[i] = editFixedList2Widget.resultValueList
            if not self.decryptFile.saveElse2List(self.trainIndex, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadWidget()


class EditFixedList2Widget(QDialog):
    def __init__(self, parent, title, valList):
        super().__init__(parent)
        self.setWindowTitle(title)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.valList = valList
        self.resultValueList = []
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        elseInfoGridLayout = QGridLayout()
        layout.addLayout(elseInfoGridLayout)
        self.lineEditList = []
        for i, elseValue in enumerate(valList):
            # layout - QGridLayout - railLabel
            if i == 0:
                nameText = textSetting.textList["orgInfoEditor"]["fixedList2NumLabel"]
            else:
                nameText = textSetting.textList["orgInfoEditor"]["fixedList2NameLabel"]
            elseInfoNameLabel = QLabel(nameText, font=font2)
            elseInfoGridLayout.addWidget(elseInfoNameLabel, i, 0)
            # layout - QGridLayout - railLineEdit
            elseInfoLineEdit = QLineEdit(font=font2)
            if i == 0:
                elseInfoLineEdit.setValidator(integerValidator)
            elseInfoLineEdit.setText("{0}".format(elseValue))
            self.lineEditList.append(elseInfoLineEdit)
            elseInfoGridLayout.addWidget(elseInfoLineEdit, i, 1)

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

            if i == 0:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                self.resultValueList.append(lineEdit.text())
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
