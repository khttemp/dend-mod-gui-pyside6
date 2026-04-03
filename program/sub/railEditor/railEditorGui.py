import os
import traceback

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
import program.sub.railEditor.railEditorProcess as railEditorProcess

import program.sub.railEditor.dendDecrypt.RSdecrypt as dendRs
import program.sub.railEditor.dendDecrypt.CSdecrypt as dendCs
import program.sub.railEditor.dendDecrypt.BSdecrypt as dendBs
import program.sub.railEditor.dendDecrypt.LSdecrypt as dendLs
import program.sub.railEditor.dendDecrypt.LSTrialDecrypt as dendLsTrial

from PySide6.QtWidgets import (
    QWidget, QFrame, QScrollArea, QLabel, QComboBox,
    QRadioButton, QPushButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout,
    QFileDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()

class RailEditorWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.decryptFile = None
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        labelHeight = 28
        buttonWidth = 200
        buttonHeight = 28
        self.LSTrial = -1
        self.LS = 0
        self.BS = 1
        self.CS = 2
        self.RS = 3

        mainLayout = QVBoxLayout(self)
        mainLayout.addSpacing(10)
        # header
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout, 2)

        # headerLeft
        headerLeftLayout = QVBoxLayout()
        headerLeftLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(10)
        headerLayout.addLayout(headerLeftLayout, 3)
        # headerLeft - fileName
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedHeight(labelHeight)
        headerLeftLayout.addWidget(self.fileNameLabel)
        # headerLeft - space
        headerLeftLayout.addSpacing(10)
        # headerLeft - tabCombo
        self.tabCombo = QComboBox(font=font2)
        self.tabCombo.setEnabled(False)
        headerLeftLayout.addWidget(self.tabCombo)

        # space
        headerLayout.addSpacing(30)

        # headerRight
        headerRightLayout = QVBoxLayout()
        headerRightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addLayout(headerRightLayout, 9)
        # headerRight - gameListLayout
        gameListLayout = QHBoxLayout()
        headerRightLayout.addLayout(gameListLayout)
        # headerRight - gameListLayout - lsRadioLayout
        lsRadioLayout = QVBoxLayout()
        lsRadioLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gameListLayout.addLayout(lsRadioLayout)
        gameListLayout.addStretch()
        # headerRight - gameListLayout - lsRadioLayout - lsRadio
        lsRadioButton = QRadioButton("Lightning Stage")
        lsRadioLayout.addWidget(lsRadioButton, 1)
        # headerRight - gameListLayout - lsRadioLayout - lsTrialRadio
        lsTrialRadioButton = QRadioButton("Lightning Stage(体験版)")
        lsRadioLayout.addWidget(lsTrialRadioButton, 1)

        # headerRight - gameListLayout - bsRaioLayout
        bsRadioLayout = QVBoxLayout()
        bsRadioLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gameListLayout.addLayout(bsRadioLayout)
        gameListLayout.addStretch()
        # headerRight - gameListLayout - bsRaioLayout - bsRadio
        bsRadioButton = QRadioButton("Burning Stage")
        bsRadioLayout.addWidget(bsRadioButton, 1)

        # headerRight - gameListLayout - csRaioLayout
        csRadioLayout = QVBoxLayout()
        csRadioLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gameListLayout.addLayout(csRadioLayout)
        gameListLayout.addStretch()
        # headerRight - gameListLayout - csRaioLayout - csRadio
        csRadioButton = QRadioButton("Climax Stage")
        csRadioLayout.addWidget(csRadioButton, 1)

        # headerRight - gameListLayout - rsRaioLayout
        rsRadioLayout = QVBoxLayout()
        rsRadioLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        gameListLayout.addLayout(rsRadioLayout)
        gameListLayout.addSpacing(30)
        # headerRight - gameListLayout - rsRaioLayout - rsRadio
        rsRadioButton = QRadioButton("Rising Stage")
        rsRadioButton.setChecked(True)
        rsRadioLayout.addWidget(rsRadioButton, 1)

        # headerRight - buttonLayout
        excelButtonLayout = QHBoxLayout()
        headerRightLayout.addLayout(excelButtonLayout)
        # headerRight - buttonLayout - space
        excelButtonLayout.addStretch()
        # headerRight - buttonLayout - button1
        self.excelExtractButton = QPushButton(textSetting.textList["railEditor"]["railDataExtractExcel"])
        self.excelExtractButton.setFixedSize(buttonWidth, buttonHeight)
        self.excelExtractButton.setEnabled(False)
        excelButtonLayout.addWidget(self.excelExtractButton)
        # headerRight - buttonLayout - space
        excelButtonLayout.addStretch()
        # headerRight - buttonLayout - button2
        self.excelSaveButton = QPushButton(textSetting.textList["railEditor"]["railDataSaveExcel"])
        self.excelSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.excelSaveButton.setEnabled(False)
        excelButtonLayout.addWidget(self.excelSaveButton)
        # headerRight - buttonLayout - stretch
        excelButtonLayout.addStretch()

        # content(scroll area)
        self.contentScrollArea = QScrollArea()
        mainLayout.addWidget(self.contentScrollArea, 14)

        lsRadioButton.toggled.connect(self.radioButtonTrigger)
        lsTrialRadioButton.toggled.connect(self.radioButtonTrigger)
        bsRadioButton.toggled.connect(self.radioButtonTrigger)
        csRadioButton.toggled.connect(self.radioButtonTrigger)
        rsRadioButton.toggled.connect(self.radioButtonTrigger)
        # RadioGroup
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(lsTrialRadioButton, self.LSTrial)
        self.radioGroup.addButton(lsRadioButton, self.LS)
        self.radioGroup.addButton(bsRadioButton, self.BS)
        self.radioGroup.addButton(csRadioButton, self.CS)
        self.radioGroup.addButton(rsRadioButton, self.RS)

    def radioButtonTrigger(self, isChecked):
        if not isChecked:
            return

        self.fileNameLabel.setText("")
        self.tabCombo.clear()
        self.tabCombo.setEnabled(False)
        self.excelExtractButton.setEnabled(False)
        self.excelSaveButton.setEnabled(False)
        self.clearContent()

    def clearContent(self):
        widget = self.contentScrollArea.widget()
        if not widget:
            return

        widget.deleteLater()
        self.contentScrollArea.setWidget(None)

    def openFile(self):
        fileType = "{0} ({1})".format(textSetting.textList["railEditor"]["fileType"], "*.BIN")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.fileNameLabel.setText(filename)
            del self.decryptFile
            self.decryptFile = None

            selectedRadioId = self.radioGroup.checkedId()
            if selectedRadioId == self.RS:
                self.decryptFile = dendRs.RailDecrypt(file_path)
            elif selectedRadioId == self.CS:
                self.decryptFile = dendCs.RailDecrypt(file_path)
            elif selectedRadioId == self.BS:
                self.decryptFile = dendBs.RailDecrypt(file_path)
            elif selectedRadioId == self.LS:
                self.decryptFile = dendLs.RailDecrypt(file_path)
            elif selectedRadioId == self.LSTrial:
                self.decryptFile = dendLsTrial.RailDecrypt(file_path)

            if not self.decryptFile.open():
                if self.decryptFile.error == "":
                    errorMsg = textSetting.textList["errorList"]["E76"].format(self.decryptFile.game)
                    mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                else:
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E21"])
                return

            self.clearContent()
            self.tabCombo.clear()
            self.tabCombo.setEnabled(True)
            if selectedRadioId in [self.LS, self.LSTrial]:
                self.tabCombo.addItems(textSetting.textList["railEditor"]["railLsComboValue"])
            else:
                self.tabCombo.addItems(textSetting.textList["railEditor"]["railComboValue"])

            self.excelExtractButton.setEnabled(True)
            self.excelSaveButton.setEnabled(True)
            self.selectInfo(self.tabCombo.currentIndex())

    def selectInfo(self, selectId=None):
        pass
