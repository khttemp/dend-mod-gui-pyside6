import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout,
    QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class ComicScriptWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.comicScriptList = decryptFile.comicScriptList
        self.reloadFunc = reloadFunc

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(5, 5, 0, 5)
        # mainLayout - QGroupBox
        mainGroupBox = QGroupBox(textSetting.textList["railEditor"]["comicScriptLabel"])
        mainLayout.addWidget(mainGroupBox)
        # mainLayout - QGroupBox - comicScriptListLayout
        comicScriptListLayout = QVBoxLayout()
        mainGroupBox.setLayout(comicScriptListLayout)
        # mainLayout - QGroupBox - comicScriptListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        comicScriptListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - comicScriptListLayout - buttonLayout - modifyButton
        self.modifyButton = QPushButton(textSetting.textList["modify"], font=font6)
        self.modifyButton.setEnabled(False)
        self.modifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.modifyButton.clicked.connect(self.modifyFunc)
        buttonLayout.addWidget(self.modifyButton)
        # layout - buttonLayout - insertButton
        self.insertButton = QPushButton(textSetting.textList["insert"], font=font6)
        self.insertButton.setEnabled(False)
        self.insertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.insertButton.clicked.connect(self.insertFunc)
        buttonLayout.addWidget(self.insertButton)
        # layout - buttonLayout - deleteButton
        self.deleteButton = QPushButton(textSetting.textList["delete"], font=font6)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.clicked.connect(self.deleteFunc)
        buttonLayout.addWidget(self.deleteButton)

        # mainLayout - QGroupBox - comicScriptListLayout - QListWidget
        self.comicScriptListListWidget = QListWidget(font=font2)
        displayComicScriptList = self.setListboxInfo(self.comicScriptList)
        self.comicScriptListListWidget.addItems(displayComicScriptList)
        self.comicScriptListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        comicScriptListLayout.addWidget(self.comicScriptListListWidget, stretch=1)

    def setListboxInfo(self, comicScriptList):
        displayComicScriptList = []
        if len(comicScriptList) > 0:
            for i in range(len(comicScriptList)):
                comicScriptInfo = comicScriptList[i]
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}]".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2]))
                elif self.decryptFile.game == "LS":
                    comicScriptTempList = [round(x, 3) for x in comicScriptInfo[3]]
                    displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptTempList))
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        comicScriptTempList = [round(x, 3) for x in comicScriptInfo[3]]
                        displayComicScriptList.append("{0:02d}→{1}, [{2}, {3}], {4}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptInfo[2], comicScriptTempList))
                    else:
                        comicScriptTempList = [round(x, 3) for x in comicScriptInfo[2]]
                        displayComicScriptList.append("{0:02d}→{1}, [{2}], {3}".format(i, comicScriptInfo[0], comicScriptInfo[1], comicScriptTempList))
        else:
            displayComicScriptList = [textSetting.textList["railEditor"]["noList"]]
        return displayComicScriptList

    def onItemClicked(self, item):
        if self.decryptFile.game == "LSTrial":
            if not (self.decryptFile.readFlag or self.decryptFile.filenameNum == 7):
                self.modifyButton.setEnabled(False)
                self.insertButton.setEnabled(False)
                self.deleteButton.setEnabled(False)
                return

        self.selectIndex = self.comicScriptListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["railEditor"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.comicScriptList[self.selectIndex]
        editComicScriptListWidget = EditComicScriptListWidget(self, textSetting.textList["railEditor"]["modifyComicScriptLabel"], self.decryptFile, "modify", item)
        if editComicScriptListWidget.exec() == QDialog.Accepted:
            self.comicScriptList[self.selectIndex] = editComicScriptListWidget.resultValueList
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()

    def insertFunc(self):
        editComicScriptListWidget = EditComicScriptListWidget(self, textSetting.textList["railEditor"]["insertComicScriptLabel"], self.decryptFile, "insert")
        if editComicScriptListWidget.exec() == QDialog.Accepted:
            self.comicScriptList.insert(self.selectIndex + editComicScriptListWidget.insertPos, editComicScriptListWidget.resultValueList)
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.comicScriptList.pop(self.selectIndex)
            if not self.decryptFile.saveComicScriptList(self.comicScriptList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I85"])
            self.reloadFunc()


class EditComicScriptListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        allIntegerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        self.insertPos = None
        self.resultValueList = []

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.comicScriptInfoGridLayout = QGridLayout()
        layout.addLayout(self.comicScriptInfoGridLayout)
        self.lineEditList = []

        comicScriptLabelList = copy.deepcopy(textSetting.textList["railEditor"]["editComicScriptLabelList"])
        if self.decryptFile.game == "LSTrial" and self.decryptFile.filenameNum == 7:
            comicScriptLabelList.pop()

        for i, comicScriptLabelValue in enumerate(comicScriptLabelList):
            # layout - QGridLayout - label
            comicScriptNameLabel = QLabel(comicScriptLabelValue, font=self.font2)
            self.comicScriptInfoGridLayout.addWidget(comicScriptNameLabel, i, 0)
            # layout - QGridLayout - LineEdit
            comicScriptLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(comicScriptLineEdit)
            if i > 1:
                comicScriptLineEdit.setValidator(allIntegerValidator)
            else:
                comicScriptLineEdit.setValidator(integerValidator)
            self.comicScriptInfoGridLayout.addWidget(comicScriptLineEdit, i, 1)

            if self.mode == "modify":
                comicScriptLineEdit.setText("{0}".format(item[i]))

        if self.decryptFile.game in ["LS", "LSTrial"]:
            horizentalLine = QFrame()
            horizentalLine.setFrameShape(QFrame.Shape.HLine)
            horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
            self.comicScriptInfoGridLayout.addWidget(horizentalLine, len(comicScriptLabelList), 0, 1, 2)

            for i in range(9):
                comicScriptTempListNameLabel = QLabel(textSetting.textList["railEditor"]["editLsComicScriptFLabel"].format(i + 1), font=self.font2)
                self.comicScriptInfoGridLayout.addWidget(comicScriptTempListNameLabel, len(comicScriptLabelList) + i + 1, 0)
                comicScriptTempListLineEdit = QLineEdit(font=self.font2)
                self.lineEditList.append(comicScriptTempListLineEdit)
                comicScriptTempListLineEdit.setValidator(numberValidator)
                self.comicScriptInfoGridLayout.addWidget(comicScriptTempListLineEdit, len(comicScriptLabelList) + i + 1, 1)

                if self.mode == "modify":
                    if self.decryptFile.game == "LSTrial" and self.decryptFile.filenameNum == 7:
                        comicScriptTempListLineEdit.setText("{0}".format(round(float(item[2][i]), 3)))
                    else:
                        comicScriptTempListLineEdit.setText("{0}".format(round(float(item[3][i]), 3)))

        if self.mode == "insert":
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.setInsertWidget(len(comicScriptLabelList))
            else:
                self.setInsertWidget(len(comicScriptLabelList) + 10)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.comicScriptInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.comicScriptInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.comicScriptInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        tempList = []
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game == "LS":
                if i in [0, 1, 2]:
                    self.resultValueList.append(int(lineEdit.text()))
                else:
                    tempList.append(float(lineEdit.text()))
            elif self.decryptFile.game == "LSTrial":
                if self.decryptFile.readFlag:
                    if i in [0, 1, 2]:
                        res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    else:
                        tempList.append(float(lineEdit.text()))
                else:
                    if i in [0, 1]:
                        res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    else:
                        tempList.append(float(lineEdit.text()))
        if len(tempList) > 0:
            self.resultValueList.append(tempList)

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
