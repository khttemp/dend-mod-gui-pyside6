import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox, QGroupBox,
    QHBoxLayout, QListWidget, QComboBox, QFrame, QGridLayout,
    QLineEdit, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtGui import QFont

mb = customMessageBoxWidget.CustomMessageBox()


class SimpleListWidget(QWidget):
    def __init__(self, groupBoxTitle, decryptFile, simpleList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.decryptFile = decryptFile
        self.simpleList = copy.deepcopy(simpleList)
        self.dirtyFlag = False

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
                displaySimpleList.append(simpleList[i])
        else:
            displaySimpleList = [textSetting.textList["orgInfoEditor"]["noList"]]
        return displaySimpleList

    def onItemClicked(self, item):
        self.selectIndex = self.simpleListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["orgInfoEditor"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.simpleList[self.selectIndex]
        editSimpleListWidget = EditSimpleListWidget(self, self.groupBoxTitle + textSetting.textList["orgInfoEditor"]["commonModifyLabel"], self.decryptFile, "modify", item)
        if editSimpleListWidget.exec() == QDialog.Accepted:
            self.simpleList[self.selectIndex] = editSimpleListWidget.simpleInfoLineEdit.text()
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.simpleListListWidget.clear()
            self.simpleListListWidget.addItems(displaySimpleList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editSimpleListWidget = EditSimpleListWidget(self, self.groupBoxTitle + textSetting.textList["orgInfoEditor"]["commonInsertLabel"], self.decryptFile, "insert")
        if editSimpleListWidget.exec() == QDialog.Accepted:
            self.simpleList.insert(self.selectIndex + editSimpleListWidget.insertPos, editSimpleListWidget.simpleInfoLineEdit.text())
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.simpleListListWidget.clear()
            self.simpleListListWidget.addItems(displaySimpleList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.simpleList.pop(self.selectIndex)
            displaySimpleList = self.setListboxInfo(self.simpleList)
            self.simpleListListWidget.clear()
            self.simpleListListWidget.addItems(displaySimpleList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditSimpleListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.simpleInfoGridLayout = QGridLayout()
        layout.addLayout(self.simpleInfoGridLayout)
        # layout - QGridLayout - LineEdit
        self.simpleInfoLineEdit = QLineEdit(font=self.font2)
        self.simpleInfoGridLayout.addWidget(self.simpleInfoLineEdit, 0, 0, 1, 2)

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
        insertLabel = QLabel(textSetting.textList["orgInfoEditor"]["posLabel"], font=self.font2)
        self.simpleInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["orgInfoEditor"]["posValue"])
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


class EditModelWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - editModelButton
        editModelButton = QPushButton(textSetting.textList["orgInfoEditor"]["modelInfoModify"])
        editModelButton.clicked.connect(self.editModel)
        mainLayout.addWidget(editModelButton)

    def editModel(self):
        editModelDialog = EditModelDialog(self, textSetting.textList["orgInfoEditor"]["editModelLabel"], self.trainIndex, self.decryptFile)
        if editModelDialog.exec() == QDialog.Accepted:
            self.reloadWidget()


class EditModelDialog(QDialog):
    def __init__(self, parent, title, trainIndex, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        modelInfo = self.decryptFile.trainModelList[trainIndex]

        # layout
        layout = QVBoxLayout(self)
        # listLayout
        listLayout = QGridLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(listLayout)
        noText = textSetting.textList["orgInfoEditor"]["noList"]
        # listLayout - trackModelList
        self.trackModelSimpleList = SimpleListWidget(textSetting.textList["orgInfoEditor"]["csvDaishaTitle"], decryptFile, modelInfo["trackNames"])
        listLayout.addWidget(self.trackModelSimpleList, 0, 0)
        # LS、BSの場合、台車の数は変更不可
        if self.decryptFile.game in ["LS", "BS"]:
            self.trackModelSimpleList.insertButton.hide()
            self.trackModelSimpleList.deleteButton.hide()
        # listLayout - trainModelList
        trainModelList = copy.deepcopy(modelInfo["mdlNames"])
        if noText in trainModelList:
            noIndex = trainModelList.index(noText)
            trainModelList.pop(noIndex)
        self.trainModelSimpleList = SimpleListWidget(textSetting.textList["orgInfoEditor"]["csvMdlTitle"], decryptFile, trainModelList)
        listLayout.addWidget(self.trainModelSimpleList, 0, 1)
        # LSの場合、モデルの数は変更不可
        if self.decryptFile.game == "LS":
            self.trainModelSimpleList.insertButton.hide()
            self.trainModelSimpleList.deleteButton.hide()

        # listLayout - pantaModelList
        pantaModelList = copy.deepcopy(modelInfo["pantaNames"])
        if noText in pantaModelList:
            noIndex = pantaModelList.index(noText)
            pantaModelList.pop(noIndex)
        self.pantaModelSimpleList = SimpleListWidget(textSetting.textList["orgInfoEditor"]["csvPantaTitle"], decryptFile, pantaModelList)
        listLayout.addWidget(self.pantaModelSimpleList, 1, 0)
        # listLayout - colModelList
        colModelList = copy.deepcopy(modelInfo["colNames"])
        if noText in colModelList:
            noIndex = colModelList.index(noText)
            colModelList.pop(noIndex)
        self.colModelSimpleList = SimpleListWidget(textSetting.textList["orgInfoEditor"]["csvColTitle"], decryptFile, colModelList)
        listLayout.addWidget(self.colModelSimpleList, 1, 1)
        # LSの場合、COLの数は変更不可
        if self.decryptFile.game == "LS":
            self.colModelSimpleList.insertButton.hide()
            self.colModelSimpleList.deleteButton.hide()

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        modelInfo = self.decryptFile.trainModelList[self.trainIndex]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I63"], icon="warning")
        if result == mb.OK:
            newTrackList = []
            for i in range(self.trackModelSimpleList.simpleListListWidget.count()):
                item = self.trackModelSimpleList.simpleListListWidget.item(i)
                if item.text() == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
            newTrackList.append(item.text())
            trackModelCount = len(newTrackList)

            newTrainList = []
            for i in range(self.trainModelSimpleList.simpleListListWidget.count()):
                item = self.trainModelSimpleList.simpleListListWidget.item(i)
                if item.text() == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
                newTrainList.append(item.text())
            trainModelCount = len(newTrainList)

            newPantaList = []
            for i in range(self.pantaModelSimpleList.simpleListListWidget.count()):
                item = self.pantaModelSimpleList.simpleListListWidget.item(i)
                if item.text() == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
                newPantaList.append(item.text())
            pantaModelCount = len(newPantaList)

            newColList = []
            for i in range(self.colModelSimpleList.simpleListListWidget.count()):
                item = self.colModelSimpleList.simpleListListWidget.item(i)
                if item.text() == textSetting.textList["orgInfoEditor"]["noList"]:
                    continue
                newColList.append(item.text())
            colModelCount = len(newColList)

            if self.trackModelSimpleList.dirtyFlag:
                if self.decryptFile.game in ["LS", "BS"]:
                    if trackModelCount <= 1:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(1))
                        return
                elif self.decryptFile.game in ["CS", "RS"]:
                    if trackModelCount <= 2:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(2))
                        return

            if self.trainModelSimpleList.dirtyFlag:
                trainModelText = textSetting.textList["orgInfoEditor"]["csvMdlTitle"]
                trainModelIndexList = modelInfo["mdlList"]
                if self.decryptFile.game in ["BS", "CS"]:
                    if trainModelCount != colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E136"])
                        return
                if trainModelCount == 0:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(trainModelText))
                    return
                for trainModelIndex in trainModelIndexList:
                    if trainModelIndex != -1 and trainModelIndex >= trainModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(trainModelText, trainModelIndex))
                        return

            if self.pantaModelSimpleList.dirtyFlag:
                pantaModelText = textSetting.textList["orgInfoEditor"]["csvPantaTitle"]
                pantaModelIndexList = modelInfo["pantaList"]
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    if pantaModelCount == 0:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(pantaModelText))
                        return
                if pantaModelCount > 0:
                    for pantaModelIndex in pantaModelIndexList:
                        if pantaModelIndex != -1 and pantaModelIndex >= pantaModelCount:
                            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(pantaModelText, pantaModelIndex))
                            return

            if self.colModelSimpleList.dirtyFlag:
                colModelText = textSetting.textList["orgInfoEditor"]["csvColTitle"]
                colModelIndexList = modelInfo["colList"]
                if self.decryptFile.game in ["BS", "CS"]:
                    if trainModelCount != colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E136"])
                        return
                if colModelCount == 0:
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E137"].format(colModelText))
                    return
                for colModelIndex in colModelIndexList:
                    if colModelIndex != -1 and colModelIndex >= colModelCount:
                        mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(colModelText, colModelIndex))
                        return

            modelInfo["trackNames"] = newTrackList
            modelInfo["mdlNames"] = newTrainList

            newPantaList.append(textSetting.textList["orgInfoEditor"]["noList"])
            modelInfo["pantaNames"] = newPantaList
            if pantaModelCount == 0:
                if len(modelInfo["pantaList"]) > 0:
                    modelInfo["pantaList"] = []
            else:
                if len(modelInfo["pantaList"]) == 0:
                    modelInfo["pantaList"] = [-1]*len(modelInfo["mdlList"])
            modelInfo["colNames"] = newColList

            if not self.decryptFile.saveModelInfo(self.trainIndex, modelInfo):
                self.decryptFile.printError()
                errorMsg = textSetting.textList["errorList"]["E4"]
                mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
                return
            return True

    def accept(self):
        ret = False
        ret |= self.trackModelSimpleList.dirtyFlag
        ret |= self.trainModelSimpleList.dirtyFlag
        ret |= self.pantaModelSimpleList.dirtyFlag
        ret |= self.colModelSimpleList.dirtyFlag

        if ret:
            if not self.validate():
                return
            super().accept()
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I64"])
        else:
            super().accept()
