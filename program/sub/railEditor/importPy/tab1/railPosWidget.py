from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QGroupBox, QFrame, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class RailPosWidget(QWidget):
    def __init__(self, title, num, decryptFile, trainList, reloadFunc):
        super().__init__()
        self.title = title
        self.num = num
        self.decryptFile = decryptFile
        self.trainList = trainList
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        railPosGroupBox = QGroupBox(title)
        railPosGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(railPosGroupBox)
        # mainLayout - QGroupBox - QGridLayout
        railPosGridLayout = QGridLayout()
        railPosGridLayout.setSpacing(0)
        railPosGridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        railPosGroupBox.setLayout(railPosGridLayout)

        # mainLayout - QGroupBox - QGridLayout - playerHeaderLabel
        playerHeaderLabel = QLabel(textSetting.textList["railEditor"]["railPosPlayerLabel"], font=font6)
        playerHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        playerHeaderLabel.setFixedSize(fixedWidth, fixedHeight)
        playerHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railPosGridLayout.addWidget(playerHeaderLabel, 0, 0)
        # mainLayout - QGroupBox - QGridLayout - railNoHeaderLabel
        railNoHeaderLabel = QLabel(textSetting.textList["railEditor"]["railPosRailNoLabel"], font=font6)
        railNoHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        railNoHeaderLabel.setFixedSize(fixedWidth, fixedHeight)
        railNoHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railPosGridLayout.addWidget(railNoHeaderLabel, 0, 1)
        # mainLayout - QGroupBox - QGridLayout - railPosHeaderLabel
        railPosHeaderLabel = QLabel(textSetting.textList["railEditor"]["railPosRailPosLabel"], font=font6)
        railPosHeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        railPosHeaderLabel.setFixedSize(fixedWidth, fixedHeight)
        railPosHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railPosGridLayout.addWidget(railPosHeaderLabel, 0, 2)
        # mainLayout - QGroupBox - QGridLayout - b1HeaderLabel
        b1HeaderLabel = QLabel(textSetting.textList["railEditor"]["railPosB1Label"], font=font6)
        b1HeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        b1HeaderLabel.setFixedSize(fixedWidth - 20, fixedHeight)
        b1HeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railPosGridLayout.addWidget(b1HeaderLabel, 0, 3)

        if not (self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag):
            # mainLayout - QGroupBox - QGridLayout - b1HeaderLabel
            f1HeaderLabel = QLabel(textSetting.textList["railEditor"]["railPosF1Label"], font=font6)
            f1HeaderLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            f1HeaderLabel.setFixedSize(fixedWidth - 20, fixedHeight)
            f1HeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            railPosGridLayout.addWidget(f1HeaderLabel, 0, 4)

        for i, trainInfo in enumerate(self.trainList):
            # mainLayout - QGroupBox - QGridLayout - playerLabel
            playerLabel = QLabel(textSetting.textList["railEditor"]["railPosPlayerNameLabel"].format(i + 1), font=font6)
            playerLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            playerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            railPosGridLayout.addWidget(playerLabel, i + 1, 0)
            for j in range(len(trainInfo)):
                # mainLayout - QGroupBox - QGridLayout - valueLabel
                if j == 3:
                    trainValue = round(float(trainInfo[j]), 3)
                else:
                    trainValue = trainInfo[j]
                valueLabel = QLabel("{0}".format(trainValue), font=font6)
                valueLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                railPosGridLayout.addWidget(valueLabel, i + 1, j + 1)

            if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag and i == 2:
                continue
            # mainLayout - QGroupBox - QGridLayout - railPosButton
            railPosButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
            railPosButton.clicked.connect(partial(self.editVar, i, trainInfo))
            railPosGridLayout.addWidget(railPosButton, i + 1, len(trainInfo) + 1)

    def editVar(self, i, trainInfo):
        editRailPosWidget = EditRailPosWidget(self, self.title + textSetting.textList["railEditor"]["commonModifyLabel"], self.decryptFile, trainInfo)
        if editRailPosWidget.exec() == QDialog.Accepted:
            self.trainList[i] = editRailPosWidget.resultValueList
            if not self.decryptFile.saveRailPos(self.num, self.trainList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=self.title + textSetting.textList["infoList"]["I61"])
            self.reloadFunc()


class EditRailPosWidget(QDialog):
    def __init__(self, parent, title, decryptFile, trainInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.trainInfo = trainInfo
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.railPosGridLayout = QGridLayout()
        layout.addLayout(self.railPosGridLayout)
        self.lineEditList = []
        railPosLabelList = textSetting.textList["railEditor"]["editRailPosLabelList"]
        for i, trainValue in enumerate(self.trainInfo):
            # layout - QGridLayout - railLabel
            railLabel = QLabel(railPosLabelList[i], font=font2)
            self.railPosGridLayout.addWidget(railLabel, i, 0)
            # layout - QGridLayout - railLineEdit
            railLineEdit = QLineEdit(font=font2)
            if i == 3:
                trainValue = round(float(trainValue), 3)
                railLineEdit.setValidator(numberValidator)
            else:
                railLineEdit.setValidator(integerValidator)
            railLineEdit.setText("{0}".format(trainValue))
            self.lineEditList.append(railLineEdit)
            self.railPosGridLayout.addWidget(railLineEdit, i, 1)

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
            if i == 3:
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
