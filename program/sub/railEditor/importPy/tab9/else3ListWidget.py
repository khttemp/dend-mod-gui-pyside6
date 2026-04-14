import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
import program.sub.railEditor.importPy.tab9.else3CsvProcess as else3CsvProcess

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QFileDialog
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression


mb = customMessageBoxWidget.CustomMessageBox()


class Else3ListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc, selectId):
        super().__init__()
        self.decryptFile = decryptFile
        self.else3List = decryptFile.else3List
        self.reloadFunc = reloadFunc
        self.selectId = selectId
        self.copyElse3Info = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        labelWidth = 66
        labelHeight = 30
        csvButtonWidth = 120
        buttonWidth = 180
        buttonHeight = 28

        mainLayout = QVBoxLayout(self)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 2)

        # headerLeft
        headerLeftLayout = QVBoxLayout()
        headerLeftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerLeftLayout, 3)
        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["railEditor"]["selectNum"], font=font2)
        headerSelectLayout.addWidget(selectLabel)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedSize(labelWidth, labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel)
        headerSelectLayout.addStretch()

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.title = textSetting.textList["railEditor"]["else3Label"]
            # space
            headerLeftLayout.addSpacing(13)
            # headerLeft - csvLayout
            headerCsvLayout = QHBoxLayout()
            headerLeftLayout.addLayout(headerCsvLayout)
            # headerLeft - csvLayout - csvExtractButton
            csvExtractButton = QPushButton(textSetting.textList["railEditor"]["else3ExtractCsvLabel"])
            csvExtractButton.setFixedSize(csvButtonWidth, buttonHeight)
            csvExtractButton.setEnabled(True)
            csvExtractButton.clicked.connect(self.else3ExtractCsv)
            headerCsvLayout.addWidget(csvExtractButton)
            # headerLeft - csvLayout - csvLoadAndSaveButton
            csvLoadAndSaveButton = QPushButton(textSetting.textList["railEditor"]["else3LoadAndSaveCsvLabel"])
            csvLoadAndSaveButton.setFixedSize(csvButtonWidth, buttonHeight)
            csvLoadAndSaveButton.setEnabled(True)
            csvLoadAndSaveButton.clicked.connect(self.else3LoadAndSaveCsv)
            headerCsvLayout.addWidget(csvLoadAndSaveButton)
        else:
            self.title = textSetting.textList["railEditor"]["camLabel"]

        # stretch
        headerLayout.addStretch(1)
        # headerRight
        headerRightLayout = QVBoxLayout()
        headerLayout.addLayout(headerRightLayout, 9)
        # headerRight - buttonLayout1
        headerRightButtonLayout1 = QHBoxLayout()
        headerRightButtonLayout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout1)
        # headerRight - buttonLayout1 - editButton
        self.editLineButton = QPushButton(textSetting.textList["railEditor"]["commonEditLineLabel"])
        self.editLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.editLineButton.setEnabled(False)
        self.editLineButton.clicked.connect(self.editLineFunc)
        headerRightButtonLayout1.addWidget(self.editLineButton)
        # space
        headerRightButtonLayout1.addSpacing(30)
        # headerRight - buttonLayout1 - insertButton
        self.insertLineButton = QPushButton(textSetting.textList["railEditor"]["commonInsertLineLabel"])
        self.insertLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertLineButton.setEnabled(False)
        self.insertLineButton.clicked.connect(self.insertLineFunc)
        headerRightButtonLayout1.addWidget(self.insertLineButton)
        # space
        headerRightButtonLayout1.addSpacing(30)
        # headerRight - buttonLayout1 - deleteButton
        self.deleteLineButton = QPushButton(textSetting.textList["railEditor"]["commonDeleteLineLabel"])
        self.deleteLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteLineButton.setEnabled(False)
        self.deleteLineButton.clicked.connect(self.deleteLineFunc)
        headerRightButtonLayout1.addWidget(self.deleteLineButton)
        # space
        headerRightLayout.addSpacing(15)
        # headerRight - buttonLayout2
        headerRightButtonLayout2 = QHBoxLayout()
        headerRightButtonLayout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout2)
        # headerRight - buttonLayout2 - copyButton
        self.copyLineButton = QPushButton(textSetting.textList["railEditor"]["commonCopyLineLabel"])
        self.copyLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyLineButton.setEnabled(False)
        self.copyLineButton.clicked.connect(self.copyLineFunc)
        headerRightButtonLayout2.addWidget(self.copyLineButton)
        # space
        headerRightButtonLayout2.addSpacing(30)
        # headerRight - buttonLayout2 - pasteButton
        self.pasteLineButton = QPushButton(textSetting.textList["railEditor"]["commonPasteLineLabel"])
        self.pasteLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.pasteLineButton.setEnabled(False)
        self.pasteLineButton.clicked.connect(self.pasteLineFunc)
        headerRightButtonLayout2.addWidget(self.pasteLineButton)
        # space
        headerRightButtonLayout2.addSpacing(30)
        # headerRight - buttonLayout2 - listModifyButton
        self.listModifyButton = QPushButton(textSetting.textList["railEditor"]["editElse3InfoListLabel"])
        self.listModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.listModifyButton.setEnabled(False)
        self.listModifyButton.clicked.connect(self.listModifyFunc)
        headerRightButtonLayout2.addWidget(self.listModifyButton)
        # stretch
        headerLayout.addStretch(1)
        # space
        mainLayout.addSpacing(5)
        # contentLayout
        contentLayout = QVBoxLayout()
        mainLayout.addLayout(contentLayout, 11)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

        self.createElse3Table()
        self.jumpToSelect()

    def createElse3Table(self):
        self.setElse3TableHeader()
        self.setElse3TableData()
        if len(self.else3List) == 0:
            self.insertLineButton.setEnabled(True)

    def setElse3TableHeader(self):
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            headerLabelList = [
                textSetting.textList["railEditor"]["editElse3LabelList"][0],
                textSetting.textList["railEditor"]["editElse3LabelList"][1]
            ]
        else:
            headerLabelList = [
                textSetting.textList["railEditor"]["editElse3LsLabelList"][0],
                textSetting.textList["railEditor"]["editElse3LsLabelList"][1],
                textSetting.textList["railEditor"]["editElse3LsLabelList"][2],
                textSetting.textList["railEditor"]["editElse3LsLabelList"][3]
            ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setElse3TableData(self):
        for else3Info in self.else3List:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, else3Value in enumerate(else3Info):
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    if j == 1:
                        item = QTableWidgetItem(str(len(else3Value)))
                    else:
                        item = QTableWidgetItem(str(else3Value))
                else:
                    if j == 3:
                        item = QTableWidgetItem(str(len(else3Value)))
                    else:
                        item = QTableWidgetItem(str(else3Value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.else3List):
                self.selectId = len(self.else3List) - 1
            self.contentTable.selectRow(self.selectId)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.editLineButton.setEnabled(False)
            self.insertLineButton.setEnabled(False)
            self.deleteLineButton.setEnabled(False)
            self.copyLineButton.setEnabled(False)
            self.listModifyButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.editLineButton.setEnabled(True)
        self.insertLineButton.setEnabled(True)
        self.deleteLineButton.setEnabled(True)
        self.copyLineButton.setEnabled(True)
        self.listModifyButton.setEnabled(True)

    def editLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        num = selectedItems[0].row()
        item = self.else3List[num]
        editElse3ListWidget = EditElse3ListWidget(self, textSetting.textList["railEditor"]["editElse3Label"].format(self.title), self.decryptFile, "modify", headerNameList, item)
        if editElse3ListWidget.exec() == QDialog.Accepted:
            self.else3List[num] = editElse3ListWidget.resultValueList
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc(num)

    def insertLineFunc(self):
        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            num = 0
        else:
            num = selectedItems[0].row() + 1

        editElse3ListWidget = EditElse3ListWidget(self, textSetting.textList["railEditor"]["insertElse3Label"].format(self.title), self.decryptFile, "insert", headerNameList)
        if editElse3ListWidget.exec() == QDialog.Accepted:
            self.else3List.insert(num + editElse3ListWidget.insertPos, editElse3ListWidget.resultValueList)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc(num)

    def deleteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            self.else3List.pop(num)
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc()

    def copyLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        self.copyElse3Info = copy.deepcopy(self.else3List[num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineButton.setEnabled(True)

    def pasteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteElse3ListDialog = PasteElse3ListDialog(self, textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.title), self.decryptFile, num, self.copyElse3Info)
        if pasteElse3ListDialog.exec() == QDialog.Accepted:
            self.reloadFunc(num)

    def listModifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        item = self.else3List[num]
        else3ElementWidget = Else3ElementWidget(self, textSetting.textList["railEditor"]["editElse3ElementLabel"].format(self.title), self.decryptFile, num, item)
        else3ElementWidget.exec()
        if else3ElementWidget.dirtyFlag:
            self.reloadFunc(num)

    def else3ExtractCsv(self):
        filename = self.decryptFile.filename + "_else3.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            "else3_csv (*.csv)"
        )
        if file_path:
            try:
                else3CsvProcess.extractCsv(file_path, self.else3List)
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
            except PermissionError:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def else3LoadAndSaveCsv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            "else3_csv (*.csv)"
        )
        if not file_path:
            return

        else3Obj, message = else3CsvProcess.loadCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(else3Obj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            else3List = else3Obj["data"]
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format("else3"))
            self.reloadFunc()


class EditElse3ListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, headerNameList, else3Info=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.headerNameList = headerNameList
        self.else3Info = else3Info
        self.railNoList = []
        self.insertPos = None
        self.resultValueList = []
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.else3InfoGridLayout = QGridLayout()
        layout.addLayout(self.else3InfoGridLayout)
        self.lineEditList = []

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            else3InfoLabelList = copy.deepcopy(textSetting.textList["railEditor"]["editElse3LabelList"])
            self.railNoList = [x[0] for x in self.decryptFile.else3List]
        else:
            else3InfoLabelList = copy.deepcopy(textSetting.textList["railEditor"]["editElse3LsLabelList"])
        else3InfoLabelList.pop()

        for i, else3InfoLabel in enumerate(else3InfoLabelList):
            # layout - QGridLayout - label
            else3NameLabel = QLabel(else3InfoLabel, font=self.font2)
            self.else3InfoGridLayout.addWidget(else3NameLabel, i, 0)
            # layout - QGridLayout - lineEdit
            else3InfoLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(else3InfoLineEdit)
            self.else3InfoGridLayout.addWidget(else3InfoLineEdit, i, 1)

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                else3InfoLineEdit.setValidator(integerValidator)
                if self.mode == "insert":
                    else3InfoLineEdit.setText("{0}".format(0))

                if self.mode == "modify":
                    else3InfoLineEdit.setText("{0}".format(self.else3Info[i]))
            else:
                else3InfoLineEdit.setValidator(numberValidator)
                if self.mode == "insert":
                    else3InfoLineEdit.setText("{0}".format(float(0)))

                if self.mode == "modify":
                    else3InfoLineEdit.setText("{0}".format(self.else3Info[i]))

        if self.mode == "insert":
            self.setInsertWidget(len(self.headerNameList))

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
        self.else3InfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.else3InfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.else3InfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                if i == 0:
                    isValidFlag = True
                    railNo = int(lineEdit.text())
                    if self.mode == "modify":
                        originRailNo = self.else3Info[0]
                        if originRailNo != railNo and railNo in self.railNoList:
                            isValidFlag = False
                    elif self.mode == "insert":
                        if railNo in self.railNoList:
                            isValidFlag = False

                    if not isValidFlag:
                        if self.decryptFile.game in ["BS", "CS"]:
                            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E131"].format(railNo))
                            return
                        else:
                            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["errorList"]["E132"].format(railNo), icon="warning")
                            if result != mb.OK:
                                return
                self.resultValueList.append(int(lineEdit.text()))
            else:
                self.resultValueList.append(float(lineEdit.text()))

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            if self.mode == "modify":
                originTempList = self.else3Info[1]
                self.resultValueList.append(originTempList)
            else:
                self.resultValueList.append([[0, 0, 0, 0, 0]])
        else:
            if self.mode == "modify":
                originTempList = self.else3Info[3]
                self.resultValueList.append(originTempList)
            else:
                self.resultValueList.append([])

        if self.mode == "insert":
            self.insertPos = 0
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = -1
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class PasteElse3ListDialog(QDialog):
    def __init__(self, parent, title, decryptFile, num, copyElse3Info):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.num = num
        self.copyElse3Info = copyElse3Info
        self.railNoList = [x[0] for x in self.decryptFile.else3List]

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
        frontButton = QPushButton(textSetting.textList["railEditor"]["pasteFront"], font=font2)
        frontButton.clicked.connect(self.frontInsert)
        buttonLayout.addWidget(frontButton)
        # layout - buttonLayout - backButton
        backButton = QPushButton(textSetting.textList["railEditor"]["pasteBack"], font=font2)
        backButton.clicked.connect(self.backInsert)
        buttonLayout.addWidget(backButton)
        # layout - buttonLayout - cancelButton
        cancelButton = QPushButton(textSetting.textList["railEditor"]["pasteCancel"], font=font2)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

    def frontInsert(self):
        successMsg = textSetting.textList["infoList"]["I79"]
        newRailNo = self.copyElse3Info[0]
        if self.decryptFile.game in ["BS", "CS"]:
            while newRailNo in self.railNoList:
                newRailNo -= 1
            if newRailNo < 0:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E133"])
                return
            self.copyElse3Info[0] = newRailNo
            successMsg += ("\n" + textSetting.textList["infoList"]["I140"].format(newRailNo))

        super().accept()
        self.decryptFile.else3List.insert(self.num, self.copyElse3Info)
        if not self.decryptFile.saveElse3List(self.decryptFile.else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=successMsg)

    def backInsert(self):
        successMsg = textSetting.textList["infoList"]["I79"]
        newRailNo = self.copyElse3Info[0]
        if self.decryptFile.game in ["BS", "CS"]:
            while newRailNo in self.railNoList:
                newRailNo += 1
            self.copyElse3Info[0] = newRailNo
            successMsg += ("\n" + textSetting.textList["infoList"]["I140"].format(newRailNo))

        super().accept()
        self.decryptFile.else3List.insert(self.num + 1, self.copyElse3Info)
        if not self.decryptFile.saveElse3List(self.decryptFile.else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=successMsg)


