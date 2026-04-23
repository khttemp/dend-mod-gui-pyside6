import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QPushButton, QDialog,
    QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class CountWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget
        fixedWidth = 86
        fixedHeight = 32
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        modelInfo = self.decryptFile.trainModelList[trainIndex]

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # henseiCountNameLabel
        henseiCountNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvOrgNumTitle"], font=self.font2)
        henseiCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        henseiCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        henseiCountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(henseiCountNameLabel, 0, 0)
        # henseiCountLabel
        self.henseiCount = modelInfo["mdlCnt"]
        henseiCountLabel = QLabel("{0}".format(self.henseiCount), font=self.font2)
        henseiCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        henseiCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        henseiCountLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(henseiCountLabel, 0, 1)
        # henseiCountButton
        henseiCountButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=self.font2)
        henseiCountButton.clicked.connect(self.editHenseiVar)
        mainLayout.addWidget(henseiCountButton, 0, 2)

        # colorCountNameLabel
        colorCountNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["colorCnt"], font=self.font2)
        colorCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        colorCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colorCountNameLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(colorCountNameLabel, 1, 0)
        # colorCountLabel
        self.colorCount = modelInfo["colorCnt"]
        colorCountLabel = QLabel("{0}".format(self.colorCount), font=self.font2)
        colorCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        colorCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colorCountLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(colorCountLabel, 1, 1)
        if decryptFile.game in ["CS", "RS"]:
            # colorCountButton
            colorCountButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=self.font2)
            colorCountButton.clicked.connect(self.editColorCountVar)
            mainLayout.addWidget(colorCountButton, 1, 2)

    def editHenseiVar(self):
        editHenseiCountDialog = EditHenseiCountDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.trainIndex, self.henseiCount, self.decryptFile)
        if editHenseiCountDialog.exec() == QDialog.Accepted:
            self.reloadWidget()

    def editColorCountVar(self, value):
        editColorCountDialog = EditColorCountDialog(self, textSetting.textList["orgInfoEditor"]["valueModify"], self.trainIndex, self.colorCount, self.decryptFile)
        if editColorCountDialog.exec() == QDialog.Accepted:
            self.reloadWidget()


class EditHenseiCountDialog(QDialog):
    def __init__(self, parent, title, trainIndex, henseiCount, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.henseiCount = henseiCount
        self.decryptFile = decryptFile
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        self.lineEdit.setText("{0}".format(self.henseiCount))
        self.lineEdit.setValidator(integerValidator)
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

        resultValue = int(self.lineEdit.text())
        if resultValue <= 0:
            errorMsg = textSetting.textList["errorList"]["E61"].format(1)
            mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
            return

        if resultValue < self.henseiCount:
            msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
            if result != mb.OK:
                return

        if not self.decryptFile.saveHenseiNum(self.trainIndex, resultValue):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return False
        return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])


class EditColorCountDialog(QDialog):
    def __init__(self, parent, title, trainIndex, colorCount, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        self.lineEdit.setText("{0}".format(colorCount))
        self.lineEdit.setValidator(integerValidator)
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

        resultValue = int(self.lineEdit.text())
        if not self.decryptFile.saveColor(self.trainIndex, resultValue):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return False
        return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I56"])
