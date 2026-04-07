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


class TrainCountWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # mainLayout - trainCountNameLabel
        trainCountNameLabel = QLabel(textSetting.textList["railEditor"]["trainCount"], font=font6)
        trainCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        trainCountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        trainCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(trainCountNameLabel, 0, 0)
        # mainLayout - trainCountLabel
        trainCountLabel = QLabel("{0}".format(self.decryptFile.trainCnt), font=font6)
        trainCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        trainCountLabel.setFixedSize(fixedWidth, fixedHeight)
        trainCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(trainCountLabel, 0, 1)

        if not (self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag):
            # mainLayout - trainCountButton
            trainCountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            trainCountButton.setFixedSize(fixedWidth, fixedHeight)
            mainLayout.addWidget(trainCountButton, 0, 2)
            trainCountButton.clicked.connect(self.editVar)

    def editVar(self):
        editTrainCountWidget = EditTrainCountWidget(self, textSetting.textList["railEditor"]["editTrainCountLabel"], self.decryptFile)
        if editTrainCountWidget.exec() == QDialog.Accepted:
            resultValue = int(editTrainCountWidget.lineEdit.text())
            if not self.decryptFile.saveTrainCnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I72"])
            self.reloadFunc()


class EditTrainCountWidget(QDialog):
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
        rx = QRegularExpression(r"^\d+$")
        validator = QRegularExpressionValidator(rx, self)
        self.lineEdit.setValidator(validator)
        self.lineEdit.setText("{0}".format(self.decryptFile.trainCnt))
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
        if resultValue < self.decryptFile.trainCnt:
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
