import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout,
    QListWidget, QLabel, QLineEdit, QPushButton, QFrame, QComboBox,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont

mb = customMessageBoxWidget.CustomMessageBox()


class SimpleListWidget(QWidget):
    def __init__(self, groupBoxTitle, decryptFile, simpleList, index, listCntByteNum, reloadFunc):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.decryptFile = decryptFile
        self.simpleList = copy.deepcopy(simpleList)
        self.index = index
        self.listCntByteNum = listCntByteNum
        self.reloadFunc = reloadFunc

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        simpleGroupBox = QGroupBox(groupBoxTitle)
        simpleGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(simpleGroupBox)
        # mainLayout - QGroupBox - simpleListLayout
        simpleListLayout = QVBoxLayout()
        simpleGroupBox.setLayout(simpleListLayout)
        # mainLayout - QGroupBox - simpleListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        simpleListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - simpleListLayout - buttonLayout - modifyButton
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

        # mainLayout - QGroupBox - simpleListLayout - QListWidget
        self.simpleListListWidget = QListWidget(font=font2)
        displaySimpleList = self.setListboxInfo(self.simpleList)
        self.simpleListListWidget.addItems(displaySimpleList)
        self.simpleListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        simpleListLayout.addWidget(self.simpleListListWidget, stretch=1)

    def setListboxInfo(self, simpleList):
        displaySimpleList = []
        if len(simpleList) > 0:
            for i in range(len(simpleList)):
                simpleInfo = simpleList[i]
                displaySimpleList.append("{0:02d}→{1}".format(i, simpleInfo))
        else:
            displaySimpleList = [textSetting.textList["railEditor"]["noList"]]
        return displaySimpleList

    def onItemClicked(self, item):
        self.selectIndex = self.simpleListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["railEditor"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.simpleList[self.selectIndex]
        editSimpleListWidget = EditSimpleListWidget(self, self.groupBoxTitle + textSetting.textList["railEditor"]["commonModifyLabel"], self.decryptFile, "modify", item)
        if editSimpleListWidget.exec() == QDialog.Accepted:
            self.simpleList[self.selectIndex] = editSimpleListWidget.simpleInfoLineEdit.text()
            if not self.decryptFile.saveSimpleList(self.index, self.listCntByteNum, self.simpleList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=self.groupBoxTitle + textSetting.textList["infoList"]["I76"])
            self.reloadFunc()

    def insertFunc(self):
        editSimpleListWidget = EditSimpleListWidget(self, self.groupBoxTitle + textSetting.textList["railEditor"]["commonInsertLabel"], self.decryptFile, "insert")
        if editSimpleListWidget.exec() == QDialog.Accepted:
            self.simpleList.insert(self.selectIndex + editSimpleListWidget.insertPos, editSimpleListWidget.simpleInfoLineEdit.text())
            if not self.decryptFile.saveSimpleList(self.index, self.listCntByteNum, self.simpleList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=self.groupBoxTitle + textSetting.textList["infoList"]["I76"])
            self.reloadFunc()

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.simpleList.pop(self.selectIndex)
            if not self.decryptFile.saveSimpleList(self.index, self.listCntByteNum, self.simpleList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return False
            mb.showinfo(title=textSetting.textList["success"], message=self.groupBoxTitle + textSetting.textList["infoList"]["I76"])
            self.reloadFunc()


class EditSimpleListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.insertPos = -1

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.simpleInfoGridLayout = QGridLayout()
        layout.addLayout(self.simpleInfoGridLayout)
        # layout - QGridLayout - label
        simpleInfoLabel = QLabel(textSetting.textList["railEditor"]["editValueLabel"], font=self.font2)
        self.simpleInfoGridLayout.addWidget(simpleInfoLabel, 0, 0)
        # layout - QGridLayout - LineEdit
        self.simpleInfoLineEdit = QLineEdit(font=self.font2)
        self.simpleInfoGridLayout.addWidget(self.simpleInfoLineEdit, 0, 1)

        if self.mode == "modify":
            self.simpleInfoLineEdit.setText("{0}".format(item))

        if self.mode == "insert":
            self.setInsertWidget(1)

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
        self.simpleInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.simpleInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.simpleInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        if not self.simpleInfoLineEdit.text():
            mb.showerror(title=textSetting.textList["valueError"], message=textSetting.textList["infoList"]["I44"])
            return False

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
