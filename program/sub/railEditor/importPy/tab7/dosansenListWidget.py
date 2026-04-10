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


class DosansenListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.dosansenList = decryptFile.dosansenList
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 5, 5, 5)
        # mainLayout - QGroupBox
        mainGroupBox = QGroupBox(textSetting.textList["railEditor"]["dosansenInfoLabel"])
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - QGroupBox - QVBoxLayout
        scrollBoxLayout = QVBoxLayout()
        scrollBoxLayout.setContentsMargins(0, 0, 0, 0)
        mainGroupBox.setLayout(scrollBoxLayout)
        # mainLayout - QGroupBox - QVBoxLayout - QScrollArea
        contentScrollArea = QScrollArea()
        contentScrollArea.setWidgetResizable(True)
        scrollBoxLayout.addWidget(contentScrollArea)
        # mainLayout - QGroupBox - QVBoxLayout - QScrollArea - QFrame
        contentFrame = QFrame()
        contentScrollArea.setWidget(contentFrame)

        # dosanInfoLayout
        dosanInfoLayout = QVBoxLayout()
        contentFrame.setLayout(dosanInfoLayout)
        # dosanInfoLayout - dosanCountGridLayout
        dosanCountGridLayout = QGridLayout()
        dosanCountGridLayout.setSpacing(0)
        dosanCountGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        dosanInfoLayout.addLayout(dosanCountGridLayout)
        # dosanInfoLayout - dosanCountGridLayout - dosanCountNameLabel
        dosanCountNameLabel = QLabel(textSetting.textList["railEditor"]["dosansenCntLabel"], font=font6)
        dosanCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        dosanCountNameLabel.setFixedSize(fixedWidth * 2, fixedHeight)
        dosanCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dosanCountGridLayout.addWidget(dosanCountNameLabel, 0, 0)
        # dosanInfoLayout - dosanCountGridLayout - dosanCountLabel
        dosanCountLabel = QLabel("{0}".format(len(self.dosansenList)), font=font6)
        dosanCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        dosanCountLabel.setFixedSize(fixedWidth, fixedHeight)
        dosanCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dosanCountGridLayout.addWidget(dosanCountLabel, 0, 1)
        # dosanInfoLayout - dosanCountGridLayout - dosanCountButton
        dosanCountButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
        dosanCountButton.clicked.connect(self.editDosansenCnt)
        dosanCountGridLayout.addWidget(dosanCountButton, 0, 2)

        for i, dosansenInfo in enumerate(self.dosansenList):
            # dosanInfoLayout - dosanInfoGridLayout
            dosanInfoGridLayout = QGridLayout()
            dosanInfoGridLayout.setSpacing(0)
            dosanInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            dosanInfoLayout.addLayout(dosanInfoGridLayout)
            # dosanInfoLayout - dosanInfoGridLayout - dosanInfoModifyButton
            dosanInfoModifyButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            dosanInfoModifyButton.setEnabled(True)
            dosanInfoModifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            dosanInfoModifyButton.clicked.connect(partial(self.editDosansenList, i, dosansenInfo))
            dosanInfoGridLayout.addWidget(dosanInfoModifyButton, 0, 0)
            # dosanInfoLayout - dosanInfoGridLayout - startLabel
            startLabel = QLabel(textSetting.textList["railEditor"]["dosansenStart"], font=font6)
            startLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            startLabel.setFixedSize(fixedWidth, fixedHeight)
            startLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(startLabel, 0, 1)
            # dosanInfoLayout - dosanInfoGridLayout - endLabel
            endLabel = QLabel(textSetting.textList["railEditor"]["dosansenEnd"], font=font6)
            endLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            endLabel.setFixedSize(fixedWidth, fixedHeight)
            endLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(endLabel, 1, 1)
            # dosanInfoLayout - dosanInfoGridLayout - e1Label
            e1Label = QLabel(textSetting.textList["railEditor"]["dosansenE1"], font=font6)
            e1Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            e1Label.setFixedSize(fixedWidth, fixedHeight)
            e1Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(e1Label, 2, 1)
            # dosanInfoLayout - dosanInfoGridLayout - animeLabel
            animeLabel = QLabel(textSetting.textList["railEditor"]["dosansenAnime"], font=font6)
            animeLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            animeLabel.setFixedSize(fixedWidth, fixedHeight)
            animeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(animeLabel, 3, 1)
            # dosanInfoLayout - dosanInfoGridLayout - e2Label
            e2Label = QLabel(textSetting.textList["railEditor"]["dosansenE2"], font=font6)
            e2Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            e2Label.setFixedSize(fixedWidth, fixedHeight)
            e2Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(e2Label, 4, 1)
            # dosanInfoLayout - dosanInfoGridLayout - f1Label
            f1Label = QLabel(textSetting.textList["railEditor"]["dosansenF1"], font=font6)
            f1Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            f1Label.setFixedSize(fixedWidth, fixedHeight)
            f1Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dosanInfoGridLayout.addWidget(f1Label, 5, 1)

            for j, dosansenValue in enumerate(dosansenInfo):
                # dosanInfoLayout - dosanInfoGridLayout - dosanLabel
                dosanLabel = QLabel("", font=font6)
                dosanLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                dosanLabel.setFixedSize(fixedWidth, fixedHeight)
                dosanLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                # start
                if j in [0, 1, 2]:
                    dosanLabel.setText("{0}".format(dosansenValue))
                    dosanInfoGridLayout.addWidget(dosanLabel, 0, 2 + j)
                # end
                elif j in [3, 4, 5]:
                    dosanLabel.setText("{0}".format(dosansenValue))
                    dosanInfoGridLayout.addWidget(dosanLabel, 1, j - 1)
                # e1
                elif j == 6:
                    dosanLabel.setText("{0}".format(dosansenValue))
                    dosanInfoGridLayout.addWidget(dosanLabel, 2, j - 4)
                # anime
                elif j in [7, 8, 9, 10]:
                    dosanLabel.setText("{0}".format(round(float(dosansenValue), 3)))
                    dosanInfoGridLayout.addWidget(dosanLabel, 3, j - 5)
                # e2
                elif j == 11:
                    dosanLabel.setText("{0}".format(dosansenValue))
                    dosanInfoGridLayout.addWidget(dosanLabel, 4, j - 9)
                # f1
                elif j == 12:
                    dosanLabel.setText("{0}".format(round(float(dosansenValue), 3)))
                    dosanInfoGridLayout.addWidget(dosanLabel, 5, j - 10)
        dosanInfoLayout.addStretch()

    def editDosansenCnt(self):
        editDosansenCountWidget = EditDosansenCountWidget(self, textSetting.textList["railEditor"]["editDosansenCntLabel"], self.decryptFile)
        if editDosansenCountWidget.exec() == QDialog.Accepted:
            resultValue = int(editDosansenCountWidget.lineEdit.text())
            if not self.decryptFile.saveDosansenCnt(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I86"])
            self.reloadFunc()

    def editDosansenList(self, i, valList):
        editDosansenWidget = EditDosansenWidget(self, textSetting.textList["railEditor"]["editDosansenInfoLabel"], self.decryptFile, valList)
        if editDosansenWidget.exec() == QDialog.Accepted:
            self.dosansenList[i] = editDosansenWidget.resultValueList
            if not self.decryptFile.saveDosansenList(self.dosansenList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["error"], message=textSetting.textList["infoList"]["I87"])
            self.reloadFunc()


class EditDosansenCountWidget(QDialog):
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
        self.lineEdit.setText("{0}".format(len(decryptFile.dosansenList)))
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
        if resultValue < len(self.decryptFile.dosansenList):
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


class EditDosansenWidget(QDialog):
    def __init__(self, parent, title, decryptFile, dosansenInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.dosansenInfo = dosansenInfo
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
        self.dosansenInfoGridLayout = QGridLayout()
        layout.addLayout(self.dosansenInfoGridLayout)
        self.lineEditList = []
        dosansenInfoLabelList = textSetting.textList["railEditor"]["editDosansenLabelList"]
        for i, dosansenInfoLabel in enumerate(dosansenInfoLabelList):
            # layout - QGridLayout - dosanLabel
            dosanLabel = QLabel(dosansenInfoLabel, font=font2)
            self.dosansenInfoGridLayout.addWidget(dosanLabel, i, 0)
            # layout - QGridLayout - dosanLineEdit
            dosanLineEdit = QLineEdit(font=font2)
            if i in [7, 8, 9, 10, 12]:
                lineEditValue = round(float(self.dosansenInfo[i]), 3)
                dosanLineEdit.setValidator(numberValidator)
            else:
                lineEditValue = self.dosansenInfo[i]
                dosanLineEdit.setValidator(integerValidator)
            dosanLineEdit.setText("{0}".format(lineEditValue))
            self.lineEditList.append(dosanLineEdit)
            self.dosansenInfoGridLayout.addWidget(dosanLineEdit, i, 1)

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
            if i in [7, 8, 9, 10, 12]:
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
