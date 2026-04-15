import copy
from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QButtonGroup,
    QComboBox, QCheckBox, QSizePolicy, QFileDialog
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class RailListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.railList = decryptFile.railList
        self.varRailList = []
        self.varRevRailList = []
        self.reloadFunc = reloadFunc
        self.font2 = QFont(textSetting.textList["font6"][0], textSetting.textList["font2"][1])

        if self.decryptFile.game in ["CS", "RS"]:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList1"])
        else:
            self.smfList.extend(textSetting.textList["railEditor"]["smfListAddList2"])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(self.setFirstHorizontalLayout())

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            mainLayout.addLayout(self.setDefaultSecondHorizontalLayout())
        elif self.decryptFile.game == "LS":
            mainLayout.addLayout(self.setLsSecondHorizontalLayout())
            mainLayout.addLayout(self.setLsModelInfoHorizontalLayout())
        elif self.decryptFile.game == "LSTrial":
            mainLayout.addLayout(self.setLsTrialSecondHorizontalLayout())
            mainLayout.addLayout(self.setLsTrialModelInfoHorizontalLayout())

        flagInfoLayout = self.setFlagInfoLayout()
        if flagInfoLayout is not None:
            mainLayout.addLayout(flagInfoLayout)
        railDataInfoLayout = self.setRailDataInfoLayout()
        if railDataInfoLayout is not None:
            mainLayout.addLayout(railDataInfoLayout)
        mainLayout.addStretch(1)

    def setFirstHorizontalLayout(self):
        buttonWidth = 180
        buttonHeight = 28
        lineEditWidth = 86
        lineEditHeight = 40

        # horizontalLayout
        horizontalLayout = QHBoxLayout()
        # space
        horizontalLayout.addSpacing(20)
        # horizontalLayout - railNoLayout
        railNoLayout = QHBoxLayout()
        railNoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        horizontalLayout.addLayout(railNoLayout)
        # horizontalLayout - railNoLayout - railNoNameLabel
        railNoNameLabel = QLabel(textSetting.textList["railEditor"]["railRailNo"], font=self.font2)
        railNoLayout.addWidget(railNoNameLabel)
        # space
        railNoLayout.addSpacing(15)
        # horizontalLayout - railNoLayout - railNoLabel
        self.railNoLineEdit = QLineEdit("0", font=self.font2)
        self.railNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.railNoLineEdit.setFixedSize(lineEditWidth, lineEditHeight)
        self.railNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.railNoLineEdit.setValidator(integerValidator)
        railNoLayout.addWidget(self.railNoLineEdit)

        # space
        railNoLayout.addSpacing(30)
        # horizontalLayout - railNoLayout - searchRailButton
        searchRailButton = QPushButton(textSetting.textList["railEditor"]["railSearchBtnLabel"])
        searchRailButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        searchRailButton.clicked.connect(self.searchRail)
        railNoLayout.addWidget(searchRailButton)
        # space
        horizontalLayout.addSpacing(60)
        # horizontalLayout - csvButtonLayout
        csvButtonLayout = QHBoxLayout()
        horizontalLayout.addLayout(csvButtonLayout)
        # horizontalLayout - csvButtonLayout - csvExtractButton
        csvExtractButton = QPushButton(textSetting.textList["railEditor"]["railCsvExtractLabel"])
        csvExtractButton.setFixedSize(buttonWidth, buttonHeight)
        csvExtractButton.clicked.connect(self.extractCsv)
        csvButtonLayout.addWidget(csvExtractButton)
        # space
        csvButtonLayout.addSpacing(20)
        # horizontalLayout - csvButtonLayout - csvSaveButton
        csvSaveButton = QPushButton(textSetting.textList["railEditor"]["railCsvSaveLabel"])
        csvSaveButton.setFixedSize(buttonWidth, buttonHeight)
        csvSaveButton.clicked.connect(self.saveCsv)
        csvButtonLayout.addWidget(csvSaveButton)
        if self.decryptFile.game == "CS":
            # space
            csvButtonLayout.addSpacing(20)
            csToRsButton = QPushButton(textSetting.textList["railEditor"]["railCsToRs"])
            csToRsButton.setFixedSize(buttonWidth - 50, buttonHeight)
            csToRsButton.clicked.connect(self.csToRs)
            csvButtonLayout.addWidget(csToRsButton)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setDefaultSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30

        # horizontalLayout
        horizontalLayout = QHBoxLayout()
        # QGroupBox
        blockGroupBox = QGroupBox(textSetting.textList["railEditor"]["railBlockInfo"])
        horizontalLayout.addWidget(blockGroupBox)
        # QGroupBox - QGridLayout
        blockGridLayout = QGridLayout()
        blockGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        blockGridLayout.setVerticalSpacing(20)
        blockGroupBox.setLayout(blockGridLayout)
        # QGroupBox - QGridLayout - prevRailNameLabel
        prevRailNameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRailNo"], font=self.font2)
        blockGridLayout.addWidget(prevRailNameLabel, 0, 0)
        # QGroupBox - QGridLayout - prevRailLabel
        self.prevRailLabel = QLabel("", font=self.font2)
        self.prevRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.prevRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prevRailLabel.setFixedSize(labelWidth, labelHeight)
        blockGridLayout.addWidget(self.prevRailLabel, 0, 1)
        # QGroupBox - QGridLayout - blockNameLabel
        blockNameLabel = QLabel(textSetting.textList["railEditor"]["railBlockNo"], font=self.font2)
        blockGridLayout.addWidget(blockNameLabel, 1, 0)
        # QGroupBox - QGridLayout - blockLabel
        self.blockLabel = QLabel("", font=self.font2)
        self.blockLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.blockLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blockLabel.setFixedSize(labelWidth, labelHeight)
        blockGridLayout.addWidget(self.blockLabel, 1, 1)

        # QGroupBox
        railXyzGroupBox = QGroupBox(textSetting.textList["railEditor"]["railXyzInfo"])
        horizontalLayout.addWidget(railXyzGroupBox)
        # QGroupBox - QGridLayout
        xyzGridLayout = QGridLayout()
        xyzGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        xyzGridLayout.setVerticalSpacing(20)
        railXyzGroupBox.setLayout(xyzGridLayout)
        # QGroupBox - QGridLayout - railDirXNameLabel
        railDirXNameLabel = QLabel(textSetting.textList["railEditor"]["railDirX"], font=self.font2)
        xyzGridLayout.addWidget(railDirXNameLabel, 0, 0)
        # QGroupBox - QGridLayout - railDirXLabel
        self.railDirXLabel = QLabel("", font=self.font2)
        self.railDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirXLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirXLabel, 0, 1)
        # QGroupBox - QGridLayout - railDirYNameLabel
        railDirYNameLabel = QLabel(textSetting.textList["railEditor"]["railDirY"], font=self.font2)
        xyzGridLayout.addWidget(railDirYNameLabel, 1, 0)
        # QGroupBox - QGridLayout - railDirYLabel
        self.railDirYLabel = QLabel("", font=self.font2)
        self.railDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirYLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirYLabel, 1, 1)
        # QGroupBox - QGridLayout - railDirZNameLabel
        railDirZNameLabel = QLabel(textSetting.textList["railEditor"]["railDirZ"], font=self.font2)
        xyzGridLayout.addWidget(railDirZNameLabel, 2, 0)
        # QGroupBox - QGridLayout - railDirZLabel
        self.railDirZLabel = QLabel("", font=self.font2)
        self.railDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirZLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirZLabel, 2, 1)

        # QGroupBox
        modelKasenGroupBox = QGroupBox(textSetting.textList["railEditor"]["railModelKasenInfo"])
        horizontalLayout.addWidget(modelKasenGroupBox)
        # QGroupBox - QGridLayout
        modelKasenGridLayout = QGridLayout()
        modelKasenGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        modelKasenGridLayout.setVerticalSpacing(20)
        modelKasenGroupBox.setLayout(modelKasenGridLayout)
        # QGroupBox - QGridLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(modelNameLabel, 0, 0)
        # QGroupBox - QGridLayout - modelNameCombo
        self.modelNameCombo = QComboBox(font=self.font2)
        self.modelNameCombo.addItem("")
        self.modelNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.modelNameCombo, 0, 1)
        # QGroupBox - QGridLayout - kasenNameLabel
        kasenNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(kasenNameLabel, 1, 0)
        # QGroupBox - QGridLayout - kasenNameCombo
        self.kasenNameCombo = QComboBox(font=self.font2)
        self.kasenNameCombo.addItem("")
        self.kasenNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.kasenNameCombo, 1, 1)
        # QGroupBox - QGridLayout - kasenchuNameLabel
        kasenchuNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenchuLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(kasenchuNameLabel, 2, 0)
        # QGroupBox - QGridLayout - kasenchuNameCombo
        self.kasenchuNameCombo = QComboBox(font=self.font2)
        self.kasenchuNameCombo.addItem("")
        self.kasenchuNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.kasenchuNameCombo, 2, 1)
        # QGroupBox - QGridLayout - perNameLabel
        perNameLabel = QLabel(textSetting.textList["railEditor"]["railPer"], font=self.font2)
        modelKasenGridLayout.addWidget(perNameLabel, 3, 0)
        # QGroupBox - QGridLayout - perLabel
        self.perLabel = QLabel("", font=self.font2)
        self.perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modelKasenGridLayout.addWidget(self.perLabel, 3, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30

        # horizontalLayout
        horizontalLayout = QHBoxLayout()
        if self.decryptFile.ver == "DEND_MAP_VER0101":
            # QGroupBox
            verGroupBox = QGroupBox(textSetting.textList["railEditor"]["railLsVer0101"])
            horizontalLayout.addWidget(verGroupBox)
            # QGroupBox - QGridLayout
            verGridLayout = QGridLayout()
            verGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            verGridLayout.setVerticalSpacing(20)
            verGroupBox.setLayout(verGridLayout)
            # QGroupBox - QGridLayout - prevRail2NameLabel
            prevRail2NameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRail2No"], font=self.font2)
            verGridLayout.addWidget(prevRail2NameLabel, 0, 0)
            # QGroupBox - QGridLayout - prevRail2Label
            self.prevRail2Label = QLabel("", font=self.font2)
            self.prevRail2Label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.prevRail2Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.prevRail2Label.setFixedSize(labelWidth, labelHeight)
            verGridLayout.addWidget(self.prevRail2Label, 0, 1)

        # QGroupBox
        railXyzGroupBox = QGroupBox(textSetting.textList["railEditor"]["railPosXyzInfo"])
        horizontalLayout.addWidget(railXyzGroupBox)
        # QGroupBox - QGridLayout
        xyzGridLayout = QGridLayout()
        xyzGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        xyzGridLayout.setVerticalSpacing(20)
        railXyzGroupBox.setLayout(xyzGridLayout)
        # QGroupBox - QGridLayout - railPosXNameLabel
        railPosXNameLabel = QLabel(textSetting.textList["railEditor"]["railPosX"], font=self.font2)
        xyzGridLayout.addWidget(railPosXNameLabel, 0, 0)
        # QGroupBox - QGridLayout - railPosXLabel
        self.railPosXLabel = QLabel("", font=self.font2)
        self.railPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosXLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosXLabel, 0, 1)
        # QGroupBox - QGridLayout - railDirYNameLabel
        railPosYNameLabel = QLabel(textSetting.textList["railEditor"]["railPosY"], font=self.font2)
        xyzGridLayout.addWidget(railPosYNameLabel, 1, 0)
        # QGroupBox - QGridLayout - railPosYLabel
        self.railPosYLabel = QLabel("", font=self.font2)
        self.railPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosYLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosYLabel, 1, 1)
        # QGroupBox - QGridLayout - railPosZNameLabel
        railPosZNameLabel = QLabel(textSetting.textList["railEditor"]["railPosZ"], font=self.font2)
        xyzGridLayout.addWidget(railPosZNameLabel, 2, 0)
        # QGroupBox - QGridLayout - railPosZLabel
        self.railPosZLabel = QLabel("", font=self.font2)
        self.railPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosZLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosZLabel, 2, 1)

        # QGroupBox - QGridLayout - railDirXNameLabel
        railDirXNameLabel = QLabel(textSetting.textList["railEditor"]["railDirX"], font=self.font2)
        xyzGridLayout.addWidget(railDirXNameLabel, 0, 2)
        # QGroupBox - QGridLayout - railDirXLabel
        self.railDirXLabel = QLabel("", font=self.font2)
        self.railDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirXLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirXLabel, 0, 3)
        # QGroupBox - QGridLayout - railDirYNameLabel
        railDirYNameLabel = QLabel(textSetting.textList["railEditor"]["railDirY"], font=self.font2)
        xyzGridLayout.addWidget(railDirYNameLabel, 1, 2)
        # QGroupBox - QGridLayout - railDirYLabel
        self.railDirYLabel = QLabel("", font=self.font2)
        self.railDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirYLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirYLabel, 1, 3)
        # QGroupBox - QGridLayout - railDirZNameLabel
        railDirZNameLabel = QLabel(textSetting.textList["railEditor"]["railDirZ"], font=self.font2)
        xyzGridLayout.addWidget(railDirZNameLabel, 2, 2)
        # QGroupBox - QGridLayout - railDirZLabel
        self.railDirZLabel = QLabel("", font=self.font2)
        self.railDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirZLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirZLabel, 2, 3)

        # QGroupBox
        railXyzRotGroupBox = QGroupBox(textSetting.textList["railEditor"]["railRotXyzInfo"])
        horizontalLayout.addWidget(railXyzRotGroupBox)
        # QGroupBox - QGridLayout
        xyzRotGridLayout = QGridLayout()
        xyzRotGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        xyzRotGridLayout.setVerticalSpacing(20)
        railXyzRotGroupBox.setLayout(xyzRotGridLayout)
        # QGroupBox - QGridLayout - railRotXNameLabel
        railRotXNameLabel = QLabel(textSetting.textList["railEditor"]["railRotX"], font=self.font2)
        xyzRotGridLayout.addWidget(railRotXNameLabel, 0, 0)
        # QGroupBox - QGridLayout - railRotXLabel
        self.railRotXLabel = QLabel("", font=self.font2)
        self.railRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railRotXLabel.setFixedSize(labelWidth, labelHeight)
        xyzRotGridLayout.addWidget(self.railRotXLabel, 0, 1)
        # QGroupBox - QGridLayout - railRotYNameLabel
        railRotYNameLabel = QLabel(textSetting.textList["railEditor"]["railRotY"], font=self.font2)
        xyzRotGridLayout.addWidget(railRotYNameLabel, 1, 0)
        # QGroupBox - QGridLayout - railRotYLabel
        self.railRotYLabel = QLabel("", font=self.font2)
        self.railRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railRotYLabel.setFixedSize(labelWidth, labelHeight)
        xyzRotGridLayout.addWidget(self.railRotYLabel, 1, 1)
        # QGroupBox - QGridLayout - railRotZNameLabel
        railRotZNameLabel = QLabel(textSetting.textList["railEditor"]["railRotZ"], font=self.font2)
        xyzRotGridLayout.addWidget(railRotZNameLabel, 2, 0)
        # QGroupBox - QGridLayout - railRotZLabel
        self.railRotZLabel = QLabel("", font=self.font2)
        self.railRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railRotZLabel.setFixedSize(labelWidth, labelHeight)
        xyzRotGridLayout.addWidget(self.railRotZLabel, 2, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsModelInfoHorizontalLayout(self):
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        modelKasenGroupBox = QGroupBox(textSetting.textList["railEditor"]["railModelKasenInfo"])
        horizontalLayout.addWidget(modelKasenGroupBox)
        # QGroupBox - QGridLayout
        modelKasenGridLayout = QGridLayout()
        modelKasenGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        modelKasenGridLayout.setVerticalSpacing(20)
        modelKasenGroupBox.setLayout(modelKasenGridLayout)
        # QGroupBox - QGridLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(modelNameLabel, 0, 0)
        # QGroupBox - QGridLayout - modelNameCombo
        self.modelNameCombo = QComboBox(font=self.font2)
        self.modelNameCombo.addItem("")
        self.modelNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.modelNameCombo, 0, 1)
        # QGroupBox - QGridLayout - prevRail2NameLabel
        prevRailNameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRailNo"], font=self.font2)
        modelKasenGridLayout.addWidget(prevRailNameLabel, 0, 2)
        # QGroupBox - QGridLayout - prevRail2Label
        self.prevRailLabel = QLabel("", font=self.font2)
        self.prevRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.prevRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modelKasenGridLayout.addWidget(self.prevRailLabel, 0, 3)
        # QGroupBox - QGridLayout - kasenchuNameLabel
        kasenchuNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenchuLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(kasenchuNameLabel, 1, 0)
        # QGroupBox - QGridLayout - kasenchuNameCombo
        self.kasenchuNameCombo = QComboBox(font=self.font2)
        self.kasenchuNameCombo.addItem("")
        self.kasenchuNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.kasenchuNameCombo, 1, 1)
        # QGroupBox - QGridLayout - kasenNameLabel
        kasenNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(kasenNameLabel, 1, 2)
        # QGroupBox - QGridLayout - kasenNameCombo
        self.kasenNameCombo = QComboBox(font=self.font2)
        self.kasenNameCombo.addItem("")
        self.kasenNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.kasenNameCombo, 1, 3)
        # QGroupBox - QGridLayout - fixAmbNameLabel
        fixAmbNameLabel = QLabel(textSetting.textList["railEditor"]["railFixAmbLabel"], font=self.font2)
        modelKasenGridLayout.addWidget(fixAmbNameLabel, 2, 0)
        # QGroupBox - QGridLayout - fixAmbNameCombo
        self.fixAmbNameCombo = QComboBox(font=self.font2)
        self.fixAmbNameCombo.addItem("")
        self.fixAmbNameCombo.addItems(self.smfList)
        modelKasenGridLayout.addWidget(self.fixAmbNameCombo, 2, 1)
        # QGroupBox - QGridLayout - perNameLabel
        perNameLabel = QLabel(textSetting.textList["railEditor"]["railPer"], font=self.font2)
        modelKasenGridLayout.addWidget(perNameLabel, 2, 2)
        # QGroupBox - QGridLayout - perLabel
        self.perLabel = QLabel("", font=self.font2)
        self.perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modelKasenGridLayout.addWidget(self.perLabel, 2, 3)
        return horizontalLayout

    def setLsTrialSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        railXyzGroupBox = QGroupBox(textSetting.textList["railEditor"]["railPosXyzInfo"])
        horizontalLayout.addWidget(railXyzGroupBox)
        # QGroupBox - QGridLayout
        xyzGridLayout = QGridLayout()
        xyzGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        xyzGridLayout.setVerticalSpacing(20)
        railXyzGroupBox.setLayout(xyzGridLayout)
        # QGroupBox - QGridLayout - railPosXNameLabel
        railPosXNameLabel = QLabel(textSetting.textList["railEditor"]["railPosX"], font=self.font2)
        xyzGridLayout.addWidget(railPosXNameLabel, 0, 0)
        # QGroupBox - QGridLayout - railPosXLabel
        self.railPosXLabel = QLabel("", font=self.font2)
        self.railPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosXLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosXLabel, 0, 1)
        # QGroupBox - QGridLayout - railDirYNameLabel
        railPosYNameLabel = QLabel(textSetting.textList["railEditor"]["railPosY"], font=self.font2)
        xyzGridLayout.addWidget(railPosYNameLabel, 1, 0)
        # QGroupBox - QGridLayout - railPosYLabel
        self.railPosYLabel = QLabel("", font=self.font2)
        self.railPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosYLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosYLabel, 1, 1)
        # QGroupBox - QGridLayout - railPosZNameLabel
        railPosZNameLabel = QLabel(textSetting.textList["railEditor"]["railPosZ"], font=self.font2)
        xyzGridLayout.addWidget(railPosZNameLabel, 2, 0)
        # QGroupBox - QGridLayout - railPosZLabel
        self.railPosZLabel = QLabel("", font=self.font2)
        self.railPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosZLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railPosZLabel, 2, 1)

        # QGroupBox - QGridLayout - railDirXNameLabel
        railDirXNameLabel = QLabel(textSetting.textList["railEditor"]["railDirX"], font=self.font2)
        xyzGridLayout.addWidget(railDirXNameLabel, 0, 2)
        # QGroupBox - QGridLayout - railDirXLabel
        self.railDirXLabel = QLabel("", font=self.font2)
        self.railDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirXLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirXLabel, 0, 3)
        # QGroupBox - QGridLayout - railDirYNameLabel
        railDirYNameLabel = QLabel(textSetting.textList["railEditor"]["railDirY"], font=self.font2)
        xyzGridLayout.addWidget(railDirYNameLabel, 1, 2)
        # QGroupBox - QGridLayout - railDirYLabel
        self.railDirYLabel = QLabel("", font=self.font2)
        self.railDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirYLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirYLabel, 1, 3)
        # QGroupBox - QGridLayout - railDirZNameLabel
        railDirZNameLabel = QLabel(textSetting.textList["railEditor"]["railDirZ"], font=self.font2)
        xyzGridLayout.addWidget(railDirZNameLabel, 2, 2)
        # QGroupBox - QGridLayout - railDirZLabel
        self.railDirZLabel = QLabel("", font=self.font2)
        self.railDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirZLabel.setFixedSize(labelWidth, labelHeight)
        xyzGridLayout.addWidget(self.railDirZLabel, 2, 3)

        if self.decryptFile.oldFlag:
            # QGroupBox
            railInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["railRailInfo"])
            horizontalLayout.addWidget(railInfoGroupBox)
            # QGroupBox - QGridLayout
            railInfoGridLayout = QGridLayout()
            railInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            railInfoGridLayout.setVerticalSpacing(20)
            railInfoGroupBox.setLayout(railInfoGridLayout)
            # QGroupBox - QGridLayout - nextRailNameLabel
            nextRailNameLabel = QLabel(textSetting.textList["railEditor"]["railNextRail"], font=self.font2)
            railInfoGridLayout.addWidget(nextRailNameLabel, 0, 0)
            # QGroupBox - QGridLayout - nextRailLabel
            self.nextRailLabel = QLabel("", font=self.font2)
            self.nextRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.nextRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.nextRailLabel.setFixedSize(labelWidth, labelHeight)
            railInfoGridLayout.addWidget(self.nextRailLabel, 0, 1)
            # QGroupBox - QGridLayout - prevRailNameLabel
            prevRailNameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRail"], font=self.font2)
            railInfoGridLayout.addWidget(prevRailNameLabel, 1, 0)
            # QGroupBox - QGridLayout - prevRailLabel
            self.prevRailLabel = QLabel("", font=self.font2)
            self.prevRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.prevRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.prevRailLabel.setFixedSize(labelWidth, labelHeight)
            railInfoGridLayout.addWidget(self.prevRailLabel, 1, 1)
        else:
            if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                # QGroupBox
                railXyzRotGroupBox = QGroupBox(textSetting.textList["railEditor"]["railRotXyzInfo"])
                horizontalLayout.addWidget(railXyzRotGroupBox)
                # QGroupBox - QGridLayout
                xyzRotGridLayout = QGridLayout()
                xyzRotGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
                xyzRotGridLayout.setVerticalSpacing(20)
                railXyzRotGroupBox.setLayout(xyzRotGridLayout)
                # QGroupBox - QGridLayout - railRotXNameLabel
                railRotXNameLabel = QLabel(textSetting.textList["railEditor"]["railRotX"], font=self.font2)
                xyzRotGridLayout.addWidget(railRotXNameLabel, 0, 0)
                # QGroupBox - QGridLayout - railRotXLabel
                self.railRotXLabel = QLabel("", font=self.font2)
                self.railRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                self.railRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.railRotXLabel.setFixedSize(labelWidth, labelHeight)
                xyzRotGridLayout.addWidget(self.railRotXLabel, 0, 1)
                # QGroupBox - QGridLayout - railRotYNameLabel
                railRotYNameLabel = QLabel(textSetting.textList["railEditor"]["railRotY"], font=self.font2)
                xyzRotGridLayout.addWidget(railRotYNameLabel, 1, 0)
                # QGroupBox - QGridLayout - railRotYLabel
                self.railRotYLabel = QLabel("", font=self.font2)
                self.railRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                self.railRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.railRotYLabel.setFixedSize(labelWidth, labelHeight)
                xyzRotGridLayout.addWidget(self.railRotYLabel, 1, 1)
                # QGroupBox - QGridLayout - railRotZNameLabel
                railRotZNameLabel = QLabel(textSetting.textList["railEditor"]["railRotZ"], font=self.font2)
                xyzRotGridLayout.addWidget(railRotZNameLabel, 2, 0)
                # QGroupBox - QGridLayout - railRotZLabel
                self.railRotZLabel = QLabel("", font=self.font2)
                self.railRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                self.railRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.railRotZLabel.setFixedSize(labelWidth, labelHeight)
                xyzRotGridLayout.addWidget(self.railRotZLabel, 2, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsTrialModelInfoHorizontalLayout(self):
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        if self.decryptFile.oldFlag:
            # QGroupBox
            modelKasenGroupBox = QGroupBox(textSetting.textList["railEditor"]["railModelKasenInfo"])
            horizontalLayout.addWidget(modelKasenGroupBox)
            # QGroupBox - QGridLayout
            modelKasenGridLayout = QGridLayout()
            modelKasenGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            modelKasenGridLayout.setVerticalSpacing(20)
            modelKasenGroupBox.setLayout(modelKasenGridLayout)
            # QGroupBox - QGridLayout - modelNameLabel
            modelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(modelNameLabel, 0, 0)
            # QGroupBox - QGridLayout - modelNameCombo
            self.modelNameCombo = QComboBox(font=self.font2)
            self.modelNameCombo.addItem("")
            self.modelNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.modelNameCombo, 0, 1)
            # QGroupBox - QGridLayout - kasenNameLabel
            kasenNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(kasenNameLabel, 0, 2)
            # QGroupBox - QGridLayout - kasenNameCombo
            self.kasenNameCombo = QComboBox(font=self.font2)
            self.kasenNameCombo.addItem("")
            self.kasenNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.kasenNameCombo, 0, 3)
        else:
            # QGroupBox
            modelKasenGroupBox = QGroupBox(textSetting.textList["railEditor"]["railModelKasenInfo"])
            horizontalLayout.addWidget(modelKasenGroupBox)
            # QGroupBox - QGridLayout
            modelKasenGridLayout = QGridLayout()
            modelKasenGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            modelKasenGridLayout.setVerticalSpacing(20)
            modelKasenGroupBox.setLayout(modelKasenGridLayout)
            # QGroupBox - QGridLayout - modelNameLabel
            modelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(modelNameLabel, 0, 0)
            # QGroupBox - QGridLayout - modelNameCombo
            self.modelNameCombo = QComboBox(font=self.font2)
            self.modelNameCombo.addItem("")
            self.modelNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.modelNameCombo, 0, 1)
            # QGroupBox - QGridLayout - prevRail2NameLabel
            prevRailNameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRailNo"], font=self.font2)
            modelKasenGridLayout.addWidget(prevRailNameLabel, 0, 2)
            # QGroupBox - QGridLayout - prevRail2Label
            self.prevRailLabel = QLabel("", font=self.font2)
            self.prevRailLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.prevRailLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            modelKasenGridLayout.addWidget(self.prevRailLabel, 0, 3)
            # QGroupBox - QGridLayout - kasenchuNameLabel
            kasenchuNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenchuLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(kasenchuNameLabel, 1, 0)
            # QGroupBox - QGridLayout - kasenchuNameCombo
            self.kasenchuNameCombo = QComboBox(font=self.font2)
            self.kasenchuNameCombo.addItem("")
            self.kasenchuNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.kasenchuNameCombo, 1, 1)
            # QGroupBox - QGridLayout - kasenNameLabel
            kasenNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(kasenNameLabel, 1, 2)
            # QGroupBox - QGridLayout - kasenNameCombo
            self.kasenNameCombo = QComboBox(font=self.font2)
            self.kasenNameCombo.addItem("")
            self.kasenNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.kasenNameCombo, 1, 3)
            # QGroupBox - QGridLayout - fixAmbNameLabel
            fixAmbNameLabel = QLabel(textSetting.textList["railEditor"]["railFixAmbLabel"], font=self.font2)
            modelKasenGridLayout.addWidget(fixAmbNameLabel, 2, 0)
            # QGroupBox - QGridLayout - fixAmbNameCombo
            self.fixAmbNameCombo = QComboBox(font=self.font2)
            self.fixAmbNameCombo.addItem("")
            self.fixAmbNameCombo.addItems(self.smfList)
            modelKasenGridLayout.addWidget(self.fixAmbNameCombo, 2, 1)
            # QGroupBox - QGridLayout - perNameLabel
            perNameLabel = QLabel(textSetting.textList["railEditor"]["railPer"], font=self.font2)
            modelKasenGridLayout.addWidget(perNameLabel, 2, 2)
            # QGroupBox - QGridLayout - perLabel
            self.perLabel = QLabel("", font=self.font2)
            self.perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            self.perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            modelKasenGridLayout.addWidget(self.perLabel, 2, 3)
        return horizontalLayout

    def setFlagInfoLayout(self):
        # flagInfoLayout
        flagInfoLayout = QVBoxLayout()

        flagInfoList = copy.deepcopy(textSetting.textList["railEditor"]["railFlagInfoList"])
        if self.decryptFile.game == "LSTrial":
            if self.decryptFile.oldFlag:
                return None
            flagInfoList = [flagInfoList.pop(0)]
        else:
            if self.decryptFile.game != "RS":
                flagInfoList[1][4] = textSetting.textList["railEditor"]["railOldFlag1"]
                flagInfoList[1][5] = textSetting.textList["railEditor"]["railOldFlag2"]
                flagInfoList[1][6] = textSetting.textList["railEditor"]["railOldFlag3"]
                flagInfoList[1][7] = textSetting.textList["railEditor"]["railOldFlag4"]

        # flagInfoLayout - QGroupBox
        flagGroupBox = QGroupBox(textSetting.textList["railEditor"]["railFlagInfo"])
        flagInfoLayout.addWidget(flagGroupBox)
        # flagInfoLayout - QGroupBox - flagInfoInLayout
        flagInfoInLayout = QVBoxLayout()
        flagGroupBox.setLayout(flagInfoInLayout)
        self.flagButtonGroupList = []
        for flagInfo in flagInfoList:
            # flagInfoInLayout - flagHorizontalLayout
            flagHorizontalLayout = QHBoxLayout()
            flagInfoInLayout.addLayout(flagHorizontalLayout)
            # flagInfoInLayout - flagHorizontalLayout - flagHexLabel
            flagHexLabel = QLabel("0x00 (= 0)", font=self.font2)
            flagHorizontalLayout.addWidget(flagHexLabel)
            # stretch
            flagHorizontalLayout.addStretch(1)
            # flagInfoInLayout - flagHexGridLayout
            flagHexGridLayout = QGridLayout()
            flagInfoInLayout.addLayout(flagHexGridLayout)
            flagButtonGroup = QButtonGroup()
            flagButtonGroup.setExclusive(False)
            for j, flagInfoValue in enumerate(flagInfo):
                flagCheckBox = QCheckBox(flagInfoValue)
                flagCheckBox.toggled.connect(partial(self.changeFlag, flagButtonGroup, flagHexLabel))
                flagHexGridLayout.addWidget(flagCheckBox, 0, j)
                flagButtonGroup.addButton(flagCheckBox, j)
            self.flagButtonGroupList.append(flagButtonGroup)
            # spacing
            flagInfoInLayout.addSpacing(30)
        return flagInfoLayout

    def setRailDataInfoLayout(self):
        if self.decryptFile.game == "LSTrial" and self.decryptFile.oldFlag:
            return None

        labelWidth = 66
        labelHeight = 30
        # railDataInfoLayout
        railDataInfoLayout = QVBoxLayout()
        # railDataInfoLayout - QGroupBox
        railDataGroupBox = QGroupBox(textSetting.textList["railEditor"]["railRailInfo"])
        railDataGroupBox.setFixedWidth(600)
        railDataInfoLayout.addWidget(railDataGroupBox)
        # railDataInfoLayout - QGroupBox - railDataInfoInLayout
        railDataInfoInLayout = QVBoxLayout()
        railDataGroupBox.setLayout(railDataInfoInLayout)

        # railDataCountLayout
        railDataCountLayout = QHBoxLayout()
        railDataInfoInLayout.addLayout(railDataCountLayout)
        # railDataCountLayout - railDataCountNameLabel
        railDataCountNameLabel = QLabel(textSetting.textList["railEditor"]["railRailDataCnt"], font=self.font2)
        railDataCountLayout.addWidget(railDataCountNameLabel)
        # spacing
        railDataCountLayout.addSpacing(30)
        # railDataCountLayout - railDataCountLabel
        self.railDataCountLabel = QLabel("", font=self.font2)
        self.railDataCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railDataCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDataCountLabel.setFixedSize(labelWidth, labelHeight)
        railDataCountLayout.addWidget(self.railDataCountLabel)

        if self.decryptFile.ver == "DEND_MAP_VER0300":
            # spacing
            railDataCountLayout.addSpacing(30)
            # railDataCountLayout - csvRevRailSaveButton
            csvRevRailSaveButton = QPushButton(textSetting.textList["railEditor"]["railCreateRevRail"])
            csvRevRailSaveButton.clicked.connect(self.saveRevRailCsv)
            railDataCountLayout.addWidget(csvRevRailSaveButton)
        # stretch
        railDataCountLayout.addStretch()

        # spacing
        railDataInfoInLayout.addSpacing(30)

        # nextPrevRailGridLayout
        self.nextPrevRailGridLayout = QGridLayout()
        railDataInfoInLayout.addLayout(self.nextPrevRailGridLayout)

        if self.decryptFile.ver == "DEND_MAP_VER0400":
            # spacing
            railDataInfoInLayout.addSpacing(30)

            # revNextPrevRailGridLayout
            self.revNextPrevRailGridLayout = QGridLayout()
            railDataInfoInLayout.addLayout(self.revNextPrevRailGridLayout)

        return railDataInfoLayout

    def changeFlag(self, flagButtonGroup, flagHexLabel, isChecked):
        res = 0
        for i, flagCheckBox in enumerate(flagButtonGroup.buttons()):
            if flagCheckBox.isChecked():
                res += 2**(7 - i)
        flagHexLabel.setText("0x{0:02x} (= {1})".format(res, res))

    def setRailInfo(self, gridLayout, count, railDataInfo, revFlag=False):
        while gridLayout.count():
            child = gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        labelWidth = 66
        labelHeight = 30
        nextRailName = textSetting.textList["railEditor"]["railNextRail"]
        prevRailName = textSetting.textList["railEditor"]["railPrevRail"]
        if revFlag:
            nextRailName = textSetting.textList["railEditor"]["railRevNextRail"]
            prevRailName = textSetting.textList["railEditor"]["railRevPrevRail"]

        idx = 0
        for i in range(count):
            # nextRailNameLabel
            nextRailNameLabel = QLabel(nextRailName, font=self.font2)
            gridLayout.addWidget(nextRailNameLabel, i, 0)
            # nextRailNoLabel
            nextRailNoLabel = QLabel("{0}".format(railDataInfo[idx]), font=self.font2)
            nextRailNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            nextRailNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nextRailNoLabel.setFixedSize(labelWidth, labelHeight)
            gridLayout.addWidget(nextRailNoLabel, i, 1)
            idx += 1
            # nextRailPosLabel
            nextRailPosLabel = QLabel("{0}".format(railDataInfo[idx]), font=self.font2)
            nextRailPosLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            nextRailPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nextRailPosLabel.setFixedSize(labelWidth, labelHeight)
            gridLayout.addWidget(nextRailPosLabel, i, 2)
            idx += 1
            # spacing
            gridLayout.setColumnMinimumWidth(3, 40)

            # prevRailNameLabel
            prevRailNameLabel = QLabel(prevRailName, font=self.font2)
            gridLayout.addWidget(prevRailNameLabel, i, 4)
            # prevRailNoLabel
            prevRailNoLabel = QLabel("{0}".format(railDataInfo[idx]), font=self.font2)
            prevRailNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            prevRailNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prevRailNoLabel.setFixedSize(labelWidth, labelHeight)
            gridLayout.addWidget(prevRailNoLabel, i, 5)
            idx += 1
            # prevRailPosLabel
            prevRailPosLabel = QLabel("{0}".format(railDataInfo[idx]), font=self.font2)
            prevRailPosLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            prevRailPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prevRailPosLabel.setFixedSize(labelWidth, labelHeight)
            gridLayout.addWidget(prevRailPosLabel, i, 6)
            idx += 1

    def searchRail(self):
        if not self.railNoLineEdit.hasAcceptableInput():
            return

        if len(self.railList) == 0:
            return

        railNo = int(self.railNoLineEdit.text())
        if railNo >= len(self.railList):
            railNo = len(self.railList) - 1
            self.railNoLineEdit.setText("{0}".format(railNo))
        railInfo = self.railList[railNo]

        if self.decryptFile.game in ["BS", "CS", "RS"]:
            self.prevRailLabel.setText("{0}".format(railInfo[1]))
            self.blockLabel.setText("{0}".format(railInfo[2]))
            self.railDirXLabel.setText("{0}".format(railInfo[3]))
            self.railDirYLabel.setText("{0}".format(railInfo[4]))
            self.railDirZLabel.setText("{0}".format(railInfo[5]))

            self.modelNameCombo.setCurrentIndex(railInfo[6] + 1)
            kasenNo = railInfo[7]
            if kasenNo == -1 or kasenNo == -2:
                kasenNo = len(self.smfList) + kasenNo
            kasenNo += 1
            self.kasenNameCombo.setCurrentIndex(kasenNo)
            kasenchuNo = railInfo[8]
            if kasenchuNo == -1 or kasenchuNo == -2:
                kasenchuNo = len(self.smfList) + kasenchuNo
            kasenchuNo += 1
            self.kasenchuNameCombo.setCurrentIndex(kasenchuNo)
            self.perLabel.setText("{0}".format(railInfo[9]))

            for i, flagButtonGroup in enumerate(self.flagButtonGroupList):
                railFlag = railInfo[10 + i]
                for j, flagCheckBox in enumerate(flagButtonGroup.buttons()):
                    if railFlag & (2**(7 - j)) == 0:
                        flagCheckBox.setChecked(False)
                    else:
                        flagCheckBox.setChecked(True)

            railDataCount = railInfo[14]
            self.railDataCountLabel.setText("{0}".format(railDataCount))
            railDataInfo = railInfo[15:15 + railDataCount*4]
            self.setRailInfo(self.nextPrevRailGridLayout, railDataCount, railDataInfo)

            if self.decryptFile.ver == "DEND_MAP_VER0400":
                revRailDataInfo = railInfo[15 + railDataCount*4:15 + railDataCount*4*2]
                self.setRailInfo(self.revNextPrevRailGridLayout, railDataCount, revRailDataInfo, True)
        elif self.decryptFile.game == "LS":
            railIdx = 1
            if self.decryptFile.ver == "DEND_MAP_VER0101":
                self.prevRail2Label.setText("{0}".format(railInfo[railIdx]))
                railIdx += 2

            self.railPosXLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1
            self.railPosYLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1
            self.railPosZLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1
            self.railDirXLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1
            self.railDirYLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1
            self.railDirZLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1

            self.modelNameCombo.setCurrentIndex(railInfo[railIdx] + 1)
            railIdx += 1
            prevRail = railInfo[railIdx]
            self.prevRailLabel.setText("{0}".format(prevRail))
            railIdx += 1

            if prevRail == -1:
                self.railRotXLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railRotYLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railRotZLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
            else:
                self.railRotXLabel.setText("-")
                self.railRotYLabel.setText("-")
                self.railRotZLabel.setText("-")

            kasenchuNo = railInfo[railIdx]
            if kasenchuNo == -1:
                kasenchuNo = len(self.smfList) + kasenchuNo
            kasenchuNo += 1
            self.kasenchuNameCombo.setCurrentIndex(kasenchuNo)
            railIdx += 1

            kasenNo = railInfo[railIdx]
            if kasenNo == -1:
                kasenNo = len(self.smfList) + kasenNo
            kasenNo += 1
            self.kasenNameCombo.setCurrentIndex(kasenNo)
            railIdx += 1

            fixAmbNo = railInfo[railIdx]
            if fixAmbNo == -1:
                fixAmbNo = len(self.smfList) + fixAmbNo
            fixAmbNo += 1
            self.fixAmbNameCombo.setCurrentIndex(fixAmbNo)
            railIdx += 1

            self.perLabel.setText("{0}".format(railInfo[railIdx]))
            railIdx += 1

            for i, flagButtonGroup in enumerate(self.flagButtonGroupList):
                railFlag = railInfo[railIdx]
                for j, flagCheckBox in enumerate(flagButtonGroup.buttons()):
                    if railFlag & (2**(7 - j)) == 0:
                        flagCheckBox.setChecked(False)
                    else:
                        flagCheckBox.setChecked(True)
                railIdx += 1

            railDataCount = railInfo[railIdx]
            self.railDataCountLabel.setText("{0}".format(railDataCount))
            railIdx += 1
            railDataInfo = railInfo[railIdx:railIdx + railDataCount*4]
            self.setRailInfo(self.nextPrevRailGridLayout, railDataCount, railDataInfo)
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.oldFlag:
                railIdx = 1
                #
                self.railPosXLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railPosYLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railPosZLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1

                self.nextRailLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.prevRailLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1

                self.railDirXLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railDirYLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railDirZLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1

                self.modelNameCombo.setCurrentIndex(railInfo[railIdx] + 1)
                railIdx += 1

                kasenNo = railInfo[railIdx]
                if kasenNo == -1:
                    kasenNo = len(self.smfList) + kasenNo
                kasenNo += 1
                self.kasenNameCombo.setCurrentIndex(kasenNo)
                railIdx += 1
            else:
                railIdx = 1
                #
                self.railPosXLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railPosYLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railPosZLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railDirXLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railDirYLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1
                self.railDirZLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1

                self.modelNameCombo.setCurrentIndex(railInfo[railIdx] + 1)
                railIdx += 1
                prevRail = railInfo[railIdx]
                self.prevRailLabel.setText("{0}".format(prevRail))
                railIdx += 1

                if self.decryptFile.readFlag or self.decryptFile.filenameNum == 7:
                    if prevRail == -1:
                        self.railRotXLabel.setText("{0}".format(railInfo[railIdx]))
                        railIdx += 1
                        self.railRotYLabel.setText("{0}".format(railInfo[railIdx]))
                        railIdx += 1
                        self.railRotZLabel.setText("{0}".format(railInfo[railIdx]))
                        railIdx += 1
                    else:
                        self.railRotXLabel.setText("-")
                        self.railRotYLabel.setText("-")
                        self.railRotZLabel.setText("-")

                kasenchuNo = railInfo[railIdx]
                if kasenchuNo == -1:
                    kasenchuNo = len(self.smfList) + kasenchuNo
                kasenchuNo += 1
                self.kasenchuNameCombo.setCurrentIndex(kasenchuNo)
                railIdx += 1

                kasenNo = railInfo[railIdx]
                if kasenNo == -1:
                    kasenNo = len(self.smfList) + kasenNo
                kasenNo += 1
                self.kasenNameCombo.setCurrentIndex(kasenNo)
                railIdx += 1

                fixAmbNo = railInfo[railIdx]
                if fixAmbNo == -1:
                    fixAmbNo = len(self.smfList) + fixAmbNo
                fixAmbNo += 1
                self.fixAmbNameCombo.setCurrentIndex(fixAmbNo)
                railIdx += 1

                self.perLabel.setText("{0}".format(railInfo[railIdx]))
                railIdx += 1

                for i, flagButtonGroup in enumerate(self.flagButtonGroupList):
                    railFlag = railInfo[railIdx]
                    for j, flagCheckBox in enumerate(flagButtonGroup.buttons()):
                        if railFlag & (2**(7 - j)) == 0:
                            flagCheckBox.setChecked(False)
                        else:
                            flagCheckBox.setChecked(True)
                    railIdx += 1

                railDataCount = railInfo[railIdx]
                self.railDataCountLabel.setText("{0}".format(railDataCount))
                railIdx += 1
                railDataInfo = railInfo[railIdx:railIdx + railDataCount*4]
                self.setRailInfo(self.nextPrevRailGridLayout, railDataCount, railDataInfo)

    def extractCsv(self):
        filename = self.decryptFile.filename + ".csv"
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            fileTypes
        )
        if not file_path:
            return

        try:
            self.decryptFile.extractRailCsv(file_path)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except PermissionError:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def saveCsv(self):
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["railCsvFileType"], "*.csv")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileTypes
        )
        if not file_path:
            return

        railObj, message = self.decryptFile.loadRailCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(railObj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            railList = railObj["data"]
            if not self.decryptFile.saveRailCsv(railList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I88"])
            self.reloadFunc()

    def saveRevRailCsv(self):
        filename = self.decryptFile.filename + "_rev.BIN"
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["fileType"], "*.bin")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            fileTypes
        )
        if not file_path:
            return

        revRailList = self.decryptFile.createRevRailList()
        if revRailList is None:
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
            return
        if not self.decryptFile.createRevRailFile(revRailList, file_path):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E134"])
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I89"])
        self.reloadFunc()

    def csToRs(self):
        filename = self.decryptFile.filename + "_RS.BIN"
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["railCsToRsBinType"], "*.bin")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            fileTypes
        )
        if not file_path:
            return

        newByteArr = self.decryptFile.csToRs()
        if newByteArr is None:
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E72"])
            return
        self.decryptFile.createCsToRsRailFile(newByteArr, file_path)
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I90"])
