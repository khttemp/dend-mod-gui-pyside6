from functools import partial

import program.sub.textSetting as textSetting
import program.sub.ssUnity.ssUnityProcess as ssUnityProcess

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QFrame, QGroupBox,
    QVBoxLayout, QHBoxLayout,
    QRadioButton, QComboBox, QPushButton, QButtonGroup
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class SSUnityWindow(QWidget):
    def __init__(self):
        super().__init__()
        ssUnityProcess.readModelInfo("model.json")

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font7 = QFont(textSetting.textList["font7"][0], textSetting.textList["font7"][1])
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
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerLeftLayout, 3)
        # headerLeft - fileName
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedHeight(labelHeight)
        headerLeftLayout.addWidget(self.fileNameLabel)

        # headerLeft - select
        headerSelectLayout = QHBoxLayout()
        headerSelectLayout.setContentsMargins(0, 15, 0, 15)
        headerLeftLayout.addLayout(headerSelectLayout)
        # headerLeft - select - Label1
        selectLabel = QLabel(textSetting.textList["ssUnity"]["selectNum"], font=font2)
        selectLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(selectLabel, 8)
        # headerLeft - select - Label2
        self.selectLineLabel = QLabel("", font=font2)
        self.selectLineLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.selectLineLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selectLineLabel.setFixedHeight(labelHeight)
        headerSelectLayout.addWidget(self.selectLineLabel, 3)

        # headerLeft - search
        headerSearchLayout = QHBoxLayout()
        headerLeftLayout.addLayout(headerSearchLayout)
        # headerLeft - search - Label
        searchLabel = QLabel(textSetting.textList["ssUnity"]["searchText"], font=font2)
        headerSearchLayout.addWidget(searchLabel, 1)
        # headerLeft - search - LineEdit
        self.searchLineEdit = QLineEdit("", font=font7)
        self.searchLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerSearchLayout.addWidget(self.searchLineEdit, 9)

        # headerRight
        headerRightLayout = QVBoxLayout()
        headerRightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        headerLayout.addSpacing(20)
        headerLayout.addLayout(headerRightLayout, 9)

        # headerRight - radioLayout
        headerRadioLayout = QHBoxLayout()
        headerRadioLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRadioLayout)
        # headerRight - radioLayout - combo
        self.monoCombo = QComboBox(font=font2)
        headerRadioLayout.addWidget(self.monoCombo, 1)
        headerRadioLayout.addSpacing(50)
        # headerRight - radioLayout - radio1
        self.denRadioButton = QRadioButton(textSetting.textList["ssUnity"]["editDenFile"])
        self.denRadioButton.toggled.connect(partial(self.radioButtonTrigger, "den"))
        headerRadioLayout.addWidget(self.denRadioButton, 1)
        # headerRight - radioLayout - radio2
        self.resourcesRadioButton = QRadioButton(textSetting.textList["ssUnity"]["editResourcesAssets"])
        self.resourcesRadioButton.toggled.connect(partial(self.radioButtonTrigger, "resources"))
        headerRadioLayout.addWidget(self.resourcesRadioButton, 1)
        headerRightLayout.addSpacing(10)
        # RadioGroup
        radioGroup = QButtonGroup()
        radioGroup.addButton(self.denRadioButton)
        radioGroup.addButton(self.resourcesRadioButton)

        # headerRight - buttonLayout
        headerRightButtonLayout = QHBoxLayout()
        headerRightButtonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headerRightLayout.addLayout(headerRightButtonLayout)
        # headerRight - buttonLayout - button1
        self.extractButton = QPushButton(textSetting.textList["ssUnity"]["extractFileLabel"])
        self.extractButton.setFixedSize(buttonWidth, buttonHeight)
        headerRightButtonLayout.addWidget(self.extractButton)
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout - button2
        self.loadAndSaveButton = QPushButton(textSetting.textList["ssUnity"]["saveFileLabel"])
        self.loadAndSaveButton.setFixedSize(buttonWidth, buttonHeight)
        headerRightButtonLayout.addWidget(self.loadAndSaveButton)
        headerRightButtonLayout.addStretch(1)
        # headerRight - buttonLayout - button3
        self.assertsSaveButton = QPushButton(textSetting.textList["ssUnity"]["saveResourcesAssets"])
        self.assertsSaveButton.setFixedSize(buttonWidth, buttonHeight)
        headerRightButtonLayout.addWidget(self.assertsSaveButton, 1)

        # content
        self.contentFrame = QGroupBox(textSetting.textList["ssUnity"]["scriptLabel"])
        mainLayout.addWidget(self.contentFrame, 11)

        # hide setting
        monoComboSize = self.monoCombo.sizePolicy()
        monoComboSize.setRetainSizeWhenHidden(True)
        self.monoCombo.setSizePolicy(monoComboSize)
        assertsSaveButtonSize = self.assertsSaveButton.sizePolicy()
        assertsSaveButtonSize.setRetainSizeWhenHidden(True)
        self.assertsSaveButton.setSizePolicy(assertsSaveButtonSize)

        # radioButton default setting
        self.denRadioButton.setChecked(True)

    def radioButtonTrigger(self, buttonName, isChecked):
        if not isChecked:
            return

        if buttonName == "den":
            self.monoCombo.hide()
            self.assertsSaveButton.hide()
        elif buttonName == "resources":
            self.monoCombo.show()
            self.assertsSaveButton.show()
