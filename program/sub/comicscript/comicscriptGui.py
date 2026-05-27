import os
import copy
import traceback

import program.sub.textSetting as textSetting
from program.sub.errorLogClass import ErrorLogObj
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from program.sub.cmdList import cmdList
from program.sub.comicscript.dendDecrypt.decrypt import ComicDecrypt
import program.sub.comicscript.comicscriptProcess as comicscriptProcess
from program.sub.comicscript.importPy.headerDialogWidget import EditHeaderDialog
# from program.comicscript.importPy.tkinterEditClass import InputDialog, PasteDialog, HeaderFileInfo


from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QComboBox, QGroupBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSpinBox,
    QDialog, QDialogButtonBox, QGridLayout, QCompleter, QLayout,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QColor, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()
errObj = ErrorLogObj()


def csvExtract():
    global v_fileName
    global decryptFile
    file = v_fileName.get()
    filename = os.path.splitext(os.path.basename(file))[0]
    file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
    errorMsg = textSetting.textList["errorList"]["E7"]
    if file_path:
        try:
            w = open(file_path, "w")
            for comicData in decryptFile.comicDataList:
                w.write("{0},".format(comicData[0]))
                cmdParaCnt = comicData[1]
                for i in range(cmdParaCnt):
                    w.write("{0}".format(comicData[2 + i]))
                    if i < cmdParaCnt-1:
                        w.write(",")
                w.write("\n")
            w.close()
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)


def csvLoadAndSave():
    global decryptFile
    file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("comicscript_csv", "*.csv")])
    if not file_path:
        return
    f = open(file_path)
    csvLines = f.readlines()
    f.close()

    csvComicDataList = []
    for i in range(len(csvLines)):
        csvComicData = []
        csvLine = csvLines[i].strip()
        arr = csvLine.split(",")
        cmdName = arr[0]
        if cmdName not in cmdList:
            errorMsg = textSetting.textList["errorList"]["E8"].format(i+1, cmdName)
            mb.showerror(title=textSetting.textList["error"], message=errorMsg)
            return

        comicDataParaList = []
        for j in range(1, len(arr)):
            if arr[j] == "":
                break
            try:
                comicDataParaList.append(float(arr[j]))
            except Exception:
                errObj.write(traceback.format_exc())
                errorMsg = textSetting.textList["errorList"]["E9"].format(i+1, arr[j])
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

        csvComicData.append(cmdName)
        cmdParaCnt = len(comicDataParaList)
        csvComicData.append(cmdParaCnt)
        for j in range(len(comicDataParaList)):
            csvComicData.append(comicDataParaList[j])

        csvComicDataList.append(csvComicData)
    warnMsg = textSetting.textList["infoList"]["I11"]
    result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

    if result:
        if not decryptFile.saveComicList(csvComicDataList):
            decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
        reloadFile()


def headerFileEdit():
    global root
    global rootFrameAppearance
    global decryptFile
    result = HeaderFileInfo(root, textSetting.textList["comicscript"]["headerInfo"], decryptFile, rootFrameAppearance)
    if result.reloadFlag:
        reloadFile()


class ComicscriptWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.selectId = None
        self.cmdJsonInfo = self.importDict["cmdJsonInfo"]
        self.copyComicData = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
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
        selectLabel = QLabel(textSetting.textList["comicscript"]["selectNum"], font=font2)
        selectLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

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
        self.modifyButton = QPushButton(textSetting.textList["comicscript"]["editLineLabel"])
        self.modifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifyButton.setEnabled(False)
        self.modifyButton.clicked.connect(self.modifyFunc)
        headerRightButtonLayout1.addWidget(self.modifyButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button2
        self.insertButton = QPushButton(textSetting.textList["comicscript"]["insertLineLabel"])
        self.insertButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertButton.setEnabled(False)
        self.insertButton.clicked.connect(self.insertFunc)
        headerRightButtonLayout1.addWidget(self.insertButton)
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout - button3
        self.deleteButton = QPushButton(textSetting.textList["comicscript"]["deleteLineLabel"])
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
        self.copyButton = QPushButton(textSetting.textList["comicscript"]["copyLineLabel"])
        self.copyButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyButton.setEnabled(False)
        self.copyButton.clicked.connect(self.copyFunc)
        headerRightButtonLayout2.addWidget(self.copyButton)
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout - button2
        self.pasteButton = QPushButton(textSetting.textList["comicscript"]["pasteLineLabel"])
        self.pasteButton.setFixedSize(buttonWidth, buttonHeight)
        self.pasteButton.setEnabled(False)
        self.pasteButton.clicked.connect(self.pasteFunc)
        headerRightButtonLayout2.addWidget(self.pasteButton)
        headerRightButtonLayout2.addStretch(1)

        # dummy
        dummyButton = QPushButton()
        dummyButton.setFixedSize(buttonWidth, buttonHeight)
        dummyButton.setEnabled(False)
        dummyButtonPolicy = dummyButton.sizePolicy()
        dummyButtonPolicy.setRetainSizeWhenHidden(True)
        dummyButton.setSizePolicy(dummyButtonPolicy)
        headerRightButtonLayout2.addWidget(dummyButton)
        dummyButton.hide()

        # stretch
        headerRightLayout.addStretch()

        # headerRight - buttonLayout
        headerRightButtonLayout3 = QHBoxLayout()
        headerRightButtonLayout3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout3)
        # headerRight - buttonLayout - button1
        self.csvExtractButton = QPushButton(textSetting.textList["comicscript"]["csvExtractLabel"])
        self.csvExtractButton.setFixedSize(buttonWidth, buttonHeight)
        self.csvExtractButton.setEnabled(False)
        self.csvExtractButton.clicked.connect(self.csvExtractFunc)
        headerRightButtonLayout3.addWidget(self.csvExtractButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button2
        self.csvLoadAndSaveButton = QPushButton(textSetting.textList["comicscript"]["csvSaveLabel"])
        self.csvLoadAndSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.csvLoadAndSaveButton.setEnabled(False)
        self.csvLoadAndSaveButton.clicked.connect(self.csvLoadAndSaveFunc)
        headerRightButtonLayout3.addWidget(self.csvLoadAndSaveButton)
        headerRightButtonLayout3.addStretch(1)
        # headerRight - buttonLayout - button3
        self.headerEditButton = QPushButton(textSetting.textList["comicscript"]["headerEditLabel"])
        self.headerEditButton.setFixedSize(buttonWidth, buttonHeight)
        self.headerEditButton.setEnabled(False)
        self.headerEditButton.clicked.connect(self.headerEditFunc)
        headerRightButtonLayout3.addWidget(self.headerEditButton)

        headerLayout.addSpacing(20)
        # content
        contentFrame = QGroupBox(textSetting.textList["comicscript"]["scriptLabel"])
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

    def createComicscriptTable(self):
        self.setComicscriptTableHeader()
        self.setComicscriptTableData()
    
    def setComicscriptTableHeader(self):
        headerLabelList = [
            textSetting.textList["comicscript"]["treeName"]
        ]
        for i in range(self.decryptFile.max_param):
            colName = textSetting.textList["comicscript"]["paramNumLabel"].format(i + 1)
            headerLabelList.append(colName)
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setComicscriptTableData(self):
        game = comicscriptProcess.getGameOption(self.importDict["configPath"])
        for comicData in self.decryptFile.comicDataList:
            valueList = [
                comicData[0]
            ]
            paramCnt = comicData[1]
            for i in range(paramCnt):
                valueList.append(comicData[2 + i])

            if self.cmdJsonInfo is not None:
                cmdInfo = self.cmdJsonInfo[comicData[0]]
                if "comicscript" not in cmdInfo:
                    availableList = []
                else:
                    availableList = cmdInfo["comicscript"]

            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, value in enumerate(valueList):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)
                if self.cmdJsonInfo is not None and game not in availableList:
                    item.setForeground(QColor("red"))
                    item.setBackground(QColor("#666666"))

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.copyButton.setEnabled(False)
            return
        
        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.modifyButton.setEnabled(True)
        self.insertButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.copyButton.setEnabled(True)

    def openFile(self):
        fileType = "{0} ({1})".format(textSetting.textList["comicscript"]["fileType"], "*.BIN")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return
        del self.decryptFile
        self.decryptFile = ComicDecrypt(file_path, cmdList)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])
            return

        filename = os.path.basename(file_path)
        self.fileNameLabel.setText(filename)

        self.clearTable()
        self.createComicscriptTable()
        self.headerEditButton.setEnabled(True)
        self.csvExtractButton.setEnabled(True)
        self.csvLoadAndSaveButton.setEnabled(True)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.comicDataList):
                self.selectId = len(self.decryptFile.comicDataList) - 1
            self.contentTable.selectRow(self.selectId)

    def reloadFile(self):
        try:
            self.decryptFile = self.decryptFile.reload()
            self.clearTable()
            self.createComicscriptTable()

            QTimer.singleShot(0, self.jumpToSelect)
        except Exception:
            errObj.write(traceback.format_exc())
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E6"])

    def modifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        comicData = self.decryptFile.comicDataList[num]
        editComicscriptDialog = EditComicscriptDialog(self, textSetting.textList["comicscript"]["cmdModify"], num, comicData, cmdList)
        if editComicscriptDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveFile(num, "modify", editComicscriptDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def insertFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        editComicscriptDialog = EditComicscriptDialog(self, textSetting.textList["comicscript"]["cmdModify"], num, None, cmdList)
        if editComicscriptDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveFile(num + editComicscriptDialog.insertPos, "insert", editComicscriptDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I3"])
            self.selectId = num
            self.reloadFile()

    def deleteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            if not self.decryptFile.saveFile(num, "delete"):
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

        num = selectedItems[0].row()
        self.copyComicData = self.decryptFile.comicDataList[num]
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteButton.setEnabled(True)

    def pasteFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteComicscriptDialog = PasteComicscriptDialog(self, textSetting.textList["comicscript"]["cmdPaste"])
        if pasteComicscriptDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveFile(num + pasteComicscriptDialog.insertPos, "insert", self.copyComicData):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I5"])
            self.selectId = num + pasteComicscriptDialog.insertPos
            self.reloadFile()

    def csvExtractFunc(self):
        pass

    def csvLoadAndSaveFunc(self):
        pass

    def headerEditFunc(self):
        editHeaderDialog = EditHeaderDialog(self, textSetting.textList["comicscript"]["headerInfo"], self.decryptFile)
        if editHeaderDialog.exec() == QDialog.Accepted:
            self.reloadFile()


class EditComicscriptDialog(QDialog):
    def __init__(self, parent, title, num, comicData, cmdList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.comicData = comicData
        self.cmdList = cmdList
        self.sortedCmdList = sorted(cmdList, key=str.lower)
        self.insertPos = 0
        self.resultValueList = []
        if comicData is not None:
            self.mode = "modify"
        else:
            self.mode = "insert"

        self.setWindowFlags((self.windowFlags() & ~Qt.WindowMinMaxButtonsHint) | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)

        # layout
        layout = QVBoxLayout(self)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.comicscriptGridLayout = QGridLayout()
        layout.addLayout(self.comicscriptGridLayout)

        # layout - QGridLayout - cmdLabel
        cmdLabel = QLabel(textSetting.textList["comicscript"]["treeName"], font=self.font2)
        self.comicscriptGridLayout.addWidget(cmdLabel, 0, 0)
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
            idx = self.sortedCmdList.index(comicData[0])
            self.cmdCombo.setCurrentIndex(idx)
        self.comicscriptGridLayout.addWidget(self.cmdCombo, 0, 1)

        self.lineEditList = []
        # layout - QGridLayout - paramCountLabel
        paramCountLabel = QLabel(textSetting.textList["comicscript"]["paramLabel"], font=self.font2)
        self.comicscriptGridLayout.addWidget(paramCountLabel, 1, 0)
        # layout - QGridLayout - paramCountCombo
        paramCntList = [str(cnt) for cnt in range(0, 16)]
        self.paramCountCombo = QComboBox(font=self.font2)
        self.paramCountCombo.addItems(paramCntList)
        self.paramCountCombo.currentIndexChanged.connect(self.createParam)
        self.paramCountCombo.setCurrentIndex(0)
        self.comicscriptGridLayout.addWidget(self.paramCountCombo, 1, 1)

        if self.mode == "insert":
            # layout - QGridLayout - insertLabel
            insertLabel = QLabel(textSetting.textList["comicscript"]["posLabel"], font=self.font2)
            self.comicscriptGridLayout.addWidget(insertLabel, 2, 0)
            # layout - QGridLayout - insertCombo
            self.insertCombo = QComboBox(font=self.font2)
            self.insertCombo.addItems(textSetting.textList["comicscript"]["posValue"])
            self.comicscriptGridLayout.addWidget(self.insertCombo, 2, 1)

        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.comicscriptGridLayout.addWidget(horizentalLine, 3, 0, 1, 2)

        if self.mode == "modify":
            self.paramCountCombo.setCurrentIndex(self.comicData[1])

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def deleteParam(self):
        self.lineEditList = []
        for i in range(16):
            item1 = self.comicscriptGridLayout.itemAtPosition(4 + i, 0)
            if item1 is not None:
                widget1 = item1.widget()
                if widget1 is not None:
                    self.comicscriptGridLayout.removeWidget(widget1)
                    widget1.deleteLater()

            item2 = self.comicscriptGridLayout.itemAtPosition(4 + i, 1)
            if item2 is not None:
                widget2 = item2.widget()
                if widget2 is not None:
                    self.comicscriptGridLayout.removeWidget(widget2)
                    widget2.deleteLater()
        self.adjustSize()

    def createParam(self):
        self.deleteParam()
        cnt = self.paramCountCombo.currentIndex()
        for i in range(cnt):
            # layout - QGridLayout - paramLabel
            paramLabel = QLabel(textSetting.textList["comicscript"]["paramNumLabel"].format(i + 1), font=self.font2)
            self.comicscriptGridLayout.addWidget(paramLabel, 4 + i, 0)
            # layout - QGridLayout - paramLineEdit
            paramLineEdit = QLineEdit(font=self.font2)
            paramLineEdit.setValidator(self.numberValidator)
            self.lineEditList.append(paramLineEdit)
            if self.mode == "modify" and i < self.comicData[1]:
                paramLineEdit.setText("{0}".format(self.comicData[2 + i]))
            self.comicscriptGridLayout.addWidget(paramLineEdit, 4 + i, 1)

    def validate(self):
        self.resultValueList = []
        self.resultValueList.append(self.cmdCombo.currentText())
        self.resultValueList.append(self.paramCountCombo.currentIndex())

        for i, lineEdit in enumerate(self.lineEditList):
            paramMsg = textSetting.textList["comicscript"]["paramNumLabel"].format(i + 1)
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            try:
                float(lineEdit.text())
            except ValueError:
                errorMsg = "{0} [{1}]".format(textSetting.textList["errorList"]["E5"], paramMsg)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return
            self.resultValueList.append(float(lineEdit.text()))

        msg = textSetting.textList["infoList"]["I21"]
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


class PasteComicscriptDialog(QDialog):
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
        frontButton = QPushButton(textSetting.textList["comicscript"]["pasteFront"], font=font2)
        frontButton.clicked.connect(self.frontInsert)
        buttonLayout.addWidget(frontButton)
        # layout - buttonLayout - backButton
        backButton = QPushButton(textSetting.textList["comicscript"]["pasteBack"], font=font2)
        backButton.clicked.connect(self.backInsert)
        buttonLayout.addWidget(backButton)
        # layout - buttonLayout - cancelButton
        cancelButton = QPushButton(textSetting.textList["comicscript"]["pasteCancel"], font=font2)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

    def frontInsert(self):
        super().accept()
        self.insertPos = 0

    def backInsert(self):
        super().accept()
        self.insertPos = 1