class Else3ElementWidget(QDialog):
    def __init__(self, parent, title, decryptFile, selectNum, item):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.selectNum = selectNum
        self.else3ElementList = item[-1]
        self.copyElse3ElementInfo = []
        self.resultValueList = []
        self.dirtyFlag = False

        labelWidth = 66
        labelHeight = 30
        buttonWidth = 180
        buttonHeight = 28
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.resize(720, 360)

        mainLayout = QVBoxLayout(self)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 2)

        # headerLeft
        headerLeftLayout = QVBoxLayout()
        headerLeftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(15)
        headerLayout.addLayout(headerLeftLayout)
        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["railEditor"]["selectNum"], font=font2)
        headerSelectLayout.addWidget(selectLabel)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedSize(labelWidth, labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel)
        headerSelectLayout.addStretch()

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.title = textSetting.textList["railEditor"]["else3Label"]
        else:
            self.title = textSetting.textList["railEditor"]["camLabel"]

        # space
        headerLayout.addSpacing(15)
        # stretch
        headerLayout.addStretch(1)
        # headerRight
        headerRightLayout = QVBoxLayout()
        headerLayout.addLayout(headerRightLayout)
        # headerRight - buttonLayout1
        headerRightButtonLayout1 = QHBoxLayout()
        headerRightButtonLayout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout1)
        # headerRight - buttonLayout1 - editButton
        self.editLineButton = QPushButton(textSetting.textList["railEditor"]["commonEditLineLabel"])
        self.editLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.editLineButton.setEnabled(False)
        self.editLineButton.clicked.connect(self.editLineFunc)
        headerRightButtonLayout1.addWidget(self.editLineButton)
        # space
        headerRightButtonLayout1.addSpacing(10)
        # headerRight - buttonLayout1 - insertButton
        self.insertLineButton = QPushButton(textSetting.textList["railEditor"]["commonInsertLineLabel"])
        self.insertLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertLineButton.setEnabled(False)
        self.insertLineButton.clicked.connect(self.insertLineFunc)
        headerRightButtonLayout1.addWidget(self.insertLineButton)
        # space
        headerRightButtonLayout1.addSpacing(10)
        # headerRight - buttonLayout1 - deleteButton
        self.deleteLineButton = QPushButton(textSetting.textList["railEditor"]["commonDeleteLineLabel"])
        self.deleteLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteLineButton.setEnabled(False)
        self.deleteLineButton.clicked.connect(self.deleteLineFunc)
        headerRightButtonLayout1.addWidget(self.deleteLineButton)
        # space
        headerRightLayout.addSpacing(15)
        # headerRight - buttonLayout2
        headerRightButtonLayout2 = QHBoxLayout()
        headerRightButtonLayout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout2)
        # headerRight - buttonLayout2 - copyButton
        self.copyLineButton = QPushButton(textSetting.textList["railEditor"]["commonCopyLineLabel"])
        self.copyLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.copyLineButton.setEnabled(False)
        self.copyLineButton.clicked.connect(self.copyLineFunc)
        headerRightButtonLayout2.addWidget(self.copyLineButton)
        # space
        headerRightButtonLayout2.addSpacing(10)
        # headerRight - buttonLayout2 - pasteButton
        self.pasteLineButton = QPushButton(textSetting.textList["railEditor"]["commonPasteLineLabel"])
        self.pasteLineButton.setFixedSize(buttonWidth, buttonHeight)
        self.pasteLineButton.setEnabled(False)
        self.pasteLineButton.clicked.connect(self.pasteLineFunc)
        headerRightButtonLayout2.addWidget(self.pasteLineButton)
        # space
        headerLayout.addSpacing(15)

        # space
        mainLayout.addSpacing(10)
        # contentLayout
        contentLayout = QVBoxLayout()
        mainLayout.addLayout(contentLayout)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox)

        self.createElse3ElementTable()

    def createElse3ElementTable(self):
        self.setElse3ElementTableHeader()
        self.setElse3ElementTableData()
        if len(self.else3ElementList) == 0:
            self.insertLineButton.setEnabled(True)

    def setElse3ElementTableHeader(self):
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            headerLabelList = [
                textSetting.textList["railEditor"]["editElse3ElementLabelList"][0],
                textSetting.textList["railEditor"]["editElse3ElementLabelList"][1],
                textSetting.textList["railEditor"]["editElse3ElementLabelList"][2],
                textSetting.textList["railEditor"]["editElse3ElementLabelList"][3],
                textSetting.textList["railEditor"]["editElse3ElementLabelList"][4]
            ]
        else:
            headerLabelList = [
                textSetting.textList["railEditor"]["editElse3LsElementLabelList"][0],
                textSetting.textList["railEditor"]["editElse3LsElementLabelList"][1],
                textSetting.textList["railEditor"]["editElse3LsElementLabelList"][2],
                textSetting.textList["railEditor"]["editElse3LsElementLabelList"][3],
                textSetting.textList["railEditor"]["editElse3LsElementLabelList"][4]
            ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setElse3ElementTableData(self):
        for else3ElementInfo in self.else3ElementList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, else3ElementValue in enumerate(else3ElementInfo):
                item = QTableWidgetItem(str(else3ElementValue))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self, selectId):
        if selectId is not None:
            if selectId >= len(self.else3ElementList):
                selectId = len(self.else3ElementList) - 1
            self.contentTable.selectRow(selectId)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.editLineButton.setEnabled(False)
            self.insertLineButton.setEnabled(False)
            self.deleteLineButton.setEnabled(False)
            self.copyLineButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.editLineButton.setEnabled(True)
        self.insertLineButton.setEnabled(True)
        self.deleteLineButton.setEnabled(True)
        self.copyLineButton.setEnabled(True)

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def reloadFunc(self, selectId=None):
        self.decryptFile = self.decryptFile.reload()
        self.else3ElementList = self.decryptFile.else3List[self.selectNum][-1]
        self.clearTable()
        self.createElse3ElementTable()
        self.jumpToSelect(selectId)

    def editLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        num = selectedItems[0].row()
        item = self.else3ElementList[num]
        editElse3ElementWidget = EditElse3ElementWidget(self, textSetting.textList["railEditor"]["editElse3ElementModifyLabel"].format(self.title), self.decryptFile, "modify", headerNameList, item)
        if editElse3ElementWidget.exec() == QDialog.Accepted:
            else3List = self.decryptFile.else3List
            else3List[self.selectNum][-1][num] = editElse3ElementWidget.resultValueList
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc(num)
            self.dirtyFlag = True

    def insertLineFunc(self):
        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            num = 0
        else:
            num = selectedItems[0].row() + 1

        editElse3ElementWidget = EditElse3ElementWidget(self, textSetting.textList["railEditor"]["editElse3ElementInsertLabel"].format(self.title), self.decryptFile, "insert", headerNameList)
        if editElse3ElementWidget.exec() == QDialog.Accepted:
            else3List = self.decryptFile.else3List
            else3List[self.selectNum][-1].insert(num + editElse3ElementWidget.insertPos, editElse3ElementWidget.resultValueList)
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc(num)
            self.dirtyFlag = True

    def deleteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            if len(self.else3ElementList) == 1:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E93"].format(1))
                return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            else3List = self.decryptFile.else3List
            else3List[self.selectNum][-1].pop(num)
            if not self.decryptFile.saveElse3List(else3List):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I92"].format(self.title))
            self.reloadFunc()
            self.dirtyFlag = True

    def copyLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        self.copyElse3ElementInfo = copy.deepcopy(self.decryptFile.else3List[self.selectNum][-1][num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineButton.setEnabled(True)

    def pasteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteElse3ElementDialog = PasteElse3ElementDialog(self, textSetting.textList["railEditor"]["pasteElse3InfoLabel"].format(self.title), self.decryptFile, self.selectNum, num, self.copyElse3ElementInfo)
        if pasteElse3ElementDialog.exec() == QDialog.Accepted:
            self.reloadFunc(num)
            self.dirtyFlag = True


class EditElse3ElementWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, headerNameList, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.headerNameList = headerNameList
        self.else3Element = item
        self.insertPos = None
        self.resultValueList = []
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.else3ElementGridLayout = QGridLayout()
        layout.addLayout(self.else3ElementGridLayout)
        self.lineEditList = []

        for i, else3ElementInfoLabel in enumerate(self.headerNameList):
            # layout - QGridLayout - label
            else3ElementNameLabel = QLabel(else3ElementInfoLabel, font=self.font2)
            self.else3ElementGridLayout.addWidget(else3ElementNameLabel, i, 0)
            # layout - QGridLayout - lineEdit
            else3ElementInfoLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(else3ElementInfoLineEdit)
            self.else3ElementGridLayout.addWidget(else3ElementInfoLineEdit, i, 1)

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                else3ElementInfoLineEdit.setValidator(integerValidator)
                if self.mode == "insert":
                    else3ElementInfoLineEdit.setText("{0}".format(0))

                if self.mode == "modify":
                    else3ElementInfoLineEdit.setText("{0}".format(self.else3Element[i]))
            else:
                if i == 4:
                    else3ElementInfoLineEdit.setValidator(integerValidator)
                    if self.mode == "insert":
                        else3ElementInfoLineEdit.setText("{0}".format(0))
                else:
                    else3ElementInfoLineEdit.setValidator(numberValidator)
                    if self.mode == "insert":
                        else3ElementInfoLineEdit.setText("{0}".format(float(0)))

                if self.mode == "modify":
                    else3ElementInfoLineEdit.setText("{0}".format(self.else3Element[i]))

        if self.mode == "insert":
            self.setInsertWidget(len(self.headerNameList))

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
        self.else3ElementGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.else3ElementGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.else3ElementGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                if i == 4:
                    self.resultValueList.append(int(lineEdit.text()))
                else:
                    self.resultValueList.append(float(lineEdit.text()))

        if self.mode == "insert":
            self.insertPos = 0
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = -1
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class PasteElse3ElementDialog(QDialog):
    def __init__(self, parent, title, decryptFile, selectNum, num, copyElse3ElementInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.selectNum = selectNum
        self.num = num
        self.copyElse3ElementInfo = copyElse3ElementInfo

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
        frontButton = QPushButton(textSetting.textList["railEditor"]["pasteFront"], font=font2)
        frontButton.clicked.connect(self.frontInsert)
        buttonLayout.addWidget(frontButton)
        # layout - buttonLayout - backButton
        backButton = QPushButton(textSetting.textList["railEditor"]["pasteBack"], font=font2)
        backButton.clicked.connect(self.backInsert)
        buttonLayout.addWidget(backButton)
        # layout - buttonLayout - cancelButton
        cancelButton = QPushButton(textSetting.textList["railEditor"]["pasteCancel"], font=font2)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

    def frontInsert(self):
        super().accept()
        else3List = self.decryptFile.else3List
        else3List[self.selectNum][-1].insert(self.num, self.copyElse3ElementInfo)
        if not self.decryptFile.saveElse3List(else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])

    def backInsert(self):
        super().accept()
        else3List = self.decryptFile.else3List
        else3List[self.selectNum][-1].insert(self.num + 1, self.copyElse3ElementInfo)
        if not self.decryptFile.saveElse3List(else3List):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
