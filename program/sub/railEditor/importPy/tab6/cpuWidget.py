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


class CpuWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc, selectId):
        super().__init__()
        self.decryptFile = decryptFile
        self.cpuList = decryptFile.cpuList
        self.reloadFunc = reloadFunc
        self.selectId = selectId
        self.copyCpuInfo = []
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

        self.createCpuTable()
        self.jumpToSelect()

    def createCpuTable(self):
        self.setCpuTableHeader()
        self.setCpuTableData()
        if len(self.cpuList) == 0:
            self.insertLineButton.setEnabled(True)

    def setCpuTableHeader(self):
        if self.decryptFile.game in ["BS", "RS"]:
            headerLabelList = [
                textSetting.textList["railEditor"]["cpuInfoRailNo"],
                textSetting.textList["railEditor"]["cpuInfoConst1"],
                textSetting.textList["railEditor"]["cpuInfoMode"],
                textSetting.textList["railEditor"]["cpuInfoMinLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxSpeed"],
                textSetting.textList["railEditor"]["cpuInfoMinSpeed"]
            ]
        elif self.decryptFile.game == "CS":
            headerLabelList = [
                textSetting.textList["railEditor"]["cpuInfoRailNo"],
                textSetting.textList["railEditor"]["cpuInfoConst1"],
                textSetting.textList["railEditor"]["cpuInfoMode"],
                textSetting.textList["railEditor"]["cpuInfoMinLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxSpeed"],
                textSetting.textList["railEditor"]["cpuInfoMinSpeed"],
                textSetting.textList["railEditor"]["cpuInfoDefSpeed"]
            ]
        elif self.decryptFile.game == "LS":
            headerLabelList = [
                textSetting.textList["railEditor"]["cpuInfoRailNo"],
                textSetting.textList["railEditor"]["cpuInfoList"],
                textSetting.textList["railEditor"]["cpuInfoConst1"],
                textSetting.textList["railEditor"]["cpuInfoMode"],
                textSetting.textList["railEditor"]["cpuInfoMinLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxLen"],
                textSetting.textList["railEditor"]["cpuInfoMaxSpeed"],
                textSetting.textList["railEditor"]["cpuInfoMinSpeed"],
                textSetting.textList["railEditor"]["cpuInfoDefSpeed"],
                textSetting.textList["railEditor"]["cpuInfoList2"]
            ]
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.readFlag:
                headerLabelList = [
                    textSetting.textList["railEditor"]["cpuInfoRailNo"],
                    textSetting.textList["railEditor"]["cpuInfoList"],
                    textSetting.textList["railEditor"]["cpuInfoMode"],
                    textSetting.textList["railEditor"]["cpuInfoMinLen"],
                    textSetting.textList["railEditor"]["cpuInfoMaxLen"],
                    textSetting.textList["railEditor"]["cpuInfoMaxSpeed"],
                    textSetting.textList["railEditor"]["cpuInfoMinSpeed"],
                    textSetting.textList["railEditor"]["cpuInfoDefSpeed"],
                    textSetting.textList["railEditor"]["cpuInfoList2"]
                ]
            else:
                headerLabelList = [
                    textSetting.textList["railEditor"]["cpuInfoList"],
                    textSetting.textList["railEditor"]["cpuInfoMode"],
                    textSetting.textList["railEditor"]["cpuInfoMinLen"]
                ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.decryptFile.game == "LS":
            self.contentTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        elif self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag:
            self.contentTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        else:
            self.contentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setCpuTableData(self):
        for cpuInfo in self.cpuList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, cpuValue in enumerate(cpuInfo):
                if self.decryptFile.game in ["BS", "CS", "RS"]:
                    if j > 2:
                        item = QTableWidgetItem(str(round(float(cpuValue), 3)))
                    else:
                        item = QTableWidgetItem(str(cpuValue))
                elif self.decryptFile.game == "LS":
                    if j in [1, 9]:
                        joinCpuValue = ",".join([str(round(x, 3)) for x in cpuValue])
                        item = QTableWidgetItem(joinCpuValue)
                    elif j in [4, 5, 6, 7, 8]:
                        item = QTableWidgetItem(str(round(float(cpuValue), 3)))
                    else:
                        item = QTableWidgetItem(str(cpuValue))
                elif self.decryptFile.game == "LSTrial":
                    if self.decryptFile.readFlag:
                        if j in [1, 8]:
                            joinCpuValue = ",".join([str(round(x, 3)) for x in cpuValue])
                            item = QTableWidgetItem(joinCpuValue)
                        elif j in [3, 4, 5, 6, 7]:
                            item = QTableWidgetItem(str(round(float(cpuValue), 3)))
                        else:
                            item = QTableWidgetItem(str(cpuValue))
                    else:
                        if j == 0:
                            joinCpuValue = ",".join([str(round(x, 3)) for x in cpuValue])
                            item = QTableWidgetItem(joinCpuValue)
                        elif j == 2:
                            item = QTableWidgetItem(str(round(float(cpuValue), 3)))
                        else:
                            item = QTableWidgetItem(str(cpuValue))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.cpuList):
                self.selectId = len(self.cpuList) - 1
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
        editCpuListWidget = EditCpuListWidget(self, textSetting.textList["railEditor"]["modifyCpuInfoLabel"], self.decryptFile, "modify", num, headerNameList, self.cpuList[num])
        if editCpuListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveCpuInfo(num, "modify", editCpuListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            self.reloadFunc(num)

    def insertLineFunc(self):
        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            num = 0
        else:
            num = selectedItems[0].row() + 1

        editCpuListWidget = EditCpuListWidget(self, textSetting.textList["railEditor"]["insertCpuInfoLabel"], self.decryptFile, "insert", num, headerNameList)
        if editCpuListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveCpuInfo(num + editCpuListWidget.insertPos, "insert", editCpuListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            self.reloadFunc(num)

    def deleteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            if not self.decryptFile.saveCpuInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
            self.reloadFunc()

    def copyLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        self.copyCpuInfo = copy.deepcopy(self.cpuList[num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineButton.setEnabled(True)

    def pasteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteCpuDialog = PasteCpuDialog(self, textSetting.textList["railEditor"]["pasteCpuInfoLabel"], self.decryptFile, num, self.copyCpuInfo)
        if pasteCpuDialog.exec() == QDialog.Accepted:
            self.reloadFunc(num)


class EditCpuListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, num, headerNameList, cpuInfo=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.headerNameList = headerNameList
        self.cpuInfo = cpuInfo
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
        self.cpuInfoGridLayout = QGridLayout()
        layout.addLayout(self.cpuInfoGridLayout)
        self.lineEditList = []
        rowNum = 0
        colNum = 0
        for i, headerName in enumerate(self.headerNameList):
            if self.decryptFile.game in ["BS", "CS", "RS"]:
                # layout - QGridLayout - label
                cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, i, 0)
                # layout - QGridLayout - lineEdit
                cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                if i > 2:
                    cpuNameInfoLineEdit.setValidator(numberValidator)
                else:
                    cpuNameInfoLineEdit.setValidator(integerValidator)

                if self.mode == "modify":
                    if i > 2:
                        cpuValue = round(float(self.cpuInfo[i]), 3)
                    else:
                        cpuValue = self.cpuInfo[i]
                    cpuNameInfoLineEdit.setText("{0}".format(cpuValue))
                self.lineEditList.append(cpuNameInfoLineEdit)
                self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, i, 1)
            elif self.decryptFile.game == "LS":
                if i in [0, 2, 3]:
                    # layout - QGridLayout - label
                    cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                    self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                    # layout - QGridLayout - lineEdit
                    cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                    cpuNameInfoLineEdit.setValidator(integerValidator)
                    self.lineEditList.append(cpuNameInfoLineEdit)
                    self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                    if self.mode == "modify":
                        cpuNameInfoLineEdit.setText("{0}".format(self.cpuInfo[i]))
                    rowNum += 1
                elif i in [1, 9]:
                    if i == 1:
                        tempListLen = 6
                    else:
                        tempListLen = 3

                    for j in range(tempListLen):
                        # layout - QGridLayout - label
                        cpuNameInfoLabel = QLabel(textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=self.font2)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                        # layout - QGridLayout - lineEdit
                        cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                        cpuNameInfoLineEdit.setValidator(numberValidator)
                        self.lineEditList.append(cpuNameInfoLineEdit)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                        if self.mode == "modify":
                            cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i][j]), 3)))
                        rowNum += 1
                    colNum += 1
                    rowNum = 0
                else:
                    # layout - QGridLayout - label
                    cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                    self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                    # layout - QGridLayout - lineEdit
                    cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                    cpuNameInfoLineEdit.setValidator(numberValidator)
                    self.lineEditList.append(cpuNameInfoLineEdit)
                    self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                    if self.mode == "modify":
                        cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i]), 3)))
                    rowNum += 1
            elif self.decryptFile.game == "LSTrial":
                rowNum = 0
                colNum = 0
                if self.decryptFile.readFlag:
                    if i in [0, 2]:
                        # layout - QGridLayout - label
                        cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                        # layout - QGridLayout - lineEdit
                        cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                        cpuNameInfoLineEdit.setValidator(integerValidator)
                        self.lineEditList.append(cpuNameInfoLineEdit)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                        if self.mode == "modify":
                            cpuNameInfoLineEdit.setText("{0}".format(self.cpuInfo[i]))
                        rowNum += 1
                    elif i in [1, 8]:
                        if i == 1:
                            tempListLen = 6
                        else:
                            tempListLen = 3

                        for j in range(tempListLen):
                            # layout - QGridLayout - label
                            cpuNameInfoLabel = QLabel(textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=self.font2)
                            self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                            # layout - QGridLayout - lineEdit
                            cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                            cpuNameInfoLineEdit.setValidator(numberValidator)
                            self.lineEditList.append(cpuNameInfoLineEdit)
                            self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                            if self.mode == "modify":
                                cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i][j]), 3)))
                            rowNum += 1
                        colNum += 1
                        rowNum = 0
                    else:
                        # layout - QGridLayout - label
                        cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                        # layout - QGridLayout - lineEdit
                        cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                        cpuNameInfoLineEdit.setValidator(numberValidator)
                        self.lineEditList.append(cpuNameInfoLineEdit)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                        if self.mode == "modify":
                            cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i]), 3)))
                        rowNum += 1
                else:
                    if i == 1:
                        # layout - QGridLayout - label
                        cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                        # layout - QGridLayout - lineEdit
                        cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                        cpuNameInfoLineEdit.setValidator(integerValidator)
                        self.lineEditList.append(cpuNameInfoLineEdit)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                        if self.mode == "modify":
                            cpuNameInfoLineEdit.setText("{0}".format(self.cpuInfo[i]))
                        rowNum += 1
                    elif i == 0:
                        tempListLen = 6

                        for j in range(tempListLen):
                            # layout - QGridLayout - label
                            cpuNameInfoLabel = QLabel(textSetting.textList["railEditor"]["cpuInfoLsListLabel"].format(colNum + 1, j), font=self.font2)
                            self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                            # layout - QGridLayout - lineEdit
                            cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                            cpuNameInfoLineEdit.setValidator(numberValidator)
                            self.lineEditList.append(cpuNameInfoLineEdit)
                            self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                            if self.mode == "modify":
                                cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i][j]), 3)))
                            rowNum += 1
                        colNum += 1
                        rowNum = 0
                    else:
                        # layout - QGridLayout - label
                        cpuNameInfoLabel = QLabel(headerName, font=self.font2)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLabel, rowNum, 2*colNum)
                        # layout - QGridLayout - lineEdit
                        cpuNameInfoLineEdit = QLineEdit(font=self.font2)
                        cpuNameInfoLineEdit.setValidator(numberValidator)
                        self.lineEditList.append(cpuNameInfoLineEdit)
                        self.cpuInfoGridLayout.addWidget(cpuNameInfoLineEdit, rowNum, 2*colNum + 1)

                        if self.mode == "modify":
                            cpuNameInfoLineEdit.setText("{0}".format(round(float(self.cpuInfo[i]), 3)))
                        rowNum += 1

        if self.mode == "insert":
            if self.decryptFile.game == "LSTrial" and not self.decryptFile.readFlag:
                self.setInsertWidget(6)
            else:
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
        self.cpuInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.cpuInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.cpuInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        tempList = []
        tempList2 = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return

            if self.decryptFile.game in ["BS", "CS", "RS"]:
                if i > 2:
                    self.resultValueList.append(float(lineEdit.text()))
                else:
                    self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game == "LS":
                if i in [0, 7, 8]:
                    self.resultValueList.append(int(lineEdit.text()))
                elif i in [1, 2, 3, 4, 5, 6]:
                    tempList.append(float(lineEdit.text()))
                    if i == 6:
                        self.resultValueList.append(tempList)
                        tempList = []
                elif i in [9, 10, 11, 12, 13]:
                    self.resultValueList.append(float(lineEdit.text()))
                elif i in [14, 15, 16]:
                    tempList2.append(float(lineEdit.text()))
                    if i == 16:
                        self.resultValueList.append(tempList2)
                        tempList2 = []
            elif self.decryptFile.game == "LSTrial":
                if self.decryptFile.readFlag:
                    if i in [0, 7]:
                        self.resultValueList.append(int(lineEdit.text()))
                    elif i in [1, 2, 3, 4, 5, 6]:
                        tempList.append(float(lineEdit.text()))
                        if i == 6:
                            self.resultValueList.append(tempList)
                            tempList = []
                    elif i in [8, 9, 10, 11, 12]:
                        self.resultValueList.append(float(lineEdit.text()))
                    elif i in [13, 14, 15]:
                        tempList2.append(float(lineEdit.text()))
                        if i == 15:
                            self.resultValueList.append(tempList2)
                            tempList2 = []
                else:
                    if i in [0, 1, 2, 3, 4, 5]:
                        tempList.append(float(lineEdit.text()))
                        if i == 5:
                            self.resultValueList.append(tempList)
                            tempList = []
                    elif i == 6:
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


class PasteCpuDialog(QDialog):
    def __init__(self, parent, title, decryptFile, num, copyCpuInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.num = num
        self.copyCpuInfo = copyCpuInfo
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
        if not self.decryptFile.saveCpuInfo(self.num, "insert", self.copyCpuInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
        self.reloadFlag = True

    def backInsert(self):
        super().accept()
        if not self.decryptFile.saveCpuInfo(self.num + 1, "insert", self.copyCpuInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I84"])
        self.reloadFlag = True
