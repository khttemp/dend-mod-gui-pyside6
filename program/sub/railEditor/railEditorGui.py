import traceback

import program.sub.textSetting as textSetting
import program.sub.railEditor.railEditorProcess as railEditorProcess

from PySide6.QtWidgets import (
    QWidget, QFrame, QScrollArea, QLabel, QComboBox,
    QRadioButton, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class RailEditorWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
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
        contentScrollArea = QScrollArea()
        mainLayout.addWidget(contentScrollArea, 14)
