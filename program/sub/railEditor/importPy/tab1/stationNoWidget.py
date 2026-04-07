import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton,
    QDialog, QDialogButtonBox
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class StationNoWidget(QWidget):
    def __init__(self, num, decryptFile, stationNo, reloadFunc):
        super().__init__()
        self.num = num
        self.decryptFile = decryptFile
        self.stationNo = stationNo
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # mainLayout - stationNoNameLabel
        stationNoNameLabel = QLabel(textSetting.textList["railEditor"]["stationNo"], font=font6)
        stationNoNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        stationNoNameLabel.setFixedSize(fixedWidth * 2, fixedHeight)
        stationNoNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(stationNoNameLabel, 0, 0)
        # mainLayout - stationNoLabel
        stationNoLabel = QLabel("{0}".format(self.stationNo), font=font6)
        stationNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        stationNoLabel.setFixedSize(fixedWidth, fixedHeight)
        stationNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(stationNoLabel, 0, 1)

        # mainLayout - stationNoButton
        stationNoButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
        stationNoButton.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(stationNoButton, 0, 2)
        stationNoButton.clicked.connect(self.editVar)

    def editVar(self):
        editStationNoWidget = EditStationNoWidget(self, textSetting.textList["railEditor"]["editStationNoLabel"], self.decryptFile, self.stationNo)
        if editStationNoWidget.exec() == QDialog.Accepted:
            resultValue = int(editStationNoWidget.lineEdit.text())
            if not self.decryptFile.saveStationNo(self.num, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I139"])
            self.reloadFunc()


class EditStationNoWidget(QDialog):
    def __init__(self, parent, title, decryptFile, stationNo):
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
        rx = QRegularExpression(r"^\d+$")
        validator = QRegularExpressionValidator(rx, self)
        self.lineEdit.setValidator(validator)
        self.lineEdit.setText("{0}".format(stationNo))
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
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
