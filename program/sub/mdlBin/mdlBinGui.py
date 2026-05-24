import os
import copy
import traceback

import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from program.sub.cmdList import cmdList
from program.sub.mdlBin.dendDecrypt.decrypt import MdlBinDecrypt
from program.sub.mdlBin.importPy.headerDialogWidget import EditHeaderDialog
import program.sub.mdlBin.mdlBinProcess as mdlBinProcess

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QComboBox, QGroupBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSpinBox,
    QDialog, QDialogButtonBox, QGridLayout, QCompleter, QLayout,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()
errObj = ErrorLogObj()


class MdlBinWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.selectId = None
        self.copyScriptData = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        labelHeight = 28
        csvButtonWidth = 120
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

        # headerLeft - name
        headerNameLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerNameLayout)
        # headerLeft - name - fileName
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedHeight(labelHeight)
        headerNameLayout.addWidget(self.fileNameLabel)
        # headerLeft - name - ver
        self.fileVerLabel = QLabel("", font=font2)
        self.fileVerLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileVerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileVerLabel.setFixedSize(40, labelHeight)
        headerNameLayout.addWidget(self.fileVerLabel)

        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerSelectLayout.setContentsMargins(0, 15, 0, 15)
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["mdlBin"]["selectNum"], font=font2)
        selectLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

        # headerLeft - csvButtonLayout
        headerCsvButtonLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerCsvButtonLayout)
        # headerLeft - csvButtonLayout - csvExtractButton
        self.csvExtractButton = QPushButton(textSetting.textList["mdlBin"]["csvExtractLabel"])
        self.csvExtractButton.setFixedSize(csvButtonWidth, buttonHeight)
        self.csvExtractButton.setEnabled(False)
        self.csvExtractButton.clicked.connect(self.csvExtractFunc)
        headerCsvButtonLayout.addWidget(self.csvExtractButton)
        # stretch
        headerCsvButtonLayout.addStretch()
        # headerLeft - csvButtonLayout - csvLoadAndSaveButton
        self.csvLoadAndSaveButton = QPushButton(textSetting.textList["mdlBin"]["csvSaveLabel"])
        self.csvLoadAndSaveButton.setFixedSize(csvButtonWidth, buttonHeight)
        self.csvLoadAndSaveButton.setEnabled(False)
        self.csvLoadAndSaveButton.clicked.connect(self.csvLoadAndSaveFunc)
        headerCsvButtonLayout.addWidget(self.csvLoadAndSaveButton)

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
        self.modifyButton = QPushButton(textSetting.textList["mdlBin"]["editLineLabel"])
        self.modifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifyButton.setEnabled(False)
        self.modifyButton.clicked.connect(self.modifyFunc)
        headerRightButtonLayout1.addWidget(self.modifyButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button2
        self.insertButton = QPushButton(textSetting.textList["mdlBin"]["insertLineLabel"])
        self.insertButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertButton.setEnabled(False)
        self.insertButton.clicked.connect(self.insertFunc)
        headerRightButtonLayout1.addWidget(self.insertButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button3
        self.deleteButton = QPushButton(textSetting.textList["mdlBin"]["deleteLineLabel"])
        self.deleteButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteFunc)
        headerRightButtonLayout1.addWidget(self.deleteButton)

        # stretch
        headerRightLayout.addStretch()

        # headerRight - buttonLayout
        headerRightButtonLayout2 = QHBoxLayout()
        headerRightButtonLayout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout2)
        # headerRight - buttonLayout - button1
        self.copyButton = QPushButton(textSetting.textList["mdlBin"]["copyLineLabel"])
        self.copyButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyButton.setEnabled(False)
        self.copyButton.clicked.connect(self.copyFunc)
        headerRightButtonLayout2.addWidget(self.copyButton)
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout - button2
        self.pasteButton = QPushButton(textSetting.textList["mdlBin"]["pasteLineLabel"])
        self.pasteButton.setFixedSize(buttonWidth, buttonHeight)
        self.pasteButton.setEnabled(False)
        self.pasteButton.clicked.connect(self.pasteFunc)
        headerRightButtonLayout2.addWidget(self.pasteButton)
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout - button3
        self.headerEditButton = QPushButton(textSetting.textList["mdlBin"]["headerEditLabel"])
        self.headerEditButton.setFixedSize(buttonWidth, buttonHeight)
        self.headerEditButton.setEnabled(False)
        self.headerEditButton.clicked.connect(self.headerEditFunc)
        headerRightButtonLayout2.addWidget(self.headerEditButton)

        # stretch
        headerRightLayout.addStretch()

        # headerRight - buttonLayout
        headerRightButtonLayout3 = QHBoxLayout()
        headerRightButtonLayout3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout3)
        # headerRight - buttonLayout - button1
        self.listHeaderModifyButton = QPushButton(textSetting.textList["mdlBin"]["listHeaderModifyBtnLabel"])
        self.listHeaderModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.listHeaderModifyButton.setEnabled(False)
        self.listHeaderModifyButton.clicked.connect(self.listHeaderModifyFunc)
        headerRightButtonLayout3.addWidget(self.listHeaderModifyButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button2
        self.listNumModifyButton = QPushButton(textSetting.textList["mdlBin"]["listNumModifyBtnLabel"])
        self.listNumModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.listNumModifyButton.setEnabled(False)
        self.listNumModifyButton.clicked.connect(self.listNumModifyFunc)
        headerRightButtonLayout3.addWidget(self.listNumModifyButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button3
        self.numModifyButton = QPushButton(textSetting.textList["mdlBin"]["numModifyBtnLabel"])
        self.numModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.numModifyButton.setEnabled(False)
        self.numModifyButton.clicked.connect(self.numModifyFunc)
        headerRightButtonLayout3.addWidget(self.numModifyButton)

        headerLayout.addSpacing(20)
        # content
        contentFrame = QGroupBox(textSetting.textList["mdlBin"]["scriptLabel"])
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

    def createMdlBinTable(self):
        self.setMdlBinTableHeader()
        self.setMdlBinTableData()
    
    def setMdlBinTableHeader(self):
        headerLabelList = [
            textSetting.textList["mdlBin"]["treeDelay"],
            textSetting.textList["mdlBin"]["treeName"]
        ]
        for i in range(self.decryptFile.max_param):
            colName = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
            headerLabelList.append(colName)
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setMdlBinTableData(self):
        num = 0
        for scriptDataInfoList in self.decryptFile.scriptDataAllInfoList:
            listNum = 0
            for scriptDataInfo in scriptDataInfoList:
                sectionNum = 0
                itemId = "{0},{1},{2}".format(num, listNum, sectionNum)
                valueList = [
                    "-",
                    "---#{0}, {1}#---".format(num, listNum),
                    ",".join(str(n) for n in scriptDataInfo[0])
                ]
                rowCount = self.contentTable.rowCount()
                self.contentTable.insertRow(rowCount)
                for j, value in enumerate(valueList):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setData(Qt.UserRole, itemId)
                    self.contentTable.setItem(rowCount, j, item)

                sectionNum += 1
                for scriptData in scriptDataInfo[1:]:
                    itemId = "{0},{1},{2}".format(num, listNum, sectionNum)
                    valueList = [
                        scriptData[0],
                        cmdList[scriptData[1]]
                    ]
                    paramCnt = scriptData[2]
                    for i in range(paramCnt):
                        valueList.append(scriptData[4 + i])

                    rowCount = self.contentTable.rowCount()
                    self.contentTable.insertRow(rowCount)
                    for j, value in enumerate(valueList):
                        item = QTableWidgetItem(str(value))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        item.setData(Qt.UserRole, itemId)
                        self.contentTable.setItem(rowCount, j, item)
                    sectionNum += 1
                listNum += 1
            num += 1

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.copyButton.setEnabled(False)
            self.listHeaderModifyButton.setEnabled(False)
            self.listNumModifyButton.setEnabled(False)
            self.numModifyButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        itemId = selectedItems[0].data(Qt.UserRole)
        cmdDiff = int(itemId.split(",")[2])
        if cmdDiff == 0:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.copyButton.setEnabled(False)
            self.listHeaderModifyButton.setEnabled(True)
            self.listNumModifyButton.setEnabled(True)
            self.numModifyButton.setEnabled(True)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            self.copyButton.setEnabled(True)
            self.listHeaderModifyButton.setEnabled(False)
            self.listNumModifyButton.setEnabled(False)
            self.numModifyButton.setEnabled(False)
        self.insertButton.setEnabled(True)

    def openFile(self):
        fileType = "{0} ({1})".format(textSetting.textList["mdlBin"]["fileType"], "*.BIN")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return
        del self.decryptFile
        self.decryptFile = MdlBinDecrypt(file_path, cmdList)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])
            return

        filename = os.path.basename(file_path)
        self.fileNameLabel.setText(filename)
        self.fileVerLabel.setText("{0}".format(self.decryptFile.ver))

        self.clearTable()
        self.createMdlBinTable()
        self.headerEditButton.setEnabled(True)
        self.csvExtractButton.setEnabled(True)
        self.csvLoadAndSaveButton.setEnabled(True)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= self.contentTable.rowCount():
                self.selectId = self.contentTable.rowCount() - 1
            self.contentTable.selectRow(self.selectId)

    def reloadFile(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            self.clearTable()
            self.createMdlBinTable()

            QTimer.singleShot(0, self.jumpToSelect)
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

    def getScriptData(self, itemId):
        arr = itemId.split(",")
        num = int(arr[0])
        scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[num]
        listNum = int(arr[1])
        scriptDataInfo = scriptDataInfoList[listNum]
        cmdDiff = int(arr[2])
        return scriptDataInfo[1:][cmdDiff - 1]

    def getHeaderData(self, itemId):
        arr = itemId.split(",")
        num = int(arr[0])
        scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[num]
        listNum = int(arr[1])
        scriptDataInfo = scriptDataInfoList[listNum]
        return scriptDataInfo[0]

    def modifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        scriptData = self.getScriptData(itemId)
        editMdlBinDialog = EditMdlBinDialog(self, textSetting.textList["mdlBin"]["cmdModify"], self.decryptFile.ver, itemId, scriptData, cmdList)
        if editMdlBinDialog.exec() == QDialog.Accepted:
            itemIdArr = [int(x) for x in itemId.split(",")]
            if not self.decryptFile.saveFile(itemIdArr, "modify", editMdlBinDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num + editMdlBinDialog.insertPos
            self.reloadFile()

    def insertFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        editMdlBinDialog = EditMdlBinDialog(self, textSetting.textList["mdlBin"]["cmdModify"], self.decryptFile.ver, itemId, None, cmdList)
        if editMdlBinDialog.exec() == QDialog.Accepted:
            itemIdArr = [int(x) for x in itemId.split(",")]
            scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[itemIdArr[0]]
            scriptDataInfo = scriptDataInfoList[itemIdArr[1]]
            if len(scriptDataInfo[1:]) >= 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E142"].format(itemIdArr[0], itemIdArr[1]))
                return

            itemIdArr[2] += editMdlBinDialog.insertPos
            if not self.decryptFile.saveFile(itemIdArr, "insert", editMdlBinDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num + editMdlBinDialog.insertPos
            self.reloadFile()

    def deleteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            itemIdArr = [int(x) for x in itemId.split(",")]
            if not self.decryptFile.saveFile(itemIdArr, "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def copyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        itemId = selectedItems[0].data(Qt.UserRole)
        self.copyScriptData = copy.deepcopy(self.getScriptData(itemId))
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteButton.setEnabled(True)

    def pasteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        pasteMdlBinDialog = PasteMdlBinDialog(self, textSetting.textList["mdlBin"]["cmdPaste"])
        if pasteMdlBinDialog.exec() == QDialog.Accepted:
            itemIdArr = [int(x) for x in itemId.split(",")]
            scriptDataInfoList = self.decryptFile.scriptDataAllInfoList[itemIdArr[0]]
            scriptDataInfo = scriptDataInfoList[itemIdArr[1]]
            if len(scriptDataInfo[1:]) >= 255:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E142"].format(itemIdArr[0], itemIdArr[1]))
                return

            itemIdArr[2] += pasteMdlBinDialog.insertPos
            if not self.decryptFile.saveFile(itemIdArr, "insert", self.copyScriptData):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
            self.selectId = num + pasteMdlBinDialog.insertPos
            self.reloadFile()

    def headerEditFunc(self):
        editHeaderDialog = EditHeaderDialog(self, textSetting.textList["mdlBin"]["headerInfo"], self.decryptFile)
        if editHeaderDialog.exec() == QDialog.Accepted:
            self.reloadFile()

    def listHeaderModifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        itemIdArr = [int(x) for x in itemId.split(",")]
        headerInfo = self.getHeaderData(itemId)
        editListHeaderDialog = EditListHeaderDialog(self, textSetting.textList["mdlBin"]["listHeaderModifyLabel"], headerInfo)
        if editListHeaderDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveListHeader(itemIdArr, editListHeaderDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I23"])
            self.selectId = num
            self.reloadFile()

    def listNumModifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        itemId = selectedItems[0].data(Qt.UserRole)
        itemIdArr = [int(x) for x in itemId.split(",")]
        listNumCount = len(self.decryptFile.scriptDataAllInfoList[itemIdArr[0]])
        editListNumDialog = EditListNumDialog(self, textSetting.textList["mdlBin"]["listNumModifyLabel"], itemIdArr, listNumCount)
        if editListNumDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveListNum(itemIdArr, editListNumDialog.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I22"])
            self.selectId = num
            self.reloadFile()

    def numModifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        numCount = len(self.decryptFile.scriptDataAllInfoList)
        editNumDialog = EditNumDialog(self, textSetting.textList["mdlBin"]["numModifyLabel"], numCount)
        if editNumDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveNumFile(editNumDialog.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I141"])
            self.selectId = num
            self.reloadFile()

    def csvExtractFunc(self):
        filename = os.path.splitext(os.path.basename(self.decryptFile.filePath))[0] + ".csv"
        fileTypes = "{0} ({1})".format("mdlbin_csv", "*.csv")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            fileTypes
        )
        if not file_path:
            return

        try:
            mdlBinProcess.writeCsv(file_path, self.decryptFile.scriptDataAllInfoList, cmdList)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def csvLoadAndSaveFunc(self):
        fileTypes = "{0} ({1})".format("mdlbin_csv", "*.csv")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileTypes
        )
        if not file_path:
            return

        processResult, obj = mdlBinProcess.loadCsvData(file_path, cmdList)
        if not processResult:
            mb.showerror(title=textSetting.textList["error"], message=obj["message"])
            return
        msg = textSetting.textList["infoList"]["I15"].format(obj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.saveCsv(obj["data"]):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I16"])
            self.reloadFile()


class EditMdlBinDialog(QDialog):
    def __init__(self, parent, title, ver, itemId, scriptData, cmdList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.ver = ver
        self.itemId = itemId
        self.scriptData = scriptData
        self.cmdList = cmdList
        self.sortedCmdList = sorted(cmdList, key=str.lower)
        self.insertPos = 0
        self.resultValueList = []
        if scriptData is not None:
            self.mode = "modify"
        else:
            self.mode = "insert"

        self.setWindowFlags((self.windowFlags() & ~Qt.WindowMinMaxButtonsHint) | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.mdlBinGridLayout = QGridLayout()
        layout.addLayout(self.mdlBinGridLayout)

        # layout - QGridLayout - delayLabel
        delayLabel = QLabel(textSetting.textList["mdlBin"]["treeDelay"], font=self.font2)
        self.mdlBinGridLayout.addWidget(delayLabel, 0, 0)
        # layout - QGridLayout - delayLineEdit
        self.delayLineEdit = QLineEdit(font=self.font2)
        self.delayLineEdit.setValidator(self.integerValidator)
        if self.mode == "modify":
            self.delayLineEdit.setText("{0}".format(scriptData[0]))
        elif self.mode == "insert":
            self.delayLineEdit.setText("{0}".format(0))
        self.mdlBinGridLayout.addWidget(self.delayLineEdit, 0, 1)

        # layout - QGridLayout - cmdLabel
        cmdLabel = QLabel(textSetting.textList["mdlBin"]["treeName"], font=self.font2)
        self.mdlBinGridLayout.addWidget(cmdLabel, 1, 0)
        # layout - QGridLayout - cmdCombo
        self.cmdCombo = QComboBox(font=self.font2)
        self.cmdCombo.setEditable(True)
        self.cmdCombo.addItems(self.sortedCmdList)

        completer = QCompleter(self.cmdCombo.model())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.cmdCombo.setCompleter(completer)
        if self.mode == "modify":
            idx = self.sortedCmdList.index(cmdList[scriptData[1]])
            self.cmdCombo.setCurrentIndex(idx)
        self.mdlBinGridLayout.addWidget(self.cmdCombo, 1, 1)

        self.lineEditList = []
        # layout - QGridLayout - paramCountLabel
        paramCountLabel = QLabel(textSetting.textList["mdlBin"]["paramLabel"], font=self.font2)
        self.mdlBinGridLayout.addWidget(paramCountLabel, 2, 0)
        # layout - QGridLayout - paramCountCombo
        paramCntList = [str(cnt) for cnt in range(0, 16)]
        self.paramCountCombo = QComboBox(font=self.font2)
        self.paramCountCombo.addItems(paramCntList)
        self.paramCountCombo.currentIndexChanged.connect(self.createParam)
        self.paramCountCombo.setCurrentIndex(0)
        self.mdlBinGridLayout.addWidget(self.paramCountCombo, 2, 1)

        if self.mode == "insert":
            # layout - QGridLayout - insertLabel
            insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
            self.mdlBinGridLayout.addWidget(insertLabel, 3, 0)
            # layout - QGridLayout - insertCombo
            self.insertCombo = QComboBox(font=self.font2)
            self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
            self.mdlBinGridLayout.addWidget(self.insertCombo, 3, 1)

        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.mdlBinGridLayout.addWidget(horizentalLine, 4, 0, 1, 2)

        if self.mode == "modify":
            self.paramCountCombo.setCurrentIndex(self.scriptData[2])

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def deleteParam(self):
        self.lineEditList = []
        for i in range(16):
            item1 = self.mdlBinGridLayout.itemAtPosition(5 + i, 0)
            if item1 is not None:
                widget1 = item1.widget()
                if widget1 is not None:
                    self.mdlBinGridLayout.removeWidget(widget1)
                    widget1.deleteLater()

            item2 = self.mdlBinGridLayout.itemAtPosition(5 + i, 1)
            if item2 is not None:
                widget2 = item2.widget()
                if widget2 is not None:
                    self.mdlBinGridLayout.removeWidget(widget2)
                    widget2.deleteLater()
        self.adjustSize()

    def createParam(self):
        self.deleteParam()
        cnt = self.paramCountCombo.currentIndex()
        for i in range(cnt):
            # layout - QGridLayout - paramLabel
            paramLabel = QLabel(textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1), font=self.font2)
            self.mdlBinGridLayout.addWidget(paramLabel, 5 + i, 0)
            # layout - QGridLayout - paramLineEdit
            paramLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(paramLineEdit)
            if self.mode == "modify" and i < self.scriptData[2]:
                paramLineEdit.setText("{0}".format(self.scriptData[4 + i]))
            self.mdlBinGridLayout.addWidget(paramLineEdit, 5 + i, 1)

    def validate(self):
        self.resultValueList = []
        if not self.delayLineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        self.resultValueList.append(int(self.delayLineEdit.text()))
        self.resultValueList.append(self.cmdList.index(self.cmdCombo.currentText()))
        self.resultValueList.append(self.paramCountCombo.currentIndex())
        self.resultValueList.append(0xFF)

        floatFlag = True
        strCount = 0
        strParamList = []
        for i, lineEdit in enumerate(self.lineEditList):
            paramMsg = textSetting.textList["mdlBin"]["paramNumLabel"].format(i + 1)
            if not lineEdit.text():
                errorMsg = textSetting.textList["errorList"]["E139"].format(paramMsg)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            if floatFlag:
                try:
                    float(lineEdit.text())
                except ValueError:
                    floatFlag = False
                    if self.ver == 1:
                        errorMsg = "{0} [{1}]".format(textSetting.textList["errorList"]["E5"], paramMsg)
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return
            
            if floatFlag:
                self.resultValueList.append(float(lineEdit.text()))
            else:
                self.resultValueList.append(str(lineEdit.text()))
                strCount += 1
                strParamList.append(paramMsg)

        if self.ver >= 2:
            if strCount > 0:
                self.resultValueList[3] = strCount

        if self.ver == 2:
            if self.cmdCombo.currentText() not in ["MDL_GETINDEX", "SET_LENSFLEAR_MT"]:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E140"])
                return
            else:
                errorMsg = textSetting.textList["errorList"]["E141"].format(self.cmdCombo.currentText())
                if strCount != 1:
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                    return
                else:
                    param2 = textSetting.textList["mdlBin"]["paramNumLabel"].format(2)
                    if strParamList[0] != param2:
                        mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                        return

        msg = "\n".join(strParamList)
        if msg:
            msg += "\n"
            msg += textSetting.textList["infoList"]["I17"]
        msg += textSetting.textList["infoList"]["I21"]
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=msg)
        if result == mb.OK:
            if self.mode == "insert":
                self.insertPos = 1
                if self.insertCombo.currentIndex() == 1:
                    self.insertPos = 0
            return True

    def accept(self):
        if not self.validate():
            return False
        super().accept()


class PasteMdlBinDialog(QDialog):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowTitle(title)
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

    def backInsert(self):
        super().accept()
        self.insertPos = 1


class EditListHeaderDialog(QDialog):
    def __init__(self, parent, title, headerInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resultValueList = []

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.listHeaderGridLayout = QGridLayout()
        layout.addLayout(self.listHeaderGridLayout)
        self.lineEditList = []

        # layout - QGridLayout - label
        delayNameLabel = QLabel(textSetting.textList["mdlBin"]["treeDelay"], font=font2)
        self.listHeaderGridLayout.addWidget(delayNameLabel, 0, 0)
        # layout - QGridLayout - lineEdit
        delayLineEdit = QLineEdit(font=font2)
        delayLineEdit.setText("{0}".format(headerInfo[0]))
        delayLineEdit.setValidator(integerValidator)
        self.lineEditList.append(delayLineEdit)
        self.listHeaderGridLayout.addWidget(delayLineEdit, 0, 1)

        # layout - QGridLayout - label
        anime1NameLabel = QLabel(textSetting.textList["mdlBin"]["anime1Label"], font=font2)
        self.listHeaderGridLayout.addWidget(anime1NameLabel)
        # layout - QGridLayout - lineEdit
        anime1LineEdit = QLineEdit(font=font2)
        anime1LineEdit.setText("{0}".format(headerInfo[1]))
        anime1LineEdit.setValidator(integerValidator)
        self.lineEditList.append(anime1LineEdit)
        self.listHeaderGridLayout.addWidget(anime1LineEdit, 1, 1)

        # layout - QGridLayout - label
        anime2NameLabel = QLabel(textSetting.textList["mdlBin"]["anime2Label"], font=font2)
        self.listHeaderGridLayout.addWidget(anime2NameLabel, 2, 0)
        # layout - QGridLayout - lineEdit
        anime2LineEdit = QLineEdit(font=font2)
        anime2LineEdit.setText("{0}".format(headerInfo[2]))
        anime2LineEdit.setValidator(integerValidator)
        self.lineEditList.append(anime2LineEdit)
        self.listHeaderGridLayout.addWidget(anime2LineEdit, 2, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValueList = []
        for lineEdit in self.lineEditList:
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            self.resultValueList.append(int(lineEdit.text()))
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditListNumDialog(QDialog):
    def __init__(self, parent, title, itemIdArr, listNum):
        super().__init__(parent)
        self.setWindowTitle(title)
        spinBoxWidth = 150
        self.listNum = listNum
        self.resultValue = -1

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.listNumGridLayout = QGridLayout()
        layout.addLayout(self.listNumGridLayout)

        # layout - QGridLayout - label
        numNameLabel = QLabel(textSetting.textList["infoList"]["I18"].format(itemIdArr[0]), font=font2)
        self.listNumGridLayout.addWidget(numNameLabel, 0, 0)
        # layout - QGridLayout - spinBox
        self.listNumSpinBox = QSpinBox(font=font2)
        self.listNumSpinBox.setFixedWidth(spinBoxWidth)
        self.listNumSpinBox.setRange(1, 255)
        self.listNumSpinBox.setValue(self.listNum)
        self.listNumGridLayout.addWidget(self.listNumSpinBox, 0, 1)
        # layout - QGridLayout - label
        nameLabel = QLabel(textSetting.textList["infoList"]["I19"], font=font2)
        self.listNumGridLayout.addWidget(nameLabel, 0, 2)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValue = self.listNumSpinBox.value()
        if self.resultValue < self.listNum:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result != mb.OK:
                return False
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditNumDialog(QDialog):
    def __init__(self, parent, title, num):
        super().__init__(parent)
        self.setWindowTitle(title)
        spinBoxWidth = 150
        self.num = num
        self.resultValue = -1

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.listNumGridLayout = QGridLayout()
        layout.addLayout(self.listNumGridLayout)

        # layout - QGridLayout - label
        numNameLabel = QLabel(textSetting.textList["infoList"]["I24"], font=font2)
        self.listNumGridLayout.addWidget(numNameLabel, 0, 0)
        # layout - QGridLayout - spinBox
        self.listNumSpinBox = QSpinBox(font=font2)
        self.listNumSpinBox.setFixedWidth(spinBoxWidth)
        self.listNumSpinBox.setRange(1, 255)
        self.listNumSpinBox.setValue(self.num)
        self.listNumGridLayout.addWidget(self.listNumSpinBox, 0, 1)
        # layout - QGridLayout - label
        nameLabel = QLabel(textSetting.textList["infoList"]["I19"], font=font2)
        self.listNumGridLayout.addWidget(nameLabel, 0, 2)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValue = self.listNumSpinBox.value()
        if self.resultValue < self.num:
            warnMsg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result != mb.OK:
                return False
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
