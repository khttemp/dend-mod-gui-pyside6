import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QComboBox,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QDialog, QDialogButtonBox, QGridLayout,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()


class SmfDetailDialog(QDialog):
    def __init__(self, parent, title, num, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.selectId = None
        self.dirtyFlag = False
        self.smfName = decryptFile.allInfoList[self.num]["smfName"]
        self.smfDetailList = decryptFile.allInfoList[self.num]["smfDetailList"]

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

        # headerRight - buttonLayout
        headerRightButtonLayout = QHBoxLayout()
        headerRightButtonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        headerRightLayout.addLayout(headerRightButtonLayout)
        # headerRight - buttonLayout1 - modifySmfDetailButton
        self.modifySmfDetailButton = QPushButton(textSetting.textList["mdlinfo"]["smfInfoModify"])
        self.modifySmfDetailButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifySmfDetailButton.setEnabled(False)
        self.modifySmfDetailButton.clicked.connect(self.modifySmfDetailFunc)
        headerRightButtonLayout.addWidget(self.modifySmfDetailButton)
        # space
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout2 - insertSmfDetailButton
        self.insertSmfDetailButton = QPushButton(textSetting.textList["mdlinfo"]["smfInfoInsert"])
        self.insertSmfDetailButton.setFixedSize(buttonWidth, buttonHeight)
        self.insertSmfDetailButton.setEnabled(False)
        self.insertSmfDetailButton.clicked.connect(self.insertSmfDetailFunc)
        headerRightButtonLayout.addWidget(self.insertSmfDetailButton)
        # space
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout2 - deleteSmfDetailButton
        self.deleteSmfDetailButton = QPushButton(textSetting.textList["mdlinfo"]["smfInfoDelete"])
        self.deleteSmfDetailButton.setFixedSize(buttonWidth, buttonHeight)
        self.deleteSmfDetailButton.setEnabled(False)
        self.deleteSmfDetailButton.clicked.connect(self.deleteSmfDetailFunc)
        headerRightButtonLayout.addWidget(self.deleteSmfDetailButton)
        # stretch
        headerRightLayout.addSpacing(40)

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

        self.createSmfDetailTable()

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def createSmfDetailTable(self):
        self.setSmfDetailTableHeader()
        self.setSmfDetailTableData()
        if len(self.smfDetailList) == 0:
            self.insertSmfDetailButton.setEnabled(True)

    def setSmfDetailTableHeader(self):
        self.headerLabelList = [
            textSetting.textList["mdlinfo"]["smfName"],
            textSetting.textList["mdlinfo"]["smfParam"] + "1",
            textSetting.textList["mdlinfo"]["smfParam"] + "2",
            textSetting.textList["mdlinfo"]["smfParam"] + "3",
            textSetting.textList["mdlinfo"]["smfParam"] + "4",
            textSetting.textList["mdlinfo"]["smfParam"] + "5",
            textSetting.textList["mdlinfo"]["smfParam"] + "6",
        ]
        self.contentTable.setColumnCount(len(self.headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contentTable.setHorizontalHeaderLabels(self.headerLabelList)

    def setSmfDetailTableData(self):
        for smfDetailInfo in self.smfDetailList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for j, smfDetail in enumerate(smfDetailInfo["smfDetail"]):
                item = QTableWidgetItem(str(smfDetail))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, j, item)

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.smfDetailList):
                self.selectId = len(self.smfDetailList) - 1
            self.contentTable.selectRow(self.selectId)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.selectLineLabel.setText("")
            self.modifySmfDetailButton.setEnabled(False)
            self.insertSmfDetailButton.setEnabled(False)
            self.deleteSmfDetailButton.setEnabled(False)
            return

        row = selectedItems[0].row()
        self.selectLineLabel.setText(str(row + 1))
        self.modifySmfDetailButton.setEnabled(True)
        self.insertSmfDetailButton.setEnabled(True)
        self.deleteSmfDetailButton.setEnabled(True)

    def reloadWidget(self):
        self.decryptFile = self.decryptFile.reload()
        self.smfDetailList = self.decryptFile.allInfoList[self.num]["smfDetailList"]
        self.clearTable()
        self.createSmfDetailTable()

        QTimer.singleShot(0, self.jumpToSelect)

    def modifySmfDetailFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        editSmfDetailDialog = EditSmfDetailDialog(self, textSetting.textList["mdlinfo"]["smfElementModify"], "modify", detailNum, self.smfDetailList[detailNum], self.headerLabelList)
        if editSmfDetailDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum, editSmfDetailDialog.resultValueList, "modify"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum
            self.dirtyFlag = True
            self.reloadWidget()

    def insertSmfDetailFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        editSmfDetailDialog = EditSmfDetailDialog(self, textSetting.textList["mdlinfo"]["smfElementInsert"], "insert", detailNum, self.smfDetailList[detailNum], self.headerLabelList)
        if editSmfDetailDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum + editSmfDetailDialog.insertPos, editSmfDetailDialog.resultValueList, "insert"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum + editSmfDetailDialog.insertPos
            self.dirtyFlag = True
            self.reloadWidget()

    def deleteSmfDetailFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return

        detailNum = selectedItems[0].row()
        warnMsg = textSetting.textList["infoList"]["I25"].format(detailNum + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")
        if result == mb.OK:
            if not self.decryptFile.updateSmfDetail(self.num, detailNum, None, "delete"):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I33"])
            self.selectId = detailNum
            self.dirtyFlag = True
            self.reloadWidget()


class EditSmfDetailDialog(QDialog):
    def __init__(self, parent, title, mode, detailNum, smfDetailInfo, headerLabelList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.detailNum = detailNum
        self.smfDetailInfo = smfDetailInfo["smfDetail"]
        self.insertPos = None

        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.detailGridLayout = QGridLayout()
        layout.addLayout(self.detailGridLayout)

        self.lineEditList = []
        for i, headerLabel in enumerate(headerLabelList):
            # layout - QGridLayout - detailNameLabel
            detailNameLabel = QLabel(headerLabel, font=self.font2)
            self.detailGridLayout.addWidget(detailNameLabel, i, 0)
            # layout - QGridLayout - detailLineEdit
            detailLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(detailLineEdit)
            self.detailGridLayout.addWidget(detailLineEdit, i, 1)
            if mode == "modify":
                detailLineEdit.setText("{0}".format(self.smfDetailInfo[i]))

            if i > 0:
                detailLineEdit.setValidator(numberValidator)
                if mode == "insert":
                    detailLineEdit.setText("{0}".format(float(0)))

        if self.mode == "insert":
            self.setInsertWidget(7)

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
        self.detailGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlinfo"]["posLabel"], font=self.font2)
        self.detailGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlinfo"]["posValue"])
        self.detailGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            if i > 0:
                self.resultValueList.append(float(lineEdit.text()))
            else:
                if not lineEdit.text():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E138"])
                    return False
                self.resultValueList.append(lineEdit.text())

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I34"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
