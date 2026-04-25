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


class FixedListWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, groupBoxTitle, elseList, ver, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elseList = elseList
        self.ver = ver
        self.reloadWidget = reloadWidget

        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 60

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
            if decryptFile.game == "LS" and ver == 1:
                # mainInLayout - nameLabel
                nameLabel = QLabel(textSetting.textList["orgInfoEditor"]["fixedListNumLabel"].format(i + 1), font=font6)
                nameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                nameLabel.setFixedWidth(fixedWidth)
                mainInLayout.addWidget(nameLabel, i, 0)
            # mainInLayout - valueLabel
            valueLabel = QLabel("{0}".format(elseValue), font=font6)
            valueLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainInLayout.addWidget(valueLabel, i, 1)
            # mainInLayout - elseButton
            elseButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            elseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            elseButton.clicked.connect(partial(self.editVar, i))
            mainInLayout.addWidget(elseButton, i, 2)

            if decryptFile.game == "LS" and ver == 1:
                valueLabel.setFixedWidth(fixedWidth)

    def editVar(self, i):
        editFixedListDialog = EditFixedListDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.elseList[i], self.decryptFile.game, self.ver)
        if editFixedListDialog.exec() == QDialog.Accepted:
            resultValue = editFixedListDialog.lineEdit.text()
            if self.decryptFile.game == "LS" and self.ver == 1:
                resultValue = int(resultValue)
            self.elseList[i] = resultValue
            if not self.decryptFile.saveElseList(self.trainIndex, self.ver, self.elseList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I61"])
            self.reloadWidget()


class EditFixedListDialog(QDialog):
    def __init__(self, parent, title, value, game, ver):
        super().__init__(parent)
        self.setWindowTitle(title)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)
        self.lineEdit.setText("{0}".format(value))
        if game == "LS" and ver == 1:
            self.lineEdit.setValidator(integerValidator)
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
        return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
