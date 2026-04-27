from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea,
    QFrame, QGridLayout, QLabel, QPushButton, QDialog,
    QLineEdit, QDialogButtonBox
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class TailListWidget(QWidget):
    def __init__(self, decryptFile, trainIndex, reloadWidget):
        super().__init__()
        self.decryptFile = decryptFile
        self.trainIndex = trainIndex
        tailList = decryptFile.trainModelList[trainIndex]["tailList"]
        self.tailSmfList = tailList[0]
        self.tailElseList = tailList[1]
        self.lensList = tailList[2]
        self.reloadWidget = reloadWidget
        fixedWidth = 86
        fixedHeight = 36
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - tailListGroupBox
        tailListGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["tailInfoLabel"])
        mainLayout.addWidget(tailListGroupBox)
        # groupInLayout
        groupInLayout = QVBoxLayout()
        groupInLayout.setContentsMargins(0, 0, 0, 0)
        groupInLayout.setSpacing(0)
        tailListGroupBox.setLayout(groupInLayout)
        # groupInLayout - scrollArea
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        groupInLayout.addWidget(scrollArea)
        # groupInLayout - scrollArea - QFrame
        scrollAreaFrame = QFrame()
        scrollArea.setWidget(scrollAreaFrame)
        # groupInLayout - scrollArea - QFrame - QVBoxLayout
        contentLayout = QVBoxLayout()
        scrollAreaFrame.setLayout(contentLayout)

        # tailCountLayout
        tailCountLayout = QHBoxLayout()
        contentLayout.addLayout(tailCountLayout)
        # tailCountGridLayout
        tailCountGridLayout = QGridLayout()
        tailCountGridLayout.setContentsMargins(0, 0, 0, 0)
        tailCountGridLayout.setSpacing(0)
        tailCountLayout.addLayout(tailCountGridLayout)
        # tailCountGridLayout - tailCountNameLabel
        tailCountNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["tailCntLabel"], font=font6)
        tailCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tailCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tailCountGridLayout.addWidget(tailCountNameLabel, 0, 0)
        # tailCountLabel
        tailCountLabel = QLabel("{0}".format(len(self.tailSmfList)), font=font6)
        tailCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tailCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tailCountLabel.setFixedWidth(fixedWidth)
        tailCountGridLayout.addWidget(tailCountLabel, 0, 1)
        # tailCountButton
        tailCountButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        tailCountButton.clicked.connect(self.editTailCount)
        tailCountGridLayout.addWidget(tailCountButton, 0, 2)
        # stretch
        tailCountLayout.addStretch()

        # contentLayout - tailSmfElementLayout
        tailSmfElementLayout = QHBoxLayout()
        contentLayout.addLayout(tailSmfElementLayout)
        # contentLayout - tailSmfElementLayout - tailSmfButtonLayout
        tailSmfButtonLayout = QVBoxLayout()
        tailSmfElementLayout.addLayout(tailSmfButtonLayout)
        # contentLayout - tailElementLayout - buttonLayout - tailElementButton
        tailSmfButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        tailSmfButton.clicked.connect(partial(self.editTailSmfElse, self.tailSmfList, self.tailElseList))
        tailSmfButtonLayout.addWidget(tailSmfButton)
        # stretch
        tailSmfButtonLayout.addStretch()

        # contentLayout - tailSmfElementLayout - tailSmfNameElseLayout
        tailSmfNameElseLayout = QVBoxLayout()
        tailSmfElementLayout.addLayout(tailSmfNameElseLayout)
        # contentLayout - tailSmfElementLayout - tailSmfNameElseLayout - tailSmfNameLayout
        tailSmfNameLayout = QHBoxLayout()
        tailSmfNameElseLayout.addLayout(tailSmfNameLayout)
        # contentLayout - tailSmfElementLayout - tailSmfNameElseLayout - tailSmfNameLayout - tailSmfNameGridLayout
        tailSmfNameGridLayout = QGridLayout()
        tailSmfNameGridLayout.setContentsMargins(0, 0, 0, 0)
        tailSmfNameGridLayout.setSpacing(0)
        tailSmfNameLayout.addLayout(tailSmfNameGridLayout)
        # tailSmfNameTextLabel
        tailSmfNameTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["tailNameLabel"], font=font6)
        tailSmfNameTextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tailSmfNameTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tailSmfNameTextLabel.setFixedSize(fixedWidth, fixedHeight)
        tailSmfNameGridLayout.addWidget(tailSmfNameTextLabel, 0, 0)
        for i in range(len(self.tailSmfList)):
            # tailSmfNameLabel
            tailSmfNameLabel = QLabel("{0}".format(self.tailSmfList[i]), font=font6)
            tailSmfNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            tailSmfNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tailSmfNameLabel.setFixedHeight(fixedHeight)
            tailSmfNameGridLayout.addWidget(tailSmfNameLabel, i, 1)
        # stretch
        tailSmfNameLayout.addStretch()

        # contentLayout - tailSmfElementLayout - tailSmfNameElseLayout - tailSmfElseLayout
        tailSmfElseLayout = QHBoxLayout()
        tailSmfNameElseLayout.addLayout(tailSmfElseLayout)
        # contentLayout - tailSmfElementLayout - tailSmfNameElseLayout - tailSmfElseLayout - tailSmfNameGridLayout
        tailSmfElseGridLayout = QGridLayout()
        tailSmfElseGridLayout.setContentsMargins(0, 0, 0, 0)
        tailSmfElseGridLayout.setSpacing(0)
        tailSmfElseLayout.addLayout(tailSmfElseGridLayout)
        # tailSmfElseTextLabel
        tailSmfElseTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["tailElseLabel"], font=font6)
        tailSmfElseTextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tailSmfElseTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tailSmfElseTextLabel.setFixedSize(fixedWidth, fixedHeight)
        tailSmfElseGridLayout.addWidget(tailSmfElseTextLabel, 0, 0)
        for i in range(len(self.tailElseList)):
            # tailSmfElseLabel
            tailSmfElseLabel = QLabel("{0}".format(self.tailElseList[i]), font=font6)
            tailSmfElseLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            tailSmfElseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tailSmfElseLabel.setFixedSize(fixedWidth, fixedHeight)
            tailSmfElseGridLayout.addWidget(tailSmfElseLabel, i, 1)
        # stretch
        tailSmfElseLayout.addStretch()
        # stretch
        tailSmfNameElseLayout.addStretch()
        # stretch
        tailSmfElementLayout.addStretch()

        for i in range(len(self.lensList)):
            # contentLayout - lensElementLayout
            lensElementLayout = QHBoxLayout()
            contentLayout.addLayout(lensElementLayout)
            # contentLayout - lensElementLayout - buttonLayout
            buttonLayout = QVBoxLayout()
            lensElementLayout.addLayout(buttonLayout)
            # contentLayout - lensElementLayout - buttonLayout - lensElementButton
            lensElementButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            lensElementButton.clicked.connect(partial(self.editLensList, i))
            buttonLayout.addWidget(lensElementButton)
            # stretch
            buttonLayout.addStretch()

            # contentLayout - lensElementLayout - lensInfoLayout
            lensInfoLayout = QVBoxLayout()
            lensInfoLayout.setContentsMargins(0, 0, 0, 0)
            lensInfoLayout.setSpacing(0)
            lensElementLayout.addLayout(lensInfoLayout)
            # lensInfoLayout - nameLayout
            nameLayout = QHBoxLayout()
            lensInfoLayout.addLayout(nameLayout)
            # lensInfoLayout - nameLayout - nameInfoGridLayout
            nameInfoGridLayout = QGridLayout()
            nameInfoGridLayout.setContentsMargins(0, 0, 0, 0)
            nameInfoGridLayout.setSpacing(0)
            nameLayout.addLayout(nameInfoGridLayout)
            # nameTextLabel
            nameTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensNameLabel"], font=font6)
            nameTextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            nameTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nameTextLabel.setFixedSize(fixedWidth, fixedHeight)
            nameInfoGridLayout.addWidget(nameTextLabel, 0, 0)
            for j in range(2):
                # nameLabel
                nameLabel = QLabel("{0}".format(self.lensList[i][j]), font=font6)
                nameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                nameLabel.setFixedHeight(fixedHeight)
                nameInfoGridLayout.addWidget(nameLabel, 0, j + 1)
            # stretch
            nameLayout.addStretch()

            # elementLayout
            elementLayout = QHBoxLayout()
            lensInfoLayout.addLayout(elementLayout)
            # elementGridLayout
            elementGridLayout = QGridLayout()
            elementGridLayout.setContentsMargins(0, 0, 0, 0)
            elementGridLayout.setSpacing(0)
            elementLayout.addLayout(elementGridLayout)

            # fTextLabel
            f1TextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensF1Label"], font=font6)
            f1TextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            f1TextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f1TextLabel.setFixedSize(fixedWidth, fixedHeight)
            elementGridLayout.addWidget(f1TextLabel, 0, 0)
            for j in range(2):
                # fLabel
                fLabel = QLabel("{0}".format(round(float(self.lensList[i][j + 2]), 3)), font=font6)
                fLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                fLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                fLabel.setFixedSize(fixedWidth, fixedHeight)
                elementGridLayout.addWidget(fLabel, 0, j + 1)

            # bTestLabel
            b1TextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensB1Label"], font=font6)
            b1TextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            b1TextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b1TextLabel.setFixedSize(fixedWidth, fixedHeight)
            elementGridLayout.addWidget(b1TextLabel, 1, 0)
            for j in range(len(self.lensList[i][4])):
                # bLabel
                bLabel = QLabel("{0}".format(self.lensList[i][4][j]), font=font6)
                bLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                bLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                bLabel.setFixedSize(fixedWidth, fixedHeight)
                elementGridLayout.addWidget(bLabel, 1, j + 1)

            # stretch
            elementLayout.addStretch()
            # stretch
            lensInfoLayout.addStretch()
            # stretch
            lensElementLayout.addStretch()

        # stretch
        contentLayout.addStretch()

    def editTailCount(self):
        editTailCountWidget = EditTailCountWidget(self, textSetting.textList["orgInfoEditor"]["tailEditCntLabel"], len(self.tailSmfList))
        if editTailCountWidget.exec() == QDialog.Accepted:
            resultValue = int(editTailCountWidget.lineEdit.text())
            if not self.decryptFile.saveTailCnt(self.trainIndex, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I67"])
            self.reloadWidget()

    def editTailSmfElse(self, smfList, elseList):
        editTailSmfElseWidget = EditTailSmfElseWidget(self, textSetting.textList["orgInfoEditor"]["tailEditLabel"], smfList, elseList)
        if editTailSmfElseWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveTailSmfElse(self.trainIndex, editTailSmfElseWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I68"])
            self.reloadWidget()

    def editLensList(self, i):
        editLensWidget = EditLensWidget(self, textSetting.textList["orgInfoEditor"]["lensEditLabel"], self.lensList[i])
        if editLensWidget.exec() == QDialog.Accepted:
            self.lensList[i] = editLensWidget.resultValueList
            if not self.decryptFile.saveTailLensList(self.trainIndex, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I66"])
            self.reloadWidget()


class EditTailCountWidget(QDialog):
    def __init__(self, parent, title, val):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.val = val
        self.resultValue = None
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        self.lineEdit.setValidator(integerValidator)
        self.lineEdit.setText("{0}".format(self.val))
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
        if resultValue < self.val:
            msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
            if result == mb.OK:
                return True
        else:
            return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditTailSmfElseWidget(QDialog):
    def __init__(self, parent, title, smfList, elseList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.smfList = smfList
        self.elseList = elseList
        self.smfNameVarList = []
        self.elseVarList = []
        self.resultValueList = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        tailSmfElseGridLayout = QGridLayout()
        layout.addLayout(tailSmfElseGridLayout)
        self.lineEditList = []
        for i in range(len(self.smfList)):
            # layout - QGridLayout - smfNameLabel
            smfNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["tailSmfNameLabel"].format(i + 1), font=font2)
            tailSmfElseGridLayout.addWidget(smfNameLabel, i, 0)
            # layout - QGridLayout - smfNameLineEdit
            smfNameLineEdit = QLineEdit(font=font2)
            smfNameLineEdit.setText("{0}".format(self.smfList[i]))
            self.lineEditList.append(smfNameLineEdit)
            tailSmfElseGridLayout.addWidget(smfNameLineEdit, i, 1)

        for i in range(len(self.elseList)):
            # layout - QGridLayout - elseNameLabel
            elseNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["tailSmfElseLabel"].format(i + 1), font=font2)
            tailSmfElseGridLayout.addWidget(elseNameLabel, len(self.smfList) + i, 0)
            # layout - QGridLayout - elseNameLineEdit
            elseNameLineEdit = QLineEdit(font=font2)
            elseNameLineEdit.setValidator(integerValidator)
            elseNameLineEdit.setText("{0}".format(self.elseList[i]))
            self.lineEditList.append(elseNameLineEdit)
            tailSmfElseGridLayout.addWidget(elseNameLineEdit, len(self.smfList) + i, 1)

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
            if i < len(self.smfList):
                self.resultValueList.append(lineEdit.text())
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


class EditLensWidget(QDialog):
    def __init__(self, parent, title, lensInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.lensInfo = lensInfo
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
        lensGridLayout = QGridLayout()
        layout.addLayout(lensGridLayout)
        self.lineEditList = []
        lensInfoLbList = textSetting.textList["orgInfoEditor"]["lensInfoLabelList"]
        for i in range(len(self.lensInfo)):
            if i in [0, 1]:
                # layout - QGridLayout - lensNameLabel
                lensNameLabel = QLabel(lensInfoLbList[i], font=font2)
                lensGridLayout.addWidget(lensNameLabel, i, 0)
                # layout - QGridLayout - lensLineEdit
                lensLineEdit = QLineEdit(font=font2)
                lensLineEdit.setText("{0}".format(self.lensInfo[i]))
                self.lineEditList.append(lensLineEdit)
                lensGridLayout.addWidget(lensLineEdit, i, 1)
            elif i in [2, 3]:
                # layout - QGridLayout - lensNameLabel
                lensNameLabel = QLabel(lensInfoLbList[i], font=font2)
                lensGridLayout.addWidget(lensNameLabel, i, 0)
                # layout - QGridLayout - lensLineEdit
                lensLineEdit = QLineEdit(font=font2)
                lensLineEdit.setValidator(numberValidator)
                lensLineEdit.setText("{0}".format(round(float(self.lensInfo[i]), 3)))
                self.lineEditList.append(lensLineEdit)
                lensGridLayout.addWidget(lensLineEdit, i, 1)
            elif i == 4:
                for j in range(len(self.lensInfo[i])):
                    # layout - QGridLayout - lensNameLabel
                    lensNameLabel = QLabel(lensInfoLbList[i], font=font2)
                    lensGridLayout.addWidget(lensNameLabel, i + j, 0)
                    # layout - QGridLayout - lensLineEdit
                    lensLineEdit = QLineEdit(font=font2)
                    lensLineEdit.setValidator(integerValidator)
                    lensLineEdit.setText("{0}".format(self.lensInfo[i][j]))
                    self.lineEditList.append(lensLineEdit)
                    lensGridLayout.addWidget(lensLineEdit, i + j, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValueList = []
        varList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            if i in [0, 1]:
                self.resultValueList.append(lineEdit.text())
            if i in [2, 3]:
                self.resultValueList.append(float(lineEdit.text()))
            elif i >= 4:
                varList.append(int(lineEdit.text()))
        self.resultValueList.append(varList)
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
