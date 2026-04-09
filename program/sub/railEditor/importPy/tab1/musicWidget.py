import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QComboBox,
    QDialog, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class MusicWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        fixedWidth = 86
        fixedHeight = 40

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # mainLayout - musicNameLabel
        musicNameLabel = QLabel(textSetting.textList["railEditor"]["bgmNum"], font=font6)
        musicNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        musicNameLabel.setFixedSize(fixedWidth, fixedHeight)
        musicNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(musicNameLabel, 0, 0)
        # mainLayout - musicCountLabel
        musicCountLabel = QLabel("{0}".format(self.decryptFile.musicCnt), font=font6)
        musicCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        musicCountLabel.setFixedSize(fixedWidth, fixedHeight)
        musicCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(musicCountLabel, 0, 1)
        # mainLayout - musicButton
        musicButton = QPushButton(textSetting.textList["railEditor"]["modifyBtnLabel"], font=font6)
        musicButton.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(musicButton, 0, 2)
        if self.decryptFile.game in ["CS", "RS"]:
            musicButton.clicked.connect(self.editVar)
        else:
            musicButton.clicked.connect(self.editMusicList)

    def editVar(self):
        editMusicCountDialog = EditMusicCountDialog(self, textSetting.textList["railEditor"]["editBgmNumLabel"], self.decryptFile)
        if editMusicCountDialog.exec() == QDialog.Accepted:
            resultValue = int(editMusicCountDialog.lineEdit.text())
            if not self.decryptFile.saveMusic(resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])
            self.reloadFunc()

    def editMusicList(self):
        editMusicListDialog = EditMusicListDialog(self, textSetting.textList["railEditor"]["editBgmListLabel"], self.decryptFile)
        if editMusicListDialog.exec() == QDialog.Accepted:
            if editMusicListDialog.reloadFlag:
                if not self.decryptFile.saveMusicList(editMusicListDialog.musicList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I69"])
                self.reloadFunc()


class EditMusicCountDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - LineEdit
        self.lineEdit = QLineEdit(font=font2)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.lineEdit.setValidator(integerValidator)
        self.lineEdit.setText("{0}".format(self.decryptFile.musicCnt))
        layout.addWidget(self.lineEdit)
        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if not self.lineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E60"])
            return
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditMusicListDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.musicList = copy.deepcopy(self.decryptFile.musicList)
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
        if self.decryptFile.game != "LS":
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
        self.musicListListWidget = QListWidget(font=font2)
        displayMusicList = self.setListboxInfo(self.musicList)
        self.musicListListWidget.addItems(displayMusicList)
        self.musicListListWidget.setMinimumWidth(self.getMaxWidth() + 20)
        self.musicListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        layout.addWidget(self.musicListListWidget, stretch=1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setListboxInfo(self, musicList):
        displayMusicList = []
        if len(musicList) > 0:
            for i in range(len(musicList)):
                musicInfo = musicList[i]
                displayMusicList.append("{0:02d}→{1}".format(i, musicInfo))
        else:
            displayMusicList = [textSetting.textList["railEditor"]["noList"]]
        return displayMusicList

    def getMaxWidth(self):
        maxWidth = 0
        for i in range(self.musicListListWidget.count()):
            size = self.musicListListWidget.sizeHintForIndex(self.musicListListWidget.model().index(i, 0))
            if size.width() > maxWidth:
                maxWidth = size.width()
        return maxWidth

    def onItemClicked(self, item):
        self.selectIndex = self.musicListListWidget.row(item)
        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.insertButton.setEnabled(True)
            if item.text() == textSetting.textList["railEditor"]["noList"]:
                self.modifyButton.setEnabled(False)
                self.deleteButton.setEnabled(False)
            else:
                self.modifyButton.setEnabled(True)
                self.deleteButton.setEnabled(True)
        else:
            self.modifyButton.setEnabled(True)

    def modifyFunc(self):
        item = self.musicList[self.selectIndex]
        editMusicElementWidget = EditMusicElementWidget(self, textSetting.textList["railEditor"]["modifyBgmLabel"], self.decryptFile, "modify", item)
        if editMusicElementWidget.exec() == QDialog.Accepted:
            self.dirtyFlag = True
            self.musicList[self.selectIndex] = editMusicElementWidget.resultValueList
            self.musicListListWidget.clear()
            displayMusicList = self.setListboxInfo(self.musicList)
            self.musicListListWidget.addItems(displayMusicList)
            self.musicListListWidget.setCurrentRow(self.selectIndex)

    def insertFunc(self):
        editMusicElementWidget = EditMusicElementWidget(self, textSetting.textList["railEditor"]["insertBgmLabel"], self.decryptFile, "insert")
        if editMusicElementWidget.exec() == QDialog.Accepted:
            self.dirtyFlag = True
            self.musicList.insert(self.selectIndex + editMusicElementWidget.insertPos, editMusicElementWidget.resultValueList)
            self.musicListListWidget.clear()
            displayMusicList = self.setListboxInfo(self.musicList)
            self.musicListListWidget.addItems(displayMusicList)
            self.musicListListWidget.setCurrentRow(self.selectIndex + editMusicElementWidget.insertPos)
            self.selectIndex = self.selectIndex + editMusicElementWidget.insertPos

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.dirtyFlag = True
            self.musicList.pop(self.selectIndex)
            self.musicListListWidget.clear()
            displayMusicList = self.setListboxInfo(self.musicList)
            self.musicListListWidget.addItems(displayMusicList)
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


class EditMusicElementWidget(QDialog):
    def __init__(self, parent, title, decryptFile, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?"), self)
        self.insertPos = -1
        self.resultValueList = []

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.musicGridLayout = QGridLayout()
        layout.addLayout(self.musicGridLayout)
        self.lineEditList = []
        musicElementInfoLabelList = textSetting.textList["railEditor"]["editBgmInfoLabelList"]
        for i, musicElementInfoLabel in enumerate(musicElementInfoLabelList):
            # layout - QGridLayout - musicLabel
            musicLabel = QLabel(musicElementInfoLabel, font=self.font2)
            self.musicGridLayout.addWidget(musicLabel, i, 0)
            # layout - QGridLayout - musicLineEdit
            musicLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(musicLineEdit)
            self.musicGridLayout.addWidget(musicLineEdit, i, 1)
            if i in [2, 3]:
                musicLineEdit.setValidator(numberValidator)

            if self.mode == "modify":
                musicLineEdit.setText("{0}".format(item[i]))

        if self.mode == "insert":
            self.setInsertWidget(len(musicElementInfoLabelList))

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
        self.musicGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["railEditor"]["posLabel"], font=self.font2)
        self.musicGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["railEditor"]["posValue"])
        self.musicGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        for i, lineEdit in enumerate(self.lineEditList):
            if i in [2, 3]:
                if not lineEdit.hasAcceptableInput():
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return
                self.resultValueList.append(float(lineEdit.text()))
            else:
                self.resultValueList.append(lineEdit.text())
        return True

    def accept(self):
        infoMsg = textSetting.textList["infoList"]["I21"]
        if self.mode == "insert":
            infoMsg = textSetting.textList["infoList"]["I71"]
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=infoMsg)
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
