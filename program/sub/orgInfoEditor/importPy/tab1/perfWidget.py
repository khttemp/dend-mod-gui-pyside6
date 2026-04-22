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


class PerfWidget(QWidget):
    def __init__(self, decryptFile, perfName, perfValue, defaultValue):
        super().__init__()
        self.decryptFile = decryptFile
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        fixedWidth = 100
        fixedHeight = 40

        # perfNameLabel
        self.perfNameLabel = QLabel(perfName, font=font6)
        self.perfNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perfNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.perfNameLabel, 0, 0)
        # perfLabel
        self.perfValue = perfValue
        self.perfLabel = QLabel("{0}".format(self.perfValue), font=font6)
        self.perfLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perfLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.perfLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(self.perfLabel, 0, 1)
        # editPerfButton
        editPerfButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editPerfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        editPerfButton.clicked.connect(partial(self.editVar, defaultValue))
        mainLayout.addWidget(editPerfButton, 0, 2)
        self.setLabelColor(self.perfNameLabel, self.perfLabel, self.perfValue, defaultValue)

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

    def editVar(self, defaultValue):
        editPerfVarDialog = EditPerfVarDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.perfValue, defaultValue)
        if editPerfVarDialog.exec() == QDialog.Accepted:
            editValue = float(editPerfVarDialog.lineEdit.text())
            self.perfValue = editValue
            self.perfLabel.setText("{0}".format(self.perfValue))
            self.setLabelColor(self.perfNameLabel, self.perfLabel, self.perfValue, defaultValue)


class EditPerfVarDialog(QDialog):
    def __init__(self, parent, title, value, defaultValue):
        super().__init__(parent)
        self.setWindowTitle(title)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?"), self)

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

        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        self.lineEdit.setValidator(numberValidator)
        self.lineEdit.setText("{0}".format(value))
        layout.addWidget(self.lineEdit)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if not self.lineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
