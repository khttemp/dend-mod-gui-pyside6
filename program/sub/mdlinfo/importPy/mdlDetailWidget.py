import copy
import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QDialog, QDialogButtonBox, QGridLayout, QSizePolicy, QListWidget,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()


class MdlDetailDialog(QDialog):
    def __init__(self, parent, title, num, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.selectId = None
        self.dirtyFlag = False
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.detailMdlList = decryptFile.allInfoList[self.num]["detailMdlList"]

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
        # headerLeft - smfName
        self.smfNameLabel = QLabel("{0}".format(self.smfName), font=font2)
        self.smfNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.smfNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.smfNameLabel.setFixedHeight(labelHeight)
        headerLeftLayout.addWidget(self.smfNameLabel)

        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["mdlinfo"]["selectNum"], font=font2)
        headerSelectLayout.addWidget(selectLabel)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedSize(labelWidth, labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel)

        # space
        headerLayout.addSpacing(15)
        # headerRight
        headerRightLayout = QVBoxLayout()
        headerLayout.addLayout(headerRightLayout)
        # headerRight - buttonLayout1
        headerRightButtonLayout1 = QHBoxLayout()
        headerRightButtonLayout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout1)
        # headerRight - buttonLayout1 - editColorButton
        self.editColorButton = QPushButton(textSetting.textList["mdlinfo"]["editColorLabel"])
        self.editColorButton.setFixedSize(buttonWidth, buttonHeight)
        self.editColorButton.setEnabled(False)
        self.editColorButton.clicked.connect(self.editColorFunc)
        headerRightButtonLayout1.addWidget(self.editColorButton)
        # stretch
        headerRightButtonLayout1.addStretch(1)
        # headerRight - buttonLayout1 - allEditElementButton
        self.allEditElementButton = QPushButton(textSetting.textList["mdlinfo"]["allElementModifyLabel"])
        self.allEditElementButton.setFixedSize(buttonWidth, buttonHeight)
        self.allEditElementButton.setEnabled(False)
        self.allEditElementButton.clicked.connect(self.allEditElementFunc)
        headerRightButtonLayout1.addWidget(self.allEditElementButton)

        # headerRight - buttonLayout2
        headerRightButtonLayout2 = QHBoxLayout()
        headerRightButtonLayout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout2)
        # headerRight - buttonLayout1 - modifyElementButton
        self.modifyElementButton = QPushButton(textSetting.textList["mdlinfo"]["elementModifyLabel"])
        self.modifyElementButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifyElementButton.setEnabled(False)
        self.modifyElementButton.clicked.connect(self.modifyElementFunc)
        headerRightButtonLayout2.addWidget(self.modifyElementButton)
        # space
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout2 - insertElementButton
        self.insertElementButton = QPushButton(textSetting.textList["mdlinfo"]["elementInsertLabel"])
        self.insertElementButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertElementButton.setEnabled(False)
        self.insertElementButton.clicked.connect(self.insertElementFunc)
        headerRightButtonLayout2.addWidget(self.insertElementButton)
        # space
        headerRightButtonLayout2.addStretch(1)
        # headerRight - buttonLayout2 - deleteElementButton
        self.deleteElementButton = QPushButton(textSetting.textList["mdlinfo"]["elementDeleteLabel"])
        self.deleteElementButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteElementButton.setEnabled(False)
        self.deleteElementButton.clicked.connect(self.deleteElementFunc)
        headerRightButtonLayout2.addWidget(self.deleteElementButton)
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

        self.createMdlDetailTable()

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def createMdlDetailTable(self):
        self.setMdlDetailTableHeader()
        self.setMdlDetailTableData()
        if len(self.detailMdlList) == 0:
            self.insertElementButton.setEnabled(True)

    def setMdlDetailTableHeader(self):
        headerLabelList = [
            textSetting.textList["mdlinfo"]["treeColorNum"],
            textSetting.textList["mdlinfo"]["treeMesh"],
            textSetting.textList["mdlinfo"]["treeConst"] + "1",
            textSetting.textList["mdlinfo"]["treeEle1-3"],
            textSetting.textList["mdlinfo"]["treeDiff"],
            textSetting.textList["mdlinfo"]["treeConst"] + "0",
            textSetting.textList["mdlinfo"]["treeEmis"],
            textSetting.textList["mdlinfo"]["treeNum2"] + "1",
            textSetting.textList["mdlinfo"]["treeNum2"] + "2",
        ]
        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)

    def setMdlDetailTableData(self):
        for detailMdlInfo in self.detailMdlList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            dataList = [
                detailMdlInfo["colorCnt"],
                ",".join(str(n) for n in detailMdlInfo["materialList"][0:2]),
                detailMdlInfo["materialList"][2],
                ",".join(str(n) for n in detailMdlInfo["materialList"][3:6]),
                ",".join(str(n) for n in detailMdlInfo["materialList"][6:10]),
                detailMdlInfo["materialList"][10],
                ",".join(str(n) for n in detailMdlInfo["materialList"][11:14]),
                detailMdlInfo["materialList"][14],
                detailMdlInfo["materialList"][15],
            ]
            for j, data in enumerate(dataList):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.detailMdlList):
                self.selectId = len(self.detailMdlList) - 1
            self.contentTable.selectRow(self.selectId)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.editColorButton.setEnabled(False)
            self.allEditElementButton.setEnabled(False)
            self.modifyElementButton.setEnabled(False)
            self.insertElementButton.setEnabled(False)
            self.deleteElementButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.editColorButton.setEnabled(True)
        self.allEditElementButton.setEnabled(True)
        self.modifyElementButton.setEnabled(True)
        self.insertElementButton.setEnabled(True)
        self.deleteElementButton.setEnabled(True)

    def reloadWidget(self):
        self.decryptFile = self.decryptFile.reload()
        self.detailMdlList = self.decryptFile.allInfoList[self.num]["detailMdlList"]
        self.clearTable()
        self.createMdlDetailTable()

        QTimer.singleShot(0, self.jumpToSelect)

    def editColorFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        texImageDialog = TexImageDialog(self, textSetting.textList["mdlinfo"]["texImageLabel"], self.num, detailNum, self.decryptFile, self.detailMdlList)
        if texImageDialog.exec() == QDialog.Accepted:
            if texImageDialog.dirtyFlag:
                if not self.decryptFile.updateTexImage(self.num, detailNum, texImageDialog.resultValueList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I29"])
                self.selectId = detailNum
                self.reloadWidget()

    def allEditElementFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        editDetailDialog = EditDetailDialog(self, textSetting.textList["mdlinfo"]["detailModelLabel"], "allEdit", self.num, detailNum, self.detailMdlList)
        if editDetailDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateTexList(self.num, editDetailDialog.firstDetailNum, editDetailDialog.newDetailMaterialList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()

    def modifyElementFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return
        
        detailNum = selectedItems[0].row()
        editDetailDialog = EditDetailDialog(self, textSetting.textList["mdlinfo"]["detailModelLabel"], "modify", self.num, detailNum, self.detailMdlList)
        if editDetailDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateTex(self.num, detailNum, editDetailDialog.resultValueList, "modify"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()

    def insertElementFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return
        
        detailNum = selectedItems[0].row()
        editDetailDialog = EditDetailDialog(self, textSetting.textList["mdlinfo"]["detailModelLabel"], "insert", self.num, detailNum, self.detailMdlList)
        if editDetailDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateTex(self.num, detailNum + editDetailDialog.insertPos, editDetailDialog.resultValueList, "insert"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum + editDetailDialog.insertPos
            self.reloadWidget()

    def deleteElementFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        warnMsg = textSetting.textList["infoList"]["I25"].format(detailNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.updateTex(self.num, detailNum, [], "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I26"])
            self.selectId = detailNum
            self.reloadWidget()


class TexImageDialog(QDialog):
    def __init__(self, parent, title, num, detailNum, decryptFile, detailMdlList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.detailMdlList = detailMdlList
        self.txtImgList = copy.deepcopy(detailMdlList[detailNum]["textureImgList"])
        self.resultValueList = []
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        # mainLayout - buttonLayout - modifyButton
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

        # mainLayout - QListWidget
        self.texImageListWidget = QListWidget(font=font2)
        displayTexImageList = self.setListboxInfo(self.txtImgList)
        self.texImageListWidget.addItems(displayTexImageList)
        self.texImageListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        mainLayout.addWidget(self.texImageListWidget, stretch=1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox)

    def setListboxInfo(self, txtImgList):
        displayTexImageList = []
        if len(txtImgList) > 0:
            for i in range(len(txtImgList)):
                displayTexImageList.append(txtImgList[i])
        else:
            displayTexImageList = [textSetting.textList["mdlinfo"]["noList"]]
        return displayTexImageList

    def onItemClicked(self, item):
        self.selectIndex = self.texImageListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlinfo"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.txtImgList[self.selectIndex]
        editTexImageDialog = EditTexImageDialog(self, textSetting.textList["modify"], "modify", item)
        if editTexImageDialog.exec() == QDialog.Accepted:
            self.txtImgList[self.selectIndex] = editTexImageDialog.texImageLineEdit.text()
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.texImageListWidget.clear()
            self.texImageListWidget.addItems(displayTexImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editTexImageDialog = EditTexImageDialog(self, textSetting.textList["insert"], "insert")
        if editTexImageDialog.exec() == QDialog.Accepted:
            self.txtImgList.insert(self.selectIndex + editTexImageDialog.insertPos, editTexImageDialog.texImageLineEdit.text())
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.texImageListWidget.clear()
            self.texImageListWidget.addItems(displayTexImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.txtImgList.pop(self.selectIndex)
            displayTexImageList = self.setListboxInfo(self.txtImgList)
            self.texImageListWidget.clear()
            self.texImageListWidget.addItems(displayTexImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def validate(self):
        self.resultValueList = []
        for i in range(self.texImageListWidget.count()):
            item = self.texImageListWidget.item(i)
            if item.text() == textSetting.textList["mdlinfo"]["noList"]:
                continue
            self.resultValueList.append(item.text())
        return True

    def accept(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I28"], icon="warning")
            if result != mb.OK:
                return

            if not self.validate():
                return
            super().accept()
        else:
            super().accept()


class EditTexImageDialog(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.texImageGridLayout = QGridLayout()
        layout.addLayout(self.texImageGridLayout)
        # layout - QGridLayout - LineEdit
        self.texImageLineEdit = QLineEdit(font=self.font2)
        self.texImageGridLayout.addWidget(self.texImageLineEdit, 0, 0, 1, 2)

        if self.mode == "modify":
            self.texImageLineEdit.setText("{0}".format(item))

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
        self.texImageGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlinfo"]["posLabel"], font=self.font2)
        self.texImageGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlinfo"]["posValue"])
        self.texImageGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        if not self.texImageLineEdit.text():
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


class EditDetailDialog(QDialog):
    def __init__(self, parent, title, mode, num, detailNum, detailMdlList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.num = num
        self.detailMdlList = detailMdlList
        self.materialList = detailMdlList[detailNum]["materialList"]

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.detailGridLayout = QGridLayout()
        layout.addLayout(self.detailGridLayout)

        self.lineEditList = []
        if self.mode == "allEdit":
            self.setAllEditDetailDialog()
        else:
            self.setEditDetailDialog()

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setEditDetailDialog(self):
        # layout - QGridLayout - meshNoNameLabel
        meshNoNameLabel = QLabel(textSetting.textList["mdlinfo"]["detailModelMeshLabel"], font=self.font2)
        self.detailGridLayout.addWidget(meshNoNameLabel, 0, 0)
        # layout - QGridLayout - meshNoLineEdit
        meshNoLineEdit = QLineEdit(font=self.font2)
        meshNoLineEdit.setText("{0}".format(self.materialList[0]))
        meshNoLineEdit.setValidator(self.integerValidator)
        self.lineEditList.append(meshNoLineEdit)
        self.detailGridLayout.addWidget(meshNoLineEdit, 0, 1)

        # layout - QGridLayout - mtrlNoNameLabel
        mtrlNoNameLabel = QLabel(textSetting.textList["mdlinfo"]["detailModelMtrlLabel"], font=self.font2)
        self.detailGridLayout.addWidget(mtrlNoNameLabel, 0, 2)
        # layout - QGridLayout - mtrlNoLineEdit
        mtrlNoLineEdit = QLineEdit(font=self.font2)
        mtrlNoLineEdit.setText("{0}".format(self.materialList[1]))
        mtrlNoLineEdit.setValidator(self.integerValidator)
        self.lineEditList.append(mtrlNoLineEdit)
        self.detailGridLayout.addWidget(mtrlNoLineEdit, 0, 3)

        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.detailGridLayout.addWidget(horizentalLine, 1, 0, 1, 4)

        headerLabelList = [
            textSetting.textList["mdlinfo"]["treeConst"] + "1",
            "DRAW",
            "TRAN",
            "SPEC",
            "DIFF_R",
            "DIFF_G",
            "DIFF_B",
            "DIFF_A",
            textSetting.textList["mdlinfo"]["treeConst"] + "0",
            "EMIS_R",
            "EMIS_G",
            "EMIS_B",
            textSetting.textList["mdlinfo"]["treeNum2"] + "1",
            textSetting.textList["mdlinfo"]["treeNum2"] + "2",
        ]

        for i, headerLabel in enumerate(headerLabelList):
            if i >= 8:
                # layout - QGridLayout - detailNameLabel
                detailNameLabel = QLabel(headerLabel, font=self.font2)
                self.detailGridLayout.addWidget(detailNameLabel, i - 6, 2)
                # layout - QGridLayout - detailLineEdit
                detailLineEdit = QLineEdit(font=self.font2)
                self.lineEditList.append(detailLineEdit)
                self.detailGridLayout.addWidget(detailLineEdit, i - 6, 3)
            else:
                # layout - QGridLayout - detailNameLabel
                detailNameLabel = QLabel(headerLabel, font=self.font2)
                self.detailGridLayout.addWidget(detailNameLabel, i + 2, 0)
                # layout - QGridLayout - detailLineEdit
                detailLineEdit = QLineEdit(font=self.font2)
                self.lineEditList.append(detailLineEdit)
                self.detailGridLayout.addWidget(detailLineEdit, i + 2, 1)
            detailLineEdit.setText("{0}".format(self.materialList[i + 2]))
            if i in [4, 5, 6, 7, 9, 10, 11]:
                detailLineEdit.setValidator(self.numberValidator)
            else:
                detailLineEdit.setValidator(self.integerValidator)
        
        if self.mode == "insert":
            self.setInsertWidget(10)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.detailGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlinfo"]["posLabel"], font=self.font2)
        self.detailGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlinfo"]["posValue"])
        self.detailGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def setAllEditDetailDialog(self):
        self.checkboxList = []
        # layout - QGridLayout - meshNoNameLabel
        meshNoNameLabel = QLabel(textSetting.textList["mdlinfo"]["detailModelMeshLabel"], font=self.font2)
        self.detailGridLayout.addWidget(meshNoNameLabel, 0, 0)
        # layout - QGridLayout - meshNoLabel
        meshNoLabel = QLabel("{0}".format(self.materialList[0]), font=self.font2)
        self.detailGridLayout.addWidget(meshNoLabel, 0, 1)

        headerLabelList = [
            "DRAW",
            "TRAN",
            "SPEC",
            "DIFF_R",
            "DIFF_G",
            "DIFF_B",
            "DIFF_A",
            "EMIS_R",
            "EMIS_G",
            "EMIS_B",
        ]
        valueList = [
            self.materialList[3],
            self.materialList[4],
            self.materialList[5],
            self.materialList[6],
            self.materialList[7],
            self.materialList[8],
            self.materialList[9],
            self.materialList[11],
            self.materialList[12],
            self.materialList[13],
        ]

        for i, headerLabel in enumerate(headerLabelList):
            detailCheckbox = QCheckBox(headerLabel, font=self.font2)
            self.checkboxList.append(detailCheckbox)
            self.detailGridLayout.addWidget(detailCheckbox, i + 1, 0)

            # layout - QGridLayout - detailLineEdit
            detailLineEdit = QLineEdit(font=self.font2)
            detailLineEdit.setText("{0}".format(valueList[i]))
            self.lineEditList.append(detailLineEdit)
            if i in [0, 1, 2]:
                detailLineEdit.setValidator(self.integerValidator)
            else:
                detailLineEdit.setValidator(self.numberValidator)
            self.detailGridLayout.addWidget(detailLineEdit, i + 1, 1)

    def validate(self):
        self.resultValueList = []
        if self.mode == "allEdit":
            return self.allEditValidate()
        else:
            return self.commonValidate()

    def commonValidate(self):
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            if i in [6, 7, 8, 9, 11, 12, 13]:
                self.resultValueList.append(float(lineEdit.text()))
            else:
                self.resultValueList.append(int(lineEdit.text()))

        newMeshList = [int(self.lineEditList[0].text()), int(self.lineEditList[1].text())]
        oldMeshList = [self.materialList[0], self.materialList[1]]
        materialList = [x["materialList"][0:2] for x in self.detailMdlList]
        if self.mode == "modify":
            warnMsg = ""
            if newMeshList != oldMeshList and newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
                warnMsg += textSetting.textList["infoList"]["I31"]
        elif self.mode == "insert":
            warnMsg = ""
            if newMeshList in materialList:
                warnMsg = textSetting.textList["infoList"]["I30"].format(newMeshList[0], newMeshList[1])
                warnMsg += textSetting.textList["infoList"]["I32"]
        if warnMsg:
            result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
            if result != mb.OK:
                return

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def allEditValidate(self):
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            if i in [0, 1, 2]:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                self.resultValueList.append(float(lineEdit.text()))
        
        selectMeshNo = self.materialList[0]
        self.firstDetailNum = -1
        findFlag = False
        editLabelList = []
        self.newDetailMaterialList = []
        for detailIdx, detailMdlInfo in enumerate(self.detailMdlList):
            meshNo = detailMdlInfo["materialList"][0]
            varCnt = 0
            checkVarCnt = 0
            if selectMeshNo == meshNo:
                if not findFlag:
                    findFlag = True
                    self.firstDetailNum = detailIdx
                newDetailMdlInfo = copy.deepcopy(detailMdlInfo)
                # "DRAW", "TRAN", "SPEC"
                eleLabelList = ["DRAW", "TRAN", "SPEC"]
                for i in range(3):
                    if self.checkboxList[checkVarCnt].isChecked():
                        if eleLabelList[i] not in editLabelList:
                            editLabelList.append(eleLabelList[i])
                        newDetailMdlInfo["materialList"][3 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                # DIFF
                colorLabelList = ["DIFF_R", "DIFF_G", "DIFF_B", "DIFF_A"]
                for i in range(4):
                    if self.checkboxList[checkVarCnt].isChecked():
                        if colorLabelList[i] not in editLabelList:
                            editLabelList.append(colorLabelList[i])
                        newDetailMdlInfo["materialList"][6 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                # EMIS
                colorLabelList = ["EMIS_R", "EMIS_G", "EMIS_B"]
                for i in range(3):
                    if self.checkboxList[checkVarCnt].isChecked():
                        if colorLabelList[i] not in editLabelList:
                            editLabelList.append(colorLabelList[i])
                        newDetailMdlInfo["materialList"][11 + i] = self.resultValueList[varCnt]
                    varCnt += 1
                    checkVarCnt += 1
                self.newDetailMaterialList.append(newDetailMdlInfo["materialList"])
        warnMsg = textSetting.textList["infoList"]["I129"].format(selectMeshNo, "\n".join(editLabelList))
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result == mb.OK:
            return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
