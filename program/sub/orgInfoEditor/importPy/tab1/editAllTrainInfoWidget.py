import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QDialogButtonBox,
    QLabel, QComboBox, QLineEdit
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class EditAllTrainInfoDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        font2 = QFont(textSetting.textList["font6"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - mainLayout
        mainLayout = QHBoxLayout()
        layout.addLayout(mainLayout)
        # layout - mainLayout - perfTextLabel
        perfTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["perfElement"], font=font2)
        mainLayout.addWidget(perfTextLabel)
        # layout - mainLayout - perfTextCombo
        self.perfTextCombo = QComboBox(font=font2)
        self.perfTextCombo.addItems(decryptFile.trainPerfNameList)
        mainLayout.addWidget(self.perfTextCombo)
        # layout - mainLayout - perfAllTextLabel
        perfAllTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["perfAllTrainLabel"], font=font2)
        mainLayout.addWidget(perfAllTextLabel)
        # layout - mainLayout - lineEdit
        self.lineEdit = QLineEdit("1.0", font=font2)
        self.lineEdit.setValidator(numberValidator)
        self.lineEdit.setFixedWidth(70)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
        mainLayout.addWidget(self.lineEdit)
        # layout - mainLayout - perfCalcCombo
        self.perfCalcCombo = QComboBox(font=font2)
        self.perfCalcCombo.addItems(textSetting.textList["orgInfoEditor"]["perfCalcList"])
        mainLayout.addWidget(self.perfCalcCombo)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if not self.lineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return

        if self.perfCalcCombo.currentIndex() == 0:
            warnMsg = textSetting.textList["infoList"]["I52"]
        else:
            warnMsg = textSetting.textList["infoList"]["I53"]
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

        if result == mb.OK:
            perfIndex = self.perfTextCombo.currentIndex()
            num = float(self.lineEdit.text())

            if not self.decryptFile.saveAllEdit(perfIndex, num, self.perfCalcCombo.currentIndex()):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I54"])
