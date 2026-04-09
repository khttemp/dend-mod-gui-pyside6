import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QPushButton,
    QComboBox, QMenuBar, QListWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QSizePolicy
)
from PySide6.QtGui import QFont, QAction, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class SmfListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc, selectId):
        super().__init__()
        self.decryptFile = decryptFile
        self.smfList = decryptFile.smfList
        self.reloadFunc = reloadFunc
        self.selectId = selectId
        self.copySmfInfo = []
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
        # space
        headerLeftLayout.addSpacing(15)
        # headerLeft - usedModelLayout
        headerUsedModelLayout = QHBoxLayout()
        headerUsedModelLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        headerLeftLayout.addLayout(headerUsedModelLayout)
        # headerLeft - usedModelLayout - railLabel
        self.usedRailLabel = QLabel("", font=font2)
        self.usedRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.usedRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usedRailLabel.setFixedSize(labelWidth, labelHeight)
        headerUsedModelLayout.addWidget(self.usedRailLabel)
        # space
        headerUsedModelLayout.addSpacing(20)
        # headerLeft - usedModelLayout - ambLabel
        self.usedAmbLabel = QLabel("", font=font2)
        self.usedAmbLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.usedAmbLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usedAmbLabel.setFixedSize(labelWidth, labelHeight)
        headerUsedModelLayout.addWidget(self.usedAmbLabel)

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
        # headerRight - buttonLayout2 - listModifyButton
        if self.decryptFile.game in ["LSTrial", "LS", "BS"]:
            # space
            headerRightButtonLayout2.addSpacing(30)
            self.listModifyButton = QPushButton(textSetting.textList["railEditor"]["editSmfElementListLabel"])
            self.listModifyButton.setFixedSize(buttonWidth, buttonHeight)
            self.listModifyButton.setEnabled(False)
            self.listModifyButton.clicked.connect(self.listModifyFunc)
            headerRightButtonLayout2.addWidget(self.listModifyButton)
        # stretch
        headerLayout.addStretch(1)

        # contentLayout
        contentLayout = QVBoxLayout()
        mainLayout.addLayout(contentLayout, 11)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

        self.createSmfTable()
        self.jumpToSelect()

    def createSmfTable(self):
        self.setSmfTableHeader()
        self.setSmfTableData()
        if len(self.smfList) == 0:
            self.insertLineButton.setEnabled(True)

    def setSmfTableHeader(self):
        if self.decryptFile.game in ["CS", "RS"]:
            headerLabelList = [
                textSetting.textList["railEditor"]["smfInfoName"],
                textSetting.textList["railEditor"]["smfInfoFlag1"],
                textSetting.textList["railEditor"]["smfInfoFlag2"],
                textSetting.textList["railEditor"]["smfInfoLength"],
                textSetting.textList["railEditor"]["smfInfoMesh1"],
                textSetting.textList["railEditor"]["smfInfoMesh2"],
                textSetting.textList["railEditor"]["smfInfoKasenchuNo"],
                textSetting.textList["railEditor"]["smfInfoKasenNo"]
            ]
        elif self.decryptFile.game == "BS":
            headerLabelList = [
                textSetting.textList["railEditor"]["smfInfoName"],
                textSetting.textList["railEditor"]["smfInfoLength"],
                textSetting.textList["railEditor"]["smfInfoMesh1"],
                textSetting.textList["railEditor"]["smfInfoMesh2"],
                textSetting.textList["railEditor"]["smfInfoElementList"]
            ]
        elif self.decryptFile.game in ["LSTrial", "LS"]:
            if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
                headerLabelList = [
                    textSetting.textList["railEditor"]["smfInfoName"],
                    textSetting.textList["railEditor"]["smfInfoLength"],
                    textSetting.textList["railEditor"]["smfInfoE1"],
                    textSetting.textList["railEditor"]["smfInfoElementList"]
                ]
            else:
                headerLabelList = [
                    textSetting.textList["railEditor"]["smfInfoName"],
                    textSetting.textList["railEditor"]["smfInfoLength"],
                    textSetting.textList["railEditor"]["smfInfoElementList"]
                ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setSmfTableData(self):
        useModelListObj = self.getUseModelList()
        for i, smfInfo in enumerate(self.smfList):
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, smfValue in enumerate(smfInfo):
                if self.decryptFile.game in ["CS", "RS"]:
                    if j in [1, 2]:
                        item = QTableWidgetItem(self.toHex(smfValue))
                    else:
                        item = QTableWidgetItem(str(smfValue))
                elif self.decryptFile.game == "BS":
                    if j == 4:
                        item = QTableWidgetItem(str(len(smfValue)))
                    else:
                        item = QTableWidgetItem(str(smfValue))
                elif self.decryptFile.game in ["LSTrial", "LS"]:
                    if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
                        if j == 3:
                            if len(smfValue) == 0:
                                item = QTableWidgetItem(str(-1))
                            else:
                                item = QTableWidgetItem(str(len(smfValue)))
                        else:        
                            item = QTableWidgetItem(str(smfValue))
                    else:
                        if j == 2:
                            if len(smfValue) == 0:
                                item = QTableWidgetItem(str(-1))
                            else:
                                item = QTableWidgetItem(str(len(smfValue)))
                        else:
                            item = QTableWidgetItem(str(smfValue))

                if j == 0:
                    modelName = smfValue
                    if modelName in useModelListObj["rail"] and modelName in useModelListObj["amb"]:
                        category = "allUse"
                    elif modelName not in useModelListObj["rail"] and modelName not in useModelListObj["amb"]:
                        category = "notUse"
                    elif modelName in useModelListObj["rail"]:
                        category = "rail"
                    else:
                        category = "amb"
                    item.setData(Qt.UserRole, category)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def getUseModelList(self):
        mdlInfoObj = {}
        railMdlSet = set()
        ambMdlSet = set()

        # rail
        for rail in self.decryptFile.railList:
            if self.decryptFile.game != "LSTrial" and len(rail) < 15:
                continue

            if self.decryptFile.game == "LSTrial":
                if self.decryptFile.oldFlag:
                    mdlNo = rail[9]
                    if len(self.decryptFile.smfList) > mdlNo:
                        mdlName = self.decryptFile.smfList[mdlNo][0]
                        railMdlSet.add(mdlName)

                    kasenNo = rail[10]
                    if kasenNo != -1:
                        if len(self.decryptFile.smfList) > kasenNo:
                            kasenName = self.decryptFile.smfList[kasenNo][0]
                            railMdlSet.add(kasenName)
                else:
                    mdlNo = rail[7]
                    if len(self.decryptFile.smfList) > mdlNo:
                        mdlName = self.decryptFile.smfList[mdlNo][0]
                        railMdlSet.add(mdlName)

                    offset = 0
                    if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                        if rail[8] == -1:
                            offset = 3
                    kasenchuNo = rail[9 + offset]
                    kasenNo = rail[10 + offset]
                    fixAmbNo = rail[11 + offset]

                    if kasenchuNo != -1:
                        if len(self.decryptFile.smfList) > kasenchuNo:
                            kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                            railMdlSet.add(kasenchuName)
                    if kasenNo != -1:
                        if len(self.decryptFile.smfList) > kasenNo:
                            kasenName = self.decryptFile.smfList[kasenNo][0]
                            railMdlSet.add(kasenName)
                    if fixAmbNo != -1:
                        if len(self.decryptFile.smfList) > fixAmbNo:
                            fixAmbName = self.decryptFile.smfList[fixAmbNo][0]
                            ambMdlSet.add(fixAmbName)
            elif self.decryptFile.game == "LS":
                offset = 0
                if self.decryptFile.ver == "DEND_MAP_VER0101":
                    offset = 2
                mdlNo = rail[7 + offset]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

                if rail[8 + offset] == -1:
                    kasenchuNo = rail[12 + offset]
                    kasenNo = rail[13 + offset]
                    fixAmbNo = rail[14 + offset]
                else:
                    kasenchuNo = rail[9 + offset]
                    kasenNo = rail[10 + offset]
                    fixAmbNo = rail[11 + offset]

                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
                if kasenNo != -1:
                    if len(self.decryptFile.smfList) > kasenNo:
                        kasenName = self.decryptFile.smfList[kasenNo][0]
                        railMdlSet.add(kasenName)
                if fixAmbNo != -1:
                    if len(self.decryptFile.smfList) > fixAmbNo:
                        fixAmbName = self.decryptFile.smfList[fixAmbNo][0]
                        ambMdlSet.add(fixAmbName)
            elif self.decryptFile.game == "BS":
                mdlNo = rail[6]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

                kasenNo = rail[7]
                kasenchuNo = rail[8]
                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
                if kasenNo != -1:
                    if len(self.decryptFile.smfList) > kasenNo:
                        kasenName = self.decryptFile.smfList[kasenNo][0]
                        railMdlSet.add(kasenName)
            else:
                flag = rail[13]
                if flag & 128 > 0:
                    continue
                mdlNo = rail[6]
                if len(self.decryptFile.smfList) > mdlNo:
                    mdlName = self.decryptFile.smfList[mdlNo][0]
                    railMdlSet.add(mdlName)

                kasenNo = rail[7]
                if kasenNo == -2:
                    pass
                elif kasenNo == -1:
                    if len(self.decryptFile.smfList) > mdlNo:
                        kasenNo = self.decryptFile.smfList[mdlNo][-1]
                        if kasenNo != 255:
                            if len(self.decryptFile.smfList) > kasenNo:
                                kasenName = self.decryptFile.smfList[kasenNo][0]
                                railMdlSet.add(kasenName)
                else:
                    if len(self.decryptFile.smfList) > kasenNo:
                        kasenName = self.decryptFile.smfList[kasenNo][0]
                        railMdlSet.add(kasenName)

                kasenchuNo = rail[8]
                if kasenchuNo == -2:
                    pass
                elif kasenchuNo == -1:
                    if len(self.decryptFile.smfList) > mdlNo:
                        kasenchuNo = self.decryptFile.smfList[mdlNo][-2]
                        if kasenchuNo != 255:
                            if len(self.decryptFile.smfList) > kasenchuNo:
                                kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                                railMdlSet.add(kasenchuName)

                        kasenNo = self.decryptFile.smfList[mdlNo][-1]
                        if kasenNo != 255:
                            if len(self.decryptFile.smfList) > kasenNo:
                                kasenName = self.decryptFile.smfList[kasenNo][0]
                                railMdlSet.add(kasenName)
                else:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
        if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag:
            for amb in self.decryptFile.ambList:
                kasenchuNo = amb[10]
                if kasenchuNo != -1:
                    if len(self.decryptFile.smfList) > kasenchuNo:
                        kasenchuName = self.decryptFile.smfList[kasenchuNo][0]
                        railMdlSet.add(kasenchuName)
        mdlInfoObj["rail"] = railMdlSet

        # amb
        for amb in self.decryptFile.ambList:
            if self.decryptFile.game == "LSTrial":
                if self.decryptFile.oldFlag:
                    leftAmbMdlNo = amb[8]
                    rightAmbMdlNo = amb[9]
                    fixAmbMdlNo = amb[11]
                    if leftAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > leftAmbMdlNo:
                            kasenName = self.decryptFile.smfList[leftAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                    if rightAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > rightAmbMdlNo:
                            kasenName = self.decryptFile.smfList[rightAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                    if fixAmbMdlNo != -1:
                        if len(self.decryptFile.smfList) > fixAmbMdlNo:
                            kasenName = self.decryptFile.smfList[fixAmbMdlNo][0]
                            ambMdlSet.add(kasenName)
                else:
                    if len(amb) > 3:
                        ambMdlNo = amb[3]
                        if ambMdlNo != 0:
                            if len(self.decryptFile.smfList) > ambMdlNo:
                                ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                                ambMdlSet.add(ambMdlName)
            elif self.decryptFile.game == "LS":
                if len(amb) > 3:
                    ambMdlNo = amb[3]
                    if ambMdlNo != 0:
                        if len(self.decryptFile.smfList) > ambMdlNo:
                            ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                            ambMdlSet.add(ambMdlName)
            elif self.decryptFile.game == "BS":
                if len(amb) > 3:
                    ambMdlNo = amb[3]
                    if ambMdlNo >= 0 and len(self.decryptFile.smfList) > ambMdlNo:
                        ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                        ambMdlSet.add(ambMdlName)
            else:
                if len(amb) > 23:
                    ambMdlNo = amb[12]
                    if len(self.decryptFile.smfList) > ambMdlNo:
                        ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                        ambMdlSet.add(ambMdlName)

                    childcnt = amb[12 + 11]
                    for i in range(childcnt):
                        ambMdlNo = amb[24 + i*11]
                        if len(self.decryptFile.smfList) > ambMdlNo:
                            ambMdlName = self.decryptFile.smfList[ambMdlNo][0]
                            ambMdlSet.add(ambMdlName)

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            for else3Info in self.decryptFile.else3List:
                for j in range(len(else3Info[1])):
                    tempList = else3Info[1][j]
                    if tempList[3] == -1:
                        ambMdlName = self.decryptFile.smfList[tempList[4]][0]
                        ambMdlSet.add(ambMdlName)
        mdlInfoObj["amb"] = ambMdlSet
        return mdlInfoObj

    def toHex(self, num):
        return "0x{0:02x}".format(num)

    def setUsedModelLabel(self, item):
        category = item.data(Qt.UserRole)
        if category == "notUse":
            self.usedRailLabel.setText("")
            self.usedAmbLabel.setText("")
        elif category == "allUse":
            self.usedRailLabel.setText(textSetting.textList["railEditor"]["usedRail"])
            self.usedAmbLabel.setText(textSetting.textList["railEditor"]["usedAmb"])
        elif category == "rail":
            self.usedRailLabel.setText(textSetting.textList["railEditor"]["usedRail"])
            self.usedAmbLabel.setText("")
        elif category == "amb":
            self.usedRailLabel.setText("")
            self.usedAmbLabel.setText(textSetting.textList["railEditor"]["usedAmb"])

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.smfList):
                self.selectId = len(self.smfList) - 1
            self.contentTable.selectRow(self.selectId)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.usedRailLabel.setText("")
            self.usedAmbLabel.setText("")
            self.editLineButton.setEnabled(False)
            self.insertLineButton.setEnabled(False)
            self.deleteLineButton.setEnabled(False)
            self.copyLineButton.setEnabled(False)
            if self.decryptFile.game in ["LSTrial", "LS", "BS"]:
                self.listModifyButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.setUsedModelLabel(selectedItems[0])
        self.editLineButton.setEnabled(True)
        self.insertLineButton.setEnabled(True)
        self.deleteLineButton.setEnabled(True)
        self.copyLineButton.setEnabled(True)
        if self.decryptFile.game in ["LSTrial", "LS", "BS"]:
            self.listModifyButton.setEnabled(True)

    def editLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        num = selectedItems[0].row()
        editSmfListWidget = EditSmfListWidget(self, textSetting.textList["railEditor"]["modifySmfInfo"], self.decryptFile, "modify", num, headerNameList, self.smfList[num])
        if editSmfListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveSmfInfo(num, "modify", editSmfListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            self.reloadFunc(num)

    def insertLineFunc(self):
        headerNameList = [self.contentTable.horizontalHeaderItem(i).text() for i in range(self.contentTable.columnCount())]
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            num = 0
        else:
            num = selectedItems[0].row() + 1

        editSmfListWidget = EditSmfListWidget(self, textSetting.textList["railEditor"]["insertSmfInfo"], self.decryptFile, "insert", num, headerNameList)
        if editSmfListWidget.exec() == QDialog.Accepted:
            if not self.decryptFile.saveSmfInfo(num + editSmfListWidget.insertPos, "insert", editSmfListWidget.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            self.reloadFunc(num + editSmfListWidget.insertPos)

    def deleteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I9"], icon="warning")
        if result == mb.OK:
            if not self.decryptFile.saveSmfInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])
            self.reloadFunc()

    def copyLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        self.copySmfInfo = copy.deepcopy(self.smfList[num])
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I12"])
        self.pasteLineButton.setEnabled(True)

    def pasteLineFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        pasteSmfListDialog = PasteSmfListDialog(self, textSetting.textList["railEditor"]["pasteSmfInfo"], self.decryptFile, num, self.copySmfInfo)
        if pasteSmfListDialog.exec() == QDialog.Accepted:
            self.reloadFunc(num)

    def listModifyFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        num = selectedItems[0].row()
        originTempList = self.smfList[num][-1]
        editListWidget = EditListWidget(self, textSetting.textList["railEditor"]["editSmfElementList"], self.decryptFile, originTempList)
        if editListWidget.exec() == QDialog.Accepted:
            if editListWidget.reloadFlag:
                if not self.decryptFile.saveSmfListElement(num, editListWidget.tempList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I80"])
                self.reloadFunc(num)


class EditSmfListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, num, headerNameList, smfInfo=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.headerNameList = headerNameList
        self.smfInfo = smfInfo
        self.insertPos = 0
        self.resultValueList = []
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.smfListGridLayout = QGridLayout()
        layout.addLayout(self.smfListGridLayout)
        self.lineEditList = []
        if self.decryptFile.game in ["CS", "RS"]:
            modelFlagList = textSetting.textList["railEditor"]["modelFlagList"]
            for i, headerName in enumerate(self.headerNameList):
                # layout - QGridLayout - label
                smfInfoLabel = QLabel(headerName, font=self.font2)
                self.smfListGridLayout.addWidget(smfInfoLabel, i, 0)
                # layout - QGridLayout - lineEdit, menu
                if i in [1, 2]:
                    menubar = QMenuBar()
                    menu = menubar.addMenu(textSetting.textList["railEditor"]["setSmfSwitch"])
                    for modelFlagValue in reversed(modelFlagList[i - 1]):
                        action = QAction(modelFlagValue, self)
                        action.setCheckable(True)
                        menu.addAction(action)
                    self.lineEditList.append(menu)
                    self.smfListGridLayout.addWidget(menubar, i, 1)

                    if self.mode == "modify":
                        for j, action in enumerate(reversed(menu.actions())):
                            if self.smfInfo[i] & (2**j) == 0:
                                action.setChecked(False)
                            else:
                                action.setChecked(True)
                else:
                    smfInfoLineEdit = QLineEdit(font=self.font2)
                    if i > 2:
                        smfInfoLineEdit.setValidator(integerValidator)
                    self.lineEditList.append(smfInfoLineEdit)
                    self.smfListGridLayout.addWidget(smfInfoLineEdit, i, 1)
                    if self.mode == "modify":
                        smfInfoLineEdit.setText("{0}".format(self.smfInfo[i]))
                    elif self.mode == "insert":
                        if i > 2:
                            if i == 3:
                                default = 8
                            else:
                                default = 255
                            smfInfoLineEdit.setText("{0}".format(default))
        else:
            self.headerNameList.pop()
            for i, headerName in enumerate(self.headerNameList):
                # layout - QGridLayout - label
                smfInfoLabel = QLabel(headerName, font=self.font2)
                self.smfListGridLayout.addWidget(smfInfoLabel, i, 0)
                # layout - QGridLayout - lineEdit
                smfInfoLineEdit = QLineEdit(font=self.font2)
                if i > 0:
                    smfInfoLineEdit.setValidator(integerValidator)
                self.lineEditList.append(smfInfoLineEdit)
                self.smfListGridLayout.addWidget(smfInfoLineEdit, i, 1)
                if self.mode == "modify":
                    smfInfoLineEdit.setText("{0}".format(self.smfInfo[i]))
                elif self.mode == "insert":
                    if i > 0:
                        if i == 1:
                            default = 8
                        else:
                            default = 255
                        smfInfoLineEdit.setText("{0}".format(default))

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
        self.smfListGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.smfListGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.smfListGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if self.decryptFile.game in ["CS", "RS"]:
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                elif i in [1, 2]:
                    res = 0
                    menu = lineEdit
                    for j, action in enumerate(reversed(menu.actions())):
                        if action.isChecked():
                            res |= (2**j)
                    self.resultValueList.append(res)
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game == "BS":
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    self.resultValueList.append(int(lineEdit.text()))
            elif self.decryptFile.game in ["LSTrial", "LS"]:
                if i == 0:
                    self.resultValueList.append(lineEdit.text())
                else:
                    if not lineEdit.hasAcceptableInput():
                        mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                        return
                    self.resultValueList.append(int(lineEdit.text()))

        if self.decryptFile.game == "BS":
            if self.mode == "modify":
                originTempList = self.decryptFile.smfList[self.num][4]
                self.resultValueList.append(originTempList)
            else:
                self.resultValueList.append([])
        elif self.decryptFile.game in ["LSTrial", "LS"]:
            if self.mode == "modify":
                if self.decryptFile.game == "LS" or (self.decryptFile.game == "LSTrial" and self.decryptFile.readFlag):
                    originTempList = self.decryptFile.smfList[self.num][3]
                else:
                    originTempList = self.decryptFile.smfList[self.num][2]
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


class PasteSmfListDialog(QDialog):
    def __init__(self, parent, title, decryptFile, num, copySmfInfo):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.num = num
        self.copySmfInfo = copySmfInfo
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
        if not self.decryptFile.saveSmfInfo(self.num, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])

    def backInsert(self):
        super().accept()
        if not self.decryptFile.saveSmfInfo(self.num + 1, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I79"])


class EditListWidget(QDialog):
    def __init__(self, parent, title, decryptFile, modifyList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.tempList = copy.deepcopy(modifyList)
        self.dirtyFlag = False
        self.reloadFlag = False
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - buttonLayout
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        # layout - buttonLayout - modifyButton
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

        # layout - QListWidget
        self.modifyListWidget = QListWidget(font=font2)
        displayModifyList = self.setListboxInfo(self.tempList)
        self.modifyListWidget.addItems(displayModifyList)
        self.modifyListWidget.setMinimumWidth(self.getMaxWidth() + 20)
        self.modifyListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        layout.addWidget(self.modifyListWidget, stretch=1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setListboxInfo(self, tempList):
        displayModifyList = []
        if len(tempList) > 0:
            for i in range(len(tempList)):
                tempInfo = tempList[i]
                displayModifyList.append("{0:02d}→{1}".format(i, tempInfo))
        else:
            displayModifyList = [textSetting.textList["railEditor"]["noList"]]
        return displayModifyList

    def getMaxWidth(self):
        maxWidth = 0
        for i in range(self.modifyListWidget.count()):
            size = self.modifyListWidget.sizeHintForIndex(self.modifyListWidget.model().index(i, 0))
            if size.width() > maxWidth:
                maxWidth = size.width()
        return maxWidth

    def onItemClicked(self, item):
        self.selectIndex = self.modifyListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["railEditor"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.tempList[self.selectIndex]
        editListElementWidget = EditListElementWidget(self, textSetting.textList["railEditor"]["modifySmfElementListLabel"], self.decryptFile, "modify", item)
        if editListElementWidget.exec() == QDialog.Accepted:
            self.dirtyFlag = True
            self.tempList[self.selectIndex] = editListElementWidget.resultValueList
            self.modifyListWidget.clear()
            displayModifyList = self.setListboxInfo(self.tempList)
            self.modifyListWidget.addItems(displayModifyList)
            self.modifyListWidget.setCurrentRow(self.selectIndex)

    def insertFunc(self):
        editListElementWidget = EditListElementWidget(self, textSetting.textList["railEditor"]["insertSmfElementListLabel"], self.decryptFile, "insert")
        if editListElementWidget.exec() == QDialog.Accepted:
            self.dirtyFlag = True
            self.tempList.insert(self.selectIndex + editListElementWidget.insertPos, editListElementWidget.resultValueList)
            self.modifyListWidget.clear()
            displayModifyList = self.setListboxInfo(self.tempList)
            self.modifyListWidget.addItems(displayModifyList)
            self.modifyListWidget.setCurrentRow(self.selectIndex + editListElementWidget.insertPos)
            self.selectIndex = self.selectIndex + editListElementWidget.insertPos

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.dirtyFlag = True
            self.tempList.pop(self.selectIndex)
            self.modifyListWidget.clear()
            displayModifyList = self.setListboxInfo(self.tempList)
            self.modifyListWidget.addItems(displayModifyList)
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I70"])
            if result == mb.OK:
                self.reloadFlag = True
                return True
        else:
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()


class EditListElementWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.insertPos = -1
        self.resultValueList = []

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.tempInfoGridLayout = QGridLayout()
        layout.addLayout(self.tempInfoGridLayout)
        self.lineEditList = []
        if self.decryptFile.game == "BS":
            tempInfoLabel = textSetting.textList["railEditor"]["smfElementListLabel1"]
        else:
            tempInfoLabel = textSetting.textList["railEditor"]["smfElementListLabel2"]
        for i, tempInfoValue in enumerate(tempInfoLabel):
            # layout - QGridLayout - label
            tempLabel = QLabel(tempInfoValue, font=self.font2)
            self.tempInfoGridLayout.addWidget(tempLabel, i, 0)
            # layout - QGridLayout - LineEdit
            tempLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(tempLineEdit)
            tempLineEdit.setValidator(integerValidator)
            self.tempInfoGridLayout.addWidget(tempLineEdit, i, 1)

            if self.mode == "modify":
                tempLineEdit.setText("{0}".format(item[i]))

        if self.mode == "insert":
            self.setInsertWidget(len(tempInfoLabel))
        
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
        self.tempInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.tempInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.tempInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            self.resultValueList.append(int(lineEdit.text()))
        return True

    def accept(self):
        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
