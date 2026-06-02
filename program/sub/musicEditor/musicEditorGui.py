
import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

import program.sub.musicEditor.dendDecrypt.BSMusicDecrypt as dendBs
import program.sub.musicEditor.dendDecrypt.CSMusicDecrypt as dendCs
import program.sub.musicEditor.dendDecrypt.RSMusicDecrypt as dendRs

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QGroupBox, QComboBox,
    QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox,
    QRadioButton, QPushButton, QButtonGroup, QGridLayout,
    QFileDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QTimer, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class MusicEditorWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        self.selectId = None
        self.BS = 1
        self.CS = 2
        self.RS = 3

        buttonWidth = 200
        buttonHeight = 28

        mainLayout = QVBoxLayout(self)
        mainLayout.addSpacing(10)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 1)

        # headerRight - radioLayout
        headerRadioLayout = QHBoxLayout()
        headerRadioLayout.setContentsMargins(20, 0, 30, 0)
        headerRadioLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerLayout.addLayout(headerRadioLayout, 1)
        # headerRight - radioLayout - bsRadio
        bsRadioButton = QRadioButton("Burning Stage")
        bsRadioButton.toggled.connect(self.radioButtonTrigger)
        headerRadioLayout.addWidget(bsRadioButton)
        # space
        headerRadioLayout.addSpacing(30)
        # headerRight - radioLayout - csRadio
        csRadioButton = QRadioButton("Climax Stage")
        csRadioButton.toggled.connect(self.radioButtonTrigger)
        headerRadioLayout.addWidget(csRadioButton)
        # space
        headerRadioLayout.addSpacing(30)
        # headerRight - radioLayout - rsRadio
        rsRadioButton = QRadioButton("Rising Stage")
        rsRadioButton.setChecked(True)
        rsRadioButton.toggled.connect(self.radioButtonTrigger)
        headerRadioLayout.addWidget(rsRadioButton)
        # stretch
        headerRadioLayout.addStretch()

        # RadioGroup
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(bsRadioButton, self.BS)
        self.radioGroup.addButton(csRadioButton, self.CS)
        self.radioGroup.addButton(rsRadioButton, self.RS)

        # headerRight - buttonLayout
        headerButtonLayout = QHBoxLayout()
        headerButtonLayout.setContentsMargins(30, 0, 10, 0)
        headerButtonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerLayout.addLayout(headerButtonLayout, 1)
        # headerRight - buttonLayout - button1
        self.modifyMusicButton = QPushButton(textSetting.textList["musicEditor"]["bgmModifyLabel"])
        self.modifyMusicButton.setFixedSize(buttonWidth, buttonHeight)
        self.modifyMusicButton.setEnabled(False)
        self.modifyMusicButton.clicked.connect(self.modifyMusicFunc)
        headerButtonLayout.addWidget(self.modifyMusicButton)
        # space
        headerButtonLayout.addSpacing(30)
        # headerRight - buttonLayout - button2
        self.swapMusicButton = QPushButton(textSetting.textList["musicEditor"]["bgmSwapLabel"])
        self.swapMusicButton.setFixedSize(buttonWidth, buttonHeight)
        self.swapMusicButton.setEnabled(False)
        self.swapMusicButton.clicked.connect(self.swapMusicFunc)
        headerButtonLayout.addWidget(self.swapMusicButton)

        # content
        contentFrame = QGroupBox(textSetting.textList["musicEditor"]["scriptLabel"])
        mainLayout.addWidget(contentFrame, 20)
        contentLayout = QVBoxLayout()
        contentFrame.setLayout(contentLayout)
        self.contentTable = QTableWidget()
        self.contentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contentTable.setCornerButtonEnabled(False)
        self.contentTable.itemSelectionChanged.connect(self.onSelectionChanged)
        contentLayout.addWidget(self.contentTable)

    def radioButtonTrigger(self, isChecked):
        if not isChecked:
            return

        self.deleteWidget()

    def deleteWidget(self):
        self.clearTable()
        self.modifyMusicButton.setEnabled(False)
        self.swapMusicButton.setEnabled(False)

    def clearTable(self):
        self.contentTable.clearSelection()
        self.contentTable.clear()
        self.contentTable.setRowCount(0)
        self.contentTable.setColumnCount(0)

    def createMusicTable(self):
        headerLabelList = []
        for idx, headerInfo in enumerate(self.decryptFile.headerList):
            if idx == 0:
                continue
            headerLabelList.append(headerInfo[0])

        self.contentTable.setColumnCount(len(headerLabelList))
        self.contentTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.contentTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.contentTable.setHorizontalHeaderLabels(headerLabelList)
        for musicInfo in self.decryptFile.musicList:
            rowCount = self.contentTable.rowCount()
            self.contentTable.insertRow(rowCount)
            for colIdx, data in enumerate(musicInfo):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contentTable.setItem(rowCount, colIdx, item)

    def onSelectionChanged(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            self.modifyMusicButton.setEnabled(False)
            self.swapMusicButton.setEnabled(False)
            return

        self.modifyMusicButton.setEnabled(True)
        self.swapMusicButton.setEnabled(True)

    def openFile(self):
        selectedRadioId = self.radioGroup.checkedId()
        if selectedRadioId == self.BS:
            fileType = "{0} ({1})".format(textSetting.textList["musicEditor"]["fileType"], "LS_INFO.BIN")
        elif selectedRadioId == self.CS:
            fileType = "{0} ({1})".format(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO.BIN")
        else:
            fileType = "{0} ({1})".format(textSetting.textList["musicEditor"]["fileType"], "SOUNDTRACK_INFO_4TH.BIN")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return
        del self.decryptFile
        if selectedRadioId == self.BS:
            self.decryptFile = dendBs.BSMusicDecrypt(file_path)
        elif selectedRadioId == self.CS:
            self.decryptFile = dendCs.CSMusicDecrypt(file_path)
        else:
            self.decryptFile = dendRs.RSMusicDecrypt(file_path)

        if not self.decryptFile.open():
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E21"])
            return

        self.deleteWidget()
        self.createMusicTable()

    def jumpToSelect(self):
        if self.selectId is not None:
            if self.selectId >= len(self.decryptFile.musicList):
                self.selectId = len(self.decryptFile.musicList) - 1
            self.contentTable.selectRow(self.selectId)
    
    def reloadFile(self):
        self.decryptFile = self.decryptFile.reload()
        self.deleteWidget()
        self.createMusicTable()

        QTimer.singleShot(0, self.jumpToSelect)

    def modifyMusicFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return
        
        num = selectedItems[0].row()
        bgmItem = self.decryptFile.musicList[num][1:]
        headerList = [x[0] for x in self.decryptFile.headerList[2:]]
        editMusicInfoDialog = EditMusicInfoDialog(self, textSetting.textList["musicEditor"]["bgmModify"], bgmItem, headerList)
        if editMusicInfoDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.saveMusic(num, editMusicInfoDialog.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I41"])
            self.selectId = num
            self.reloadFile()

    def swapMusicFunc(self):
        selectedItems = self.contentTable.selectedItems()
        if not selectedItems:
            return
        
        num = selectedItems[0].row()
        swapMusicDialog = SwapMusicDialog(self, textSetting.textList["musicEditor"]["bgmSwap"], num, self.decryptFile)
        if swapMusicDialog.exec() == QDialog.Accepted:
            if not self.decryptFile.swapMusic(num, swapMusicDialog.swapMusicNo):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I41"])
            self.selectId = num
            self.reloadFile()


class EditMusicInfoDialog(QDialog):
    def __init__(self, parent, title, bgmItem, headerList):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.bgmItem = bgmItem
        self.headerList = headerList
        self.resultValueList = []

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        musicInfoGridLayout = QGridLayout()
        layout.addLayout(musicInfoGridLayout)
        self.lineEditList = []

        for i, header in enumerate(headerList):
            # layout - QGridLayout - label
            nameLabel = QLabel(header, font=font2)
            musicInfoGridLayout.addWidget(nameLabel, i, 0)
            # layout - QGridLayout - lineEdit
            musicLineEdit = QLineEdit(font=font2)
            musicLineEdit.setText("{0}".format(bgmItem[i]))
            self.lineEditList.append(musicLineEdit)
            if i > 1:
                musicLineEdit.setValidator(numberValidator)
            musicInfoGridLayout.addWidget(musicLineEdit, i, 1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if i > 1:
                if not lineEdit.hasAcceptableInput():
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return
                self.resultValueList.append(float(lineEdit.text()))
            else:
                if not lineEdit.text():
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E139"].format(self.headerList[i]))
                    return False
                self.resultValueList.append(lineEdit.text())
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class SwapMusicDialog(QDialog):
    def __init__(self, parent, title, num, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.num = num
        self.decryptFile = decryptFile
        self.swapMusicNoList = []
        swapMusicComboList = []
        self.swapMusicNo = -1

        for index, musicInfo in enumerate(self.decryptFile.musicList):
            if index == num:
                continue
            self.swapMusicNoList.append(index)
            swapMusicComboList.append("%02d(%s)" % (index + 1, musicInfo[2]))

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        swapLabel = QLabel(textSetting.textList["musicEditor"]["changeBgmNum"], font=font2)
        layout.addWidget(swapLabel)
        # layout - Combobox
        self.combobox = QComboBox(font=font2)
        self.combobox.addItems(swapMusicComboList)
        layout.addWidget(self.combobox)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        swapCbIdx = self.combobox.currentIndex()
        self.swapMusicNo = self.swapMusicNoList[swapCbIdx]
        warnMsg = textSetting.textList["infoList"]["I40"].format(self.num + 1, self.swapMusicNo + 1) + textSetting.textList["infoList"]["I39"]

        result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning")
        if result == mb.OK:
            return True

    def accept(self):
        if not self.validate():
            return
        super().accept()
