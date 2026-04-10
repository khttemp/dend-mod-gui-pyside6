import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class StationNameWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc, selectId):
        super().__init__()
        self.decryptFile = decryptFile
        self.stationNameList = decryptFile.stationNameList
        self.reloadFunc = reloadFunc
        self.selectId = selectId
        self.copyStationNameInfo = []
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        labelWidth = 66
        labelHeight = 30
        buttonWidth = 200
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
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedSize(labelWidth, labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

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

        self.createStationNameTable()
        self.jumpToSelect()

    def createStationNameTable(self):
        self.setStationNameTableHeader()
        self.setStationNameTableData()
        if len(self.stationNameList) == 0:
            self.insertLineButton.setEnabled(True)

    def setStationNameTableHeader(self):
        if self.decryptFile.game in ["CS", "RS"]:
            headerLabelList = [
                textSetting.textList["railEditor"]["stationNameName"],
                textSetting.textList["railEditor"]["stationNameFlag"],
                textSetting.textList["railEditor"]["stationNameRailNo"],
                textSetting.textList["railEditor"]["stationNameF1"],
                textSetting.textList["railEditor"]["stationNameF2"],
                textSetting.textList["railEditor"]["stationNameF3"],
                textSetting.textList["railEditor"]["stationNameE1"],
                textSetting.textList["railEditor"]["stationNameE2"],
                textSetting.textList["railEditor"]["stationNameE3"],
                textSetting.textList["railEditor"]["stationNameE4"]
            ]
        elif self.decryptFile.game == "BS":
            headerLabelList = [
                textSetting.textList["railEditor"]["stationNameName"],
                textSetting.textList["railEditor"]["stationNameFlag"],
                textSetting.textList["railEditor"]["stationNameRailNo"]
            ]
        elif self.decryptFile.game == "LS":
            headerLabelList = [
                textSetting.textList["railEditor"]["stationNameName"],
                textSetting.textList["railEditor"]["stationNameFlag"],
                textSetting.textList["railEditor"]["stationNameRailNo"],
                textSetting.textList["railEditor"]["stationNameF1"],
                textSetting.textList["railEditor"]["stationNameF2"],
                textSetting.textList["railEditor"]["stationNameF3"],
                textSetting.textList["railEditor"]["stationNameF4"],
                textSetting.textList["railEditor"]["stationNameF5"],
                textSetting.textList["railEditor"]["stationNameF6"]
            ]
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.readFlag:
                headerLabelList = [
                    textSetting.textList["railEditor"]["stationNameName"],
                    textSetting.textList["railEditor"]["stationNameFlag"],
                    textSetting.textList["railEditor"]["stationNameRailNo"],
                    textSetting.textList["railEditor"]["stationNameF1"],
                    textSetting.textList["railEditor"]["stationNameF2"],
                    textSetting.textList["railEditor"]["stationNameF3"],
                    textSetting.textList["railEditor"]["stationNameF4"],
                    textSetting.textList["railEditor"]["stationNameF5"],
                    textSetting.textList["railEditor"]["stationNameF6"]
                ]
            else:
                headerLabelList = [
                    textSetting.textList["railEditor"]["stationNameName"],
                    textSetting.textList["railEditor"]["stationNameFlag"],
                    textSetting.textList["railEditor"]["stationNameF1"],
                    textSetting.textList["railEditor"]["stationNameF2"],
                    textSetting.textList["railEditor"]["stationNameF3"],
                    textSetting.textList["railEditor"]["stationNameF4"],
                    textSetting.textList["railEditor"]["stationNameF5"],
                    textSetting.textList["railEditor"]["stationNameF6"]
                ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setStationNameTableData(self):
        for stNameInfo in self.stationNameList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, stNameValue in enumerate(stNameInfo):
                if self.decryptFile.game in ["CS", "RS"]:
                    if j in [3, 4, 5]:
                        item = QTableWidgetItem(str(round(float(stNameValue), 3)))
                    else:
                        item = QTableWidgetItem(str(stNameValue))
                elif self.decryptFile.game == "BS":
                    item = QTableWidgetItem(str(stNameValue))
                elif self.decryptFile.game == "LS":
                    if j > 2:
                        item = QTableWidgetItem(str(round(float(stNameValue), 3)))
                    else:
                        item = QTableWidgetItem(str(stNameValue))
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        if j > 2:
                            item = QTableWidgetItem(str(round(float(stNameValue), 3)))
                        else:
                            item = QTableWidgetItem(str(stNameValue))
                    else:
                        if j > 1:
                            item = QTableWidgetItem(str(round(float(stNameValue), 3)))
                        else:
                            item = QTableWidgetItem(str(stNameValue))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.stationNameList):
                self.selectId = len(self.stationNameList) - 1
            self.contentTable.selectRow(self.selectId)

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

    def editLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        num = selectedItems[0].row()
        editStationNameListWidget = EditStationNameListWidget(self, textSetting.textList["railEditor"]["modifyStationNameLabel"], self.decryptFile, "modify", num, headerNameList, self.stationNameList[num])
        if editStationNameListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveStationNameInfo(num, "modify", editStationNameListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            self.reloadFunc(num)

    def insertLineFunc(self):
        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            num = 0
        else:
            num = selectedItems[0].row() + 1

        editStationNameListWidget = EditStationNameListWidget(self, textSetting.textList["railEditor"]["insertStationNameLabel"], self.decryptFile, "insert", num, headerNameList)
        if editStationNameListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveStationNameInfo(num + editStationNameListWidget.insertPos, "insert", editStationNameListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            self.reloadFunc(num)

    def deleteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            if not self.decryptFile.saveStationNameInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
            self.reloadFunc()

    def copyLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        self.copyStationNameInfo = copy.deepcopy(self.stationNameList[num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineButton.setEnabled(True)

    def pasteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteStationNameDialog = PasteStationNameDialog(self, textSetting.textList["railEditor"]["pasteStationNameLabel"], self.decryptFile, num, self.copyStationNameInfo)
        if pasteStationNameDialog.exec() == QDialog.Accepted:
            self.reloadFunc(num)


class EditStationNameListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, num, headerNameList, stationNameInfo=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.headerNameList = headerNameList
        self.stationNameInfo = stationNameInfo
        self.insertPos = 0
        self.resultValueList = []
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.stationNameGridLayout = QGridLayout()
        layout.addLayout(self.stationNameGridLayout)
        self.lineEditList = []
        for i, headerName in enumerate(self.headerNameList):
            # layout - QGridLayout - label
            stationNameInfoLabel = QLabel(headerName, font=self.font2)
            self.stationNameGridLayout.addWidget(stationNameInfoLabel, i, 0)
            # layout - QGridLayout - lineEdit
            stationNameInfoLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(stationNameInfoLineEdit)
            self.stationNameGridLayout.addWidget(stationNameInfoLineEdit, i, 1)

            if self.decryptFile.game in ["CS", "RS"]:
                if i in [3, 4, 5]:
                    stationNameInfoLineEdit.setValidator(numberValidator)
                    if self.mode == "modify":
                        stationNameInfoLineEdit.setText("{0}".format(round(float(self.stationNameInfo[i]), 3)))
                else:
                    if i > 0:
                        stationNameInfoLineEdit.setValidator(integerValidator)
                    if self.mode == "modify":
                        stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
            elif self.decryptFile.game == "BS":
                if i > 0:
                    stationNameInfoLineEdit.setValidator(integerValidator)
                if self.mode == "modify":
                    stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
            elif self.decryptFile.game == "LS":
                if i == 0:
                    if self.mode == "modify":
                        stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                elif i in [1, 2]:
                    stationNameInfoLineEdit.setValidator(integerValidator)
                    if self.mode == "modify":
                        stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                else:
                    stationNameInfoLineEdit.setValidator(numberValidator)
                    if self.mode == "modify":
                        stationNameInfoLineEdit.setText("{0}".format(round(float(self.stationNameInfo[i]), 3)))
            elif self.decryptFile.game == "LSTrial":
                if self.decryptFile.readFlag:
                    if i == 0:
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                    elif i in [1, 2]:
                        stationNameInfoLineEdit.setValidator(integerValidator)
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                    else:
                        stationNameInfoLineEdit.setValidator(numberValidator)
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(round(float(self.stationNameInfo[i]), 3)))
                else:
                    if i == 0:
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                    elif i == 1:
                        stationNameInfoLineEdit.setValidator(integerValidator)
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(self.stationNameInfo[i]))
                    else:
                        stationNameInfoLineEdit.setValidator(numberValidator)
                        if self.mode == "modify":
                            stationNameInfoLineEdit.setText("{0}".format(round(float(self.stationNameInfo[i]), 3)))

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
        self.stationNameGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.stationNameGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.stationNameGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if self.decryptFile.game in ["CS", "RS"]:
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    if i in [3, 4, 5]:
                        self.resultValueList.append(float(lineEdit.text()))
                    else:
                        self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game == "BS":
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game == "LS":
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    if i in [1, 2]:
                        self.resultValueList.append(int(lineEdit.text()))
                    else:
                        self.resultValueList.append(float(lineEdit.text()))
            elif self.decryptFile.game == "LSTrial":
                if self.decryptFile.readFlag:
                    if i == 0:
                        self.resultValueList.append(lineEdit.text())
                    else:
                        if not lineEdit.hasAcceptableInput():
                            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                            return
                        if i in [1, 2]:
                            self.resultValueList.append(int(lineEdit.text()))
                        else:
                            self.resultValueList.append(float(lineEdit.text()))
                else:
                    if i == 0:
                        self.resultValueList.append(lineEdit.text())
                    else:
                        if not lineEdit.hasAcceptableInput():
                            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                            return
                        if i == 1:
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


class PasteStationNameDialog(QDialog):
    def __init__(self, parent, title, decryptFile, num, copyStationNameInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.num = num
        self.copyStationNameInfo = copyStationNameInfo
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
        if not self.decryptFile.saveStationNameInfo(self.num, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])

    def backInsert(self):
        super().accept()
        if not self.decryptFile.saveStationNameInfo(self.num + 1, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I81"])
