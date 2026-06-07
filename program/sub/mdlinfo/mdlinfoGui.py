import os
import traceback

import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from program.sub.mdlinfo.dendDecrypt.decrypt import MdlDecrypt
from program.sub.mdlinfo.importPy.mdlDetailWidget import MdlDetailDialog
from program.sub.mdlinfo.importPy.smfDetailWidget import SmfDetailDialog
from program.sub.smf.dendDecrypt.decrypt import SmfDecrypt

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QComboBox, QGroupBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QDialog, QDialogButtonBox, QGridLayout,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()
errObj = ErrorLogObj()


class MdlinfoWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.selectId = None
        self.copyInfoByteArr = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font7 = QFont(textSetting.textList["font7"][0], textSetting.textList["font7"][1])
        labelHeight = 28
        buttonWidth = 200
        buttonHeight = 28

        mainLayout = QVBoxLayout(self)
        mainLayout.addSpacing(10)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 2)

        # headerLeft
        headerLeftLayout = QVBoxLayout()
        headerLeftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerLeftLayout, 3)
        # headerLeft - fileName
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedHeight(labelHeight)
        headerLeftLayout.addWidget(self.fileNameLabel)

        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerSelectLayout.setContentsMargins(0, 15, 0, 15)
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["mdlinfo"]["selectNum"], font=font2)
        selectLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

        # headerLeft - search
        headerSearchLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSearchLayout)
        # headerLeft - search - Label
        searchLabel = QLabel(textSetting.textList["mdlinfo"]["searchModel"], font=font2)
        headerSearchLayout.addWidget(searchLabel, 1)
        # headerLeft - search - LineEdit
        self.searchLineEdit = QLineEdit("", font=font7)
        self.searchLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.searchLineEdit.setReadOnly(True)
        self.searchLineEdit.textChanged.connect(self.tableFilterFunc)
        headerSearchLayout.addWidget(self.searchLineEdit, 9)

        # headerRight
        headerRightLayout = QVBoxLayout()
        headerRightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerRightLayout, 8)

        # headerRight - buttonLayout
        headerRightButtonLayout1 = QHBoxLayout()
        headerRightButtonLayout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout1)
        # headerRight - buttonLayout - button1
        self.mdlDetailButton = QPushButton(textSetting.textList["mdlinfo"]["mdlDetailLabel"])
        self.mdlDetailButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlDetailButton.setEnabled(False)
        self.mdlDetailButton.clicked.connect(self.mdlDetailFunc)
        headerRightButtonLayout1.addWidget(self.mdlDetailButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button2
        self.mdlTypeButton = QPushButton(textSetting.textList["mdlinfo"]["mdlTypeLabel"])
        self.mdlTypeButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlTypeButton.setEnabled(False)
        self.mdlTypeButton.clicked.connect(self.mdlTypeFunc)
        headerRightButtonLayout1.addWidget(self.mdlTypeButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button3
        self.mdlSmfElementButton = QPushButton(textSetting.textList["mdlinfo"]["mdlSmfEleLabel"])
        self.mdlSmfElementButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlSmfElementButton.setEnabled(False)
        self.mdlSmfElementButton.clicked.connect(self.mdlSmfElementFunc)
        headerRightButtonLayout1.addWidget(self.mdlSmfElementButton)

        # stretch
        headerRightLayout.addStretch()

        # headerRight - buttonLayout
        headerRightButtonLayout2 = QHBoxLayout()
        headerRightButtonLayout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout2)
        # headerRight - buttonLayout - button1
        self.binFileFlagButton = QPushButton(textSetting.textList["mdlinfo"]["binFileFlagLabel"])
        self.binFileFlagButton.setFixedSize(buttonWidth, buttonHeight)
        self.binFileFlagButton.setEnabled(False)
        self.binFileFlagButton.clicked.connect(self.binFileFlagFunc)
        headerRightButtonLayout2.addWidget(self.binFileFlagButton)
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout - button2
        self.copyAnotherMdlinfoButton = QPushButton(textSetting.textList["mdlinfo"]["copyAnotherMdlinfoLabel"])
        self.copyAnotherMdlinfoButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyAnotherMdlinfoButton.setEnabled(False)
        self.copyAnotherMdlinfoButton.clicked.connect(self.copyAnotherMdlinfoFunc)
        headerRightButtonLayout2.addWidget(self.copyAnotherMdlinfoButton)
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout - button3
        self.mdlinfoDeleteButton = QPushButton(textSetting.textList["mdlinfo"]["mdlinfoDeleteLabel"])
        self.mdlinfoDeleteButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlinfoDeleteButton.setEnabled(False)
        self.mdlinfoDeleteButton.clicked.connect(self.mdlinfoDeleteFunc)
        headerRightButtonLayout2.addWidget(self.mdlinfoDeleteButton)

        # stretch
        headerRightLayout.addStretch()

        # headerRight - buttonLayout
        headerRightButtonLayout3 = QHBoxLayout()
        headerRightButtonLayout3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout3)
        # headerRight - buttonLayout - button1
        self.mdlinfoCopyButton = QPushButton(textSetting.textList["mdlinfo"]["mdlinfoCopyLabel"])
        self.mdlinfoCopyButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlinfoCopyButton.setEnabled(False)
        self.mdlinfoCopyButton.clicked.connect(self.mdlinfoCopyFunc)
        headerRightButtonLayout3.addWidget(self.mdlinfoCopyButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button2
        self.mdlinfoPasteButton = QPushButton(textSetting.textList["mdlinfo"]["mdlinfoPasteLabel"])
        self.mdlinfoPasteButton.setFixedSize(buttonWidth, buttonHeight)
        self.mdlinfoPasteButton.setEnabled(False)
        self.mdlinfoPasteButton.clicked.connect(self.mdlinfoPasteFunc)
        headerRightButtonLayout3.addWidget(self.mdlinfoPasteButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button3
        self.addSmfModelButton = QPushButton(textSetting.textList["mdlinfo"]["addSmfModelLabel"])
        self.addSmfModelButton.setFixedSize(buttonWidth, buttonHeight)
        self.addSmfModelButton.setEnabled(False)
        self.addSmfModelButton.clicked.connect(self.addSmfModelFunc)
        headerRightButtonLayout3.addWidget(self.addSmfModelButton)

        headerLayout.addSpacing(20)
        # content
        contentFrame = QGroupBox(textSetting.textList["mdlinfo"]["scriptLabel"])
        mainLayout.addWidget(contentFrame, 11)
        contentLayout = QVBoxLayout()
        contentFrame.setLayout(contentLayout)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def createMdlinfoTable(self):
        headerLabelList = [
            textSetting.textList["mdlinfo"]["treeSmf"],
            textSetting.textList["mdlinfo"]["treeSmfType"],
            textSetting.textList["mdlinfo"]["treeSmfEleNum"],
            textSetting.textList["mdlinfo"]["binFileLabel"],
            textSetting.textList["mdlinfo"]["binFileFlag"]
        ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.contentTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)
        for mdlInfo in self.decryptFile.allInfoList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            dataList = [
                mdlInfo["smfName"],
                mdlInfo["smfType"],
                len(mdlInfo["smfDetailList"]),
                mdlInfo["binInfo"][0],
                mdlInfo["binInfo"][1]
            ]
            for colIdx, data in enumerate(dataList):
                if colIdx == 3:
                    if data:
                        item = QTableWidgetItem(str(data))
                    else:
                        item = QTableWidgetItem("-")
                else:
                    item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, colIdx, item)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.mdlDetailButton.setEnabled(False)
            self.mdlTypeButton.setEnabled(False)
            self.mdlSmfElementButton.setEnabled(False)
            self.binFileFlagButton.setEnabled(False)
            self.mdlinfoDeleteButton.setEnabled(False)
            self.mdlinfoCopyButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.mdlDetailButton.setEnabled(True)
        self.mdlTypeButton.setEnabled(True)
        self.mdlSmfElementButton.setEnabled(True)
        self.binFileFlagButton.setEnabled(True)
        self.mdlinfoDeleteButton.setEnabled(True)
        self.mdlinfoCopyButton.setEnabled(True)

    def tableFilterFunc(self):
        for row in range(self.contentTable.rowCount()):
            self.contentTable.setRowHidden(row, False)
        filterText = self.searchLineEdit.text().lower()
        if not filterText:
            return

        for row in range(self.contentTable.rowCount()):
            item = self.contentTable.item(row, 0)
            if not item:
                continue
            name = item.text().lower()
            if filterText not in name:
                self.contentTable.setRowHidden(row, True)

    def openFile(self):
        fileType = "{0} ({1})".format(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return
        del self.decryptFile
        self.decryptFile = MdlDecrypt(file_path)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E18"])
            return

        filename = os.path.basename(file_path)
        self.fileNameLabel.setText(filename)
        self.searchLineEdit.setReadOnly(False)

        self.clearTable()
        self.createMdlinfoTable()
        self.copyAnotherMdlinfoButton.setEnabled(True)
        self.addSmfModelButton.setEnabled(True)
        self.copyInfoByteArr = None
        self.mdlinfoPasteButton.setEnabled(False)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.allInfoList):
                self.selectId = len(self.decryptFile.allInfoList) - 1
            self.contentTable.selectRow(self.selectId)

    def reloadFile(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            self.clearTable()
            self.createMdlinfoTable()

            if self.searchLineEdit.text() != "":
                self.tableFilterFunc()
            QTimer.singleShot(0, self.jumpToSelect)
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def mdlDetailFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        mdlDetailDialog = MdlDetailDialog(self, textSetting.textList["mdlinfo"]["detailModelInfo"], num, self.decryptFile)
        mdlDetailDialog.exec()
        if mdlDetailDialog.dirtyFlag:
            self.selectId = num
            self.reloadFile()

    def mdlTypeFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        smfTypeDialog = SmfTypeDialog(self, textSetting.textList["mdlinfo"]["detailModelTypeInfo"], num, self.decryptFile)
        if smfTypeDialog.exec() == QDialog.Accepted:
            resultValue = int(smfTypeDialog.smfTypeLineEdit.text())
            if not self.decryptFile.updateType(num, resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I120"])
            self.selectId = num
            self.reloadFile()

    def mdlSmfElementFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        smfDetailDialog = SmfDetailDialog(self, textSetting.textList["mdlinfo"]["smfInfo"], num, self.decryptFile)
        smfDetailDialog.exec()
        if smfDetailDialog.dirtyFlag:
            self.selectId = num
            self.reloadFile()

    def binFileFlagFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        binFileOrFlagEditDialog = BinFileOrFlagEditDialog(self, textSetting.textList["mdlinfo"]["binFileOrFlagLabel"], num, self.decryptFile)
        if binFileOrFlagEditDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateBinFileOrFlag(num, binFileOrFlagEditDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I36"])
            self.selectId = num
            self.reloadFile()

    def copyAnotherMdlinfoFunc(self):
        fileType = "{0} ({1})".format(textSetting.textList["mdlinfo"]["fileType"], "MDLINFO*.BIN")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return
        tempDecryptFile = MdlDecrypt(file_path)
        if not tempDecryptFile.open():
            tempDecryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E18"])
            return

        copyMdlDialog = CopyMdlDialog(self, textSetting.textList["mdlinfo"]["copyAnotherMdlinfo"], tempDecryptFile)
        if copyMdlDialog.exec() == QDialog.Accepted:
            del tempDecryptFile
            tempDecryptFile = None

            if not self.decryptFile.copy(copyMdlDialog.copyByteArr):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
            self.selectId = len(self.decryptFile.allInfoList)
            self.reloadFile()

    def mdlinfoDeleteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        warnMsg = textSetting.textList["infoList"]["I25"].format(num + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.delete(num):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = num
            self.reloadFile()

    def mdlinfoCopyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        index = self.decryptFile.allInfoList[num]["smfIndex"]
        if num + 1 < len(self.decryptFile.allInfoList):
            nextIndex = self.decryptFile.allInfoList[num + 1]["smfIndex"]
            self.copyInfoByteArr = self.decryptFile.byteArr[index:nextIndex]
        else:
            self.copyInfoByteArr = self.decryptFile.byteArr[index:]

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.mdlinfoPasteButton.setEnabled(True)

    def mdlinfoPasteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteMdlinfoDialog = PasteMdlinfoDialog(self, textSetting.textList["mdlinfo"]["copyModelLabel"], self.decryptFile, num, self.copyInfoByteArr)
        if pasteMdlinfoDialog.exec() == QDialog.Accepted:
            self.selectId = num + pasteMdlinfoDialog.insertPos
            self.reloadFile()

    def addSmfModelFunc(self):
        fileType = "{0} ({1})".format(textSetting.textList["smf"]["fileType"], "*.SMF")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )
        if not file_path:
            return

        smfDecryptFile = SmfDecrypt(file_path)
        if not smfDecryptFile.open():
            smfDecryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return

        meshInfoList = smfDecryptFile.meshList
        filename = os.path.basename(file_path)
        if not self.decryptFile.readSMFSave(filename, meshInfoList):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E19"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
        self.selectId = len(self.decryptFile.allInfoList)
        self.reloadFile()


class SmfTypeDialog(QDialog):
    def __init__(self, parent, title, num, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.smfType = decryptFile.allInfoList[num]["smfType"]

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.smfTypeGridLayout = QGridLayout()
        layout.addLayout(self.smfTypeGridLayout)

        # layout - QGridLayout - label
        smfTypeLabel = QLabel(textSetting.textList["mdlinfo"]["smfTypeLabel"], font=self.font2)
        self.smfTypeGridLayout.addWidget(smfTypeLabel, 0, 0)
        # layout - QGridLayout - lineEdit
        self.smfTypeLineEdit = QLineEdit(font=self.font2)
        self.smfTypeLineEdit.setText("{0}".format(self.smfType))
        self.smfTypeLineEdit.setValidator(integerValidator)
        self.smfTypeGridLayout.addWidget(self.smfTypeLineEdit, 0, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if not self.smfTypeLineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I119"], icon="warning")
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class BinFileOrFlagEditDialog(QDialog):
    def __init__(self, parent, title, num, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.smfName = decryptFile.allInfoList[num]["smfName"]
        self.binFile = decryptFile.allInfoList[num]["binInfo"][0]
        self.flag = decryptFile.allInfoList[num]["binInfo"][1]
        self.resultValueList = []

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.binFileOrFlagGridLayout = QGridLayout()
        layout.addLayout(self.binFileOrFlagGridLayout)
        self.lineEditList = []

        # layout - QGridLayout - label
        smfNameLabel = QLabel(textSetting.textList["mdlinfo"]["smfNameLabel"], font=self.font2)
        self.binFileOrFlagGridLayout.addWidget(smfNameLabel, 0, 0)
        # layout - QGridLayout - lineEdit
        smfNameLineEdit = QLineEdit(font=self.font2)
        smfNameLineEdit.setText("{0}".format(self.smfName))
        self.lineEditList.append(smfNameLineEdit)
        self.binFileOrFlagGridLayout.addWidget(smfNameLineEdit, 0, 1)

        # layout - QGridLayout - label
        binFileNameLabel = QLabel(textSetting.textList["mdlinfo"]["binFileLabel"], font=self.font2)
        self.binFileOrFlagGridLayout.addWidget(binFileNameLabel)
        # layout - QGridLayout - lineEdit
        binFileNameLineEdit = QLineEdit(font=self.font2)
        binFileNameLineEdit.setText("{0}".format(self.binFile))
        self.lineEditList.append(binFileNameLineEdit)
        self.binFileOrFlagGridLayout.addWidget(binFileNameLineEdit, 1, 1)

        # layout - QGridLayout - label
        binFileFlagLabel = QLabel(textSetting.textList["mdlinfo"]["binFileFlag"], font=self.font2)
        self.binFileOrFlagGridLayout.addWidget(binFileFlagLabel, 2, 0)
        # layout - QGridLayout - lineEdit
        binFileFlagLineEdit = QLineEdit(font=self.font2)
        binFileFlagLineEdit.setText("{0}".format(self.flag))
        binFileFlagLineEdit.setValidator(integerValidator)
        self.lineEditList.append(binFileFlagLineEdit)
        self.binFileOrFlagGridLayout.addWidget(binFileFlagLineEdit, 2, 1)

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

            if i == 0:
                if not lineEdit.text():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E17"])
                    return False

            if i == 2:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                self.resultValueList.append(lineEdit.text())
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I35"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class CopyMdlDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.copyByteArr = None
        self.smfName = []
        self.comboSmfName = []

        for index, allInfo in enumerate(decryptFile.allInfoList):
            self.smfName.append(allInfo["smfName"])
            self.comboSmfName.append("({0}){1}".format(index + 1, allInfo["smfName"]))

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        copyMdlinfoLabel = QLabel(textSetting.textList["infoList"]["I37"], font=font2)
        layout.addWidget(copyMdlinfoLabel)
        # layout - Combobox
        self.combobox = QComboBox(font=font2)
        self.combobox.addItems(self.comboSmfName)
        layout.addWidget(self.combobox)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        idx = self.combobox.currentIndex()
        index = self.decryptFile.allInfoList[idx]["smfIndex"]

        if idx + 1 < len(self.decryptFile.allInfoList):
            nextIndex = self.decryptFile.allInfoList[idx + 1]["smfIndex"]
            self.copyByteArr = self.decryptFile.byteArr[index:nextIndex]
        else:
            self.copyByteArr = self.decryptFile.byteArr[index:]
        return True

    def accept(self):
        idx = self.combobox.currentIndex()
        warnMsg = textSetting.textList["infoList"]["I38"].format(self.smfName[idx])
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class PasteMdlinfoDialog(QDialog):
    def __init__(self, parent, title, decryptFile, num, copyInfoByteArr):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.num = num
        self.copyInfoByteArr = copyInfoByteArr
        self.insertPos = 0

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        pastePosLabel = QLabel(textSetting.textList["infoList"]["I4"], font=font2)
        layout.addWidget(pastePosLabel)
        # layout - buttonLayout
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        # layout - buttonLayout - frontButton
        frontButton = QPushButton(textSetting.textList["mdlinfo"]["pasteFront"], font=font2)
        frontButton.clicked.connect(self.frontInsert)
        buttonLayout.addWidget(frontButton)
        # layout - buttonLayout - backButton
        backButton = QPushButton(textSetting.textList["mdlinfo"]["pasteBack"], font=font2)
        backButton.clicked.connect(self.backInsert)
        buttonLayout.addWidget(backButton)
        # layout - buttonLayout - cancelButton
        cancelButton = QPushButton(textSetting.textList["mdlinfo"]["pasteCancel"], font=font2)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

    def frontInsert(self):
        super().accept()
        self.insertPos = 0
        if not self.decryptFile.copySaveFile(self.num, self.copyInfoByteArr):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])

    def backInsert(self):
        super().accept()
        self.insertPos = 1
        if not self.decryptFile.copySaveFile(self.num + 1, self.copyInfoByteArr):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
