import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox,
    QComboBox, QSizePolicy, QFileDialog
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class AmbListWidget(QWidget):
    def __init__(self, decryptFile, reloadFunc):
        super().__init__()
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.smfList.append("なし")
        self.ambList = decryptFile.ambList
        self.reloadFunc = reloadFunc
        self.font2 = QFont(textSetting.textList["font6"][0], textSetting.textList["font2"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(self.setFirstHorizontalLayout())

        if self.decryptFile.game in ["CS", "RS"]:
            mainLayout.addLayout(self.setDefaultSecondHorizontalLayout())
            mainLayout.addLayout(self.setDefaultAmbModelInfoLayout())
            # ambChildInfoLayout
            self.ambChildInfoLayout = QHBoxLayout()
            self.ambChildInfoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            mainLayout.addLayout(self.ambChildInfoLayout)
        elif self.decryptFile.game == "BS":
            mainLayout.addLayout(self.setBsSecondHorizontalLayout())
            mainLayout.addLayout(self.setBsAmbModelInfoLayout())
        elif self.decryptFile.game == "LS":
            mainLayout.addLayout(self.setLsSecondHorizontalLayout())
        elif self.decryptFile.game == "LSTrial":
            if not self.decryptFile.oldFlag:
                mainLayout.addLayout(self.setLsSecondHorizontalLayout())
            else:
                mainLayout.addLayout(self.setLsTrialOldSecondHorizontalLayout())
                mainLayout.addLayout(self.setLsTrialOldModelInfoLayout())
                # ambAddInfoLayout
                self.ambAddInfoLayout = QHBoxLayout()
                self.ambAddInfoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                mainLayout.addLayout(self.ambAddInfoLayout)

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
        # horizontalLayout - ambNoLayout
        ambNoLayout = QHBoxLayout()
        ambNoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        horizontalLayout.addLayout(ambNoLayout)
        # horizontalLayout - ambNoLayout - ambNoNameLabel
        ambNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambAmbNo"], font=self.font2)
        ambNoLayout.addWidget(ambNoNameLabel)
        # space
        ambNoLayout.addSpacing(15)
        # horizontalLayout - ambNoLayout - ambNo
        self.ambNoLineEdit = QLineEdit("0", font=self.font2)
        self.ambNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ambNoLineEdit.setFixedSize(lineEditWidth, lineEditHeight)
        self.ambNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.ambNoLineEdit.setValidator(integerValidator)
        ambNoLayout.addWidget(self.ambNoLineEdit)
        # space
        ambNoLayout.addSpacing(30)
        # horizontalLayout - ambNoLayout - searchAmbButton
        searchAmbButton = QPushButton(textSetting.textList["railEditor"]["ambSearchBtnLabel"])
        searchAmbButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        searchAmbButton.clicked.connect(self.searchAmb)
        ambNoLayout.addWidget(searchAmbButton)

        # space
        horizontalLayout.addSpacing(60)
        # horizontalLayout - csvButtonLayout
        csvButtonLayout = QHBoxLayout()
        horizontalLayout.addLayout(csvButtonLayout)
        # horizontalLayout - csvButtonLayout - csvExtractButton
        csvExtractButton = QPushButton(textSetting.textList["railEditor"]["ambCsvExtractLabel"])
        csvExtractButton.setFixedSize(buttonWidth, buttonHeight)
        csvExtractButton.clicked.connect(self.extractCsv)
        csvButtonLayout.addWidget(csvExtractButton)
        # space
        csvButtonLayout.addSpacing(20)
        # horizontalLayout - csvButtonLayout - csvSaveButton
        csvSaveButton = QPushButton(textSetting.textList["railEditor"]["ambCsvSaveLabel"])
        csvSaveButton.setFixedSize(buttonWidth, buttonHeight)
        csvSaveButton.clicked.connect(self.saveCsv)
        csvButtonLayout.addWidget(csvSaveButton)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setDefaultSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambInfoLabel"])
        horizontalLayout.addWidget(ambInfoGroupBox)
        # QGroupBox - QGridLayout
        ambInfoGridLayout = QGridLayout()
        ambInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambInfoGridLayout.setVerticalSpacing(20)
        ambInfoGroupBox.setLayout(ambInfoGridLayout)
        # typeNameLabel
        typeNameLabel = QLabel(textSetting.textList["railEditor"]["ambType"], font=self.font2)
        ambInfoGridLayout.addWidget(typeNameLabel, 0, 0)
        # typeLabel
        self.typeLabel = QLabel("", font=self.font2)
        self.typeLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.typeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.typeLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.typeLabel, 0, 1)
        # lengthNameLabel
        lengthNameLabel = QLabel(textSetting.textList["railEditor"]["ambLength"], font=self.font2)
        ambInfoGridLayout.addWidget(lengthNameLabel, 1, 0)
        # lengthLabel
        self.lengthLabel = QLabel("", font=self.font2)
        self.lengthLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.lengthLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lengthLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.lengthLabel, 1, 1)
        # railNoNameLabel
        railNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambRailNo"], font=self.font2)
        ambInfoGridLayout.addWidget(railNoNameLabel, 2, 0)
        # railNoLabel
        self.railNoLabel = QLabel("", font=self.font2)
        self.railNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railNoLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.railNoLabel, 2, 1)
        # railPosNameLabel
        railPosNameLabel = QLabel(textSetting.textList["railEditor"]["ambRailPos"], font=self.font2)
        ambInfoGridLayout.addWidget(railPosNameLabel, 3, 0)
        # railPosLabel
        self.railPosLabel = QLabel("", font=self.font2)
        self.railPosLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.railPosLabel, 3, 1)

        # QGroupBox
        ambXyzGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambPosDirInfo"])
        horizontalLayout.addWidget(ambXyzGroupBox)
        # QGroupBox - QGridLayout
        ambXyzGridLayout = QGridLayout()
        ambXyzGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambXyzGridLayout.setVerticalSpacing(20)
        ambXyzGroupBox.setLayout(ambXyzGridLayout)
        # ambBasePosXNameLabel
        ambBasePosXNameLabel = QLabel(textSetting.textList["railEditor"]["ambBasePosX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBasePosXNameLabel, 0, 0)
        # ambBasePosXLabel
        self.ambBasePosXLabel = QLabel("", font=self.font2)
        self.ambBasePosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBasePosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBasePosXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBasePosXLabel, 0, 1)
        # ambBasePosYNameLabel
        ambBasePosYNameLabel = QLabel(textSetting.textList["railEditor"]["ambBasePosY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBasePosYNameLabel, 1, 0)
        # ambBasePosYLabel
        self.ambBasePosYLabel = QLabel("", font=self.font2)
        self.ambBasePosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBasePosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBasePosYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBasePosYLabel, 1, 1)
        # ambBasePosZNameLabel
        ambBasePosZNameLabel = QLabel(textSetting.textList["railEditor"]["ambBasePosZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBasePosZNameLabel, 2, 0)
        # ambBasePosZLabel
        self.ambBasePosZLabel = QLabel("", font=self.font2)
        self.ambBasePosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBasePosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBasePosZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBasePosZLabel, 2, 1)
        # ambBaseRotXNameLabel
        ambBaseRotXNameLabel = QLabel(textSetting.textList["railEditor"]["ambBaseDirX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBaseRotXNameLabel, 0, 2)
        # ambBaseRotXLabel
        self.ambBaseRotXLabel = QLabel("", font=self.font2)
        self.ambBaseRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBaseRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBaseRotXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBaseRotXLabel, 0, 3)
        # ambBaseRotYNameLabel
        ambBaseRotYNameLabel = QLabel(textSetting.textList["railEditor"]["ambBaseDirY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBaseRotYNameLabel, 1, 2)
        # ambBaseRotYLabel
        self.ambBaseRotYLabel = QLabel("", font=self.font2)
        self.ambBaseRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBaseRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBaseRotYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBaseRotYLabel, 1, 3)
        # ambBaseRotZNameLabel
        ambBaseRotZNameLabel = QLabel(textSetting.textList["railEditor"]["ambBaseDirZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambBaseRotZNameLabel, 2, 2)
        # ambBaseRotZLabel
        self.ambBaseRotZLabel = QLabel("", font=self.font2)
        self.ambBaseRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambBaseRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambBaseRotZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambBaseRotZLabel, 2, 3)

        # QGroupBox
        ambInfo2GroupBox = QGroupBox(textSetting.textList["railEditor"]["ambInfo2Label"])
        horizontalLayout.addWidget(ambInfo2GroupBox)
        # QGroupBox - QGridLayout
        ambInfo2GridLayout = QGridLayout()
        ambInfo2GridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambInfo2GridLayout.setVerticalSpacing(20)
        ambInfo2GroupBox.setLayout(ambInfo2GridLayout)
        # priorityNameLabel
        priorityNameLabel = QLabel(textSetting.textList["railEditor"]["ambPriority"], font=self.font2)
        ambInfo2GridLayout.addWidget(priorityNameLabel, 0, 0)
        # priorityLabel
        self.priorityLabel = QLabel("", font=self.font2)
        self.priorityLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.priorityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priorityLabel.setFixedSize(labelWidth, labelHeight)
        ambInfo2GridLayout.addWidget(self.priorityLabel, 0, 1)
        # fogNameLabel
        fogNameLabel = QLabel(textSetting.textList["railEditor"]["ambFog"], font=self.font2)
        ambInfo2GridLayout.addWidget(fogNameLabel, 1, 0)
        # fogLabel
        self.fogLabel = QLabel("", font=self.font2)
        self.fogLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fogLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fogLabel.setFixedSize(labelWidth, labelHeight)
        ambInfo2GridLayout.addWidget(self.fogLabel, 1, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setDefaultAmbModelInfoLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambModelInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambModelInfo"])
        horizontalLayout.addWidget(ambModelInfoGroupBox)
        # QGroupBox - ambModelInfoInLayout
        ambModelInfoInLayout = QVBoxLayout()
        ambModelInfoGroupBox.setLayout(ambModelInfoInLayout)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambModelInfoGridLayout = QGridLayout()
        ambModelInfoGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambModelInfoGridLayout)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelSmf"], font=self.font2)
        ambModelInfoGridLayout.addWidget(modelNameLabel, 0, 0)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameCombo
        self.modelNameCombo = QComboBox(font=self.font2)
        self.modelNameCombo.addItem("")
        self.modelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.modelNameCombo, 0, 1)

        # spacing
        ambModelInfoInLayout.addSpacing(20)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambXyzGridLayout = QGridLayout()
        ambXyzGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambXyzGridLayout)
        # ambPosXNameLabel
        ambPosXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosXNameLabel, 0, 0)
        # ambPosXLabel
        self.ambPosXLabel = QLabel("", font=self.font2)
        self.ambPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosXLabel, 0, 1)
        # ambPosYNameLabel
        ambPosYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosYNameLabel, 0, 2)
        # ambPosYLabel
        self.ambPosYLabel = QLabel("", font=self.font2)
        self.ambPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosYLabel, 0, 3)
        # ambPosZNameLabel
        ambPosZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosZNameLabel, 0, 4)
        # ambPosZLabel
        self.ambPosZLabel = QLabel("", font=self.font2)
        self.ambPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosZLabel, 0, 5)

        # ambDirXNameLabel
        ambDirXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirXNameLabel, 1, 0)
        # ambDirXLabel
        self.ambDirXLabel = QLabel("", font=self.font2)
        self.ambDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirXLabel, 1, 1)
        # ambDirYNameLabel
        ambDirYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirYNameLabel, 1, 2)
        # ambDirYLabel
        self.ambDirYLabel = QLabel("", font=self.font2)
        self.ambDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirYLabel, 1, 3)
        # ambDirZNameLabel
        ambDirZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirZNameLabel, 1, 4)
        # ambDirZLabel
        self.ambDirZLabel = QLabel("", font=self.font2)
        self.ambDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirZLabel, 1, 5)

        # ambRotXNameLabel
        ambRotXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotXNameLabel, 2, 0)
        # ambRotXLabel
        self.ambRotXLabel = QLabel("", font=self.font2)
        self.ambRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotXLabel, 2, 1)
        # ambRotYNameLabel
        ambRotYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotYNameLabel, 2, 2)
        # ambRotYLabel
        self.ambRotYLabel = QLabel("", font=self.font2)
        self.ambRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotYLabel, 2, 3)
        # ambRotZNameLabel
        ambRotZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotZNameLabel, 2, 4)
        # ambRotZLabel
        self.ambRotZLabel = QLabel("", font=self.font2)
        self.ambRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotZLabel, 2, 5)

        # perNameLabel
        perNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPer"], font=self.font2)
        ambXyzGridLayout.addWidget(perNameLabel, 3, 0)
        # perLabel
        self.perLabel = QLabel("", font=self.font2)
        self.perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambXyzGridLayout.addWidget(self.perLabel, 3, 1)

        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setDefaultAmbChildModelInfoLayout(self, childCount, ambChildInfo):
        item = self.ambChildInfoLayout.takeAt(0)
        if item is not None and item.widget():
            item.widget().deleteLater()

        if childCount == 0:
            return

        newGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambChildModelInfo"])
        newGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ambChildInfoLayout.addWidget(newGroupBox)
        ambChildInfoInLayout = QVBoxLayout()
        newGroupBox.setLayout(ambChildInfoInLayout)
        ambSize = 11
        ambChunkList = [ambChildInfo[i:i + ambSize] for i in range(0, len(ambChildInfo), ambSize)]
        for i, ambChunkInfo in enumerate(ambChunkList):
            self.setDefaultAmbChildModel(ambChildInfoInLayout, i, ambChunkInfo)
            if i != len(ambChunkList) - 1:
                horizentalLine = QFrame()
                horizentalLine.setFrameShape(QFrame.Shape.HLine)
                horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
                ambChildInfoInLayout.addWidget(horizentalLine)

    def setDefaultAmbChildModel(self, layout, index, ambInfo):
        labelWidth = 66
        labelHeight = 30

        ambModelInfoInLayout = QVBoxLayout()
        layout.addLayout(ambModelInfoInLayout)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambModelInfoGridLayout = QGridLayout()
        ambModelInfoGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambModelInfoGridLayout)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["ambChildModelSmf"].format(index), font=self.font2)
        ambModelInfoGridLayout.addWidget(modelNameLabel, 0, 0)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameCombo
        modelNameCombo = QComboBox(font=self.font2)
        modelNameCombo.addItem("")
        modelNameCombo.addItems(self.smfList)
        modelNameCombo.setCurrentIndex(ambInfo[0] + 1)
        ambModelInfoGridLayout.addWidget(modelNameCombo, 0, 1)

        # spacing
        ambModelInfoInLayout.addSpacing(20)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambXyzGridLayout = QGridLayout()
        ambXyzGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambXyzGridLayout)
        # ambPosXNameLabel
        ambPosXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosXNameLabel, 0, 0)
        # ambPosXLabel
        ambPosXLabel = QLabel("{0}".format(ambInfo[1]), font=self.font2)
        ambPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambPosXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambPosXLabel, 0, 1)
        # ambPosYNameLabel
        ambPosYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosYNameLabel, 0, 2)
        # ambPosYLabel
        ambPosYLabel = QLabel("{0}".format(ambInfo[2]), font=self.font2)
        ambPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambPosYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambPosYLabel, 0, 3)
        # ambPosZNameLabel
        ambPosZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosZNameLabel, 0, 4)
        # ambPosZLabel
        ambPosZLabel = QLabel("{0}".format(ambInfo[3]), font=self.font2)
        ambPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambPosZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambPosZLabel, 0, 5)

        # ambDirXNameLabel
        ambDirXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirXNameLabel, 1, 0)
        # ambDirXLabel
        ambDirXLabel = QLabel("{0}".format(ambInfo[4]), font=self.font2)
        ambDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambDirXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambDirXLabel, 1, 1)
        # ambDirYNameLabel
        ambDirYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirYNameLabel, 1, 2)
        # ambDirYLabel
        ambDirYLabel = QLabel("{0}".format(ambInfo[5]), font=self.font2)
        ambDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambDirYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambDirYLabel, 1, 3)
        # ambDirZNameLabel
        ambDirZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelDirZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirZNameLabel, 1, 4)
        # ambDirZLabel
        ambDirZLabel = QLabel("{0}".format(ambInfo[6]), font=self.font2)
        ambDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambDirZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambDirZLabel, 1, 5)

        # ambRotXNameLabel
        ambRotXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotXNameLabel, 2, 0)
        # ambRotXLabel
        ambRotXLabel = QLabel("{0}".format(ambInfo[7]), font=self.font2)
        ambRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambRotXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambRotXLabel, 2, 1)
        # ambRotYNameLabel
        ambRotYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotYNameLabel, 2, 2)
        # ambRotYLabel
        ambRotYLabel = QLabel("{0}".format(ambInfo[8]), font=self.font2)
        ambRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambRotYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambRotYLabel, 2, 3)
        # ambRotZNameLabel
        ambRotZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotZNameLabel, 2, 4)
        # ambRotZLabel
        ambRotZLabel = QLabel("{0}".format(ambInfo[9]), font=self.font2)
        ambRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        ambRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambRotZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(ambRotZLabel, 2, 5)

        # perNameLabel
        perNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPer"], font=self.font2)
        ambXyzGridLayout.addWidget(perNameLabel, 3, 0)
        # perLabel
        perLabel = QLabel("{0}".format(ambInfo[10]), font=self.font2)
        perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambXyzGridLayout.addWidget(perLabel, 3, 1)

    def setBsSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambInfoLabel"])
        horizontalLayout.addWidget(ambInfoGroupBox)
        # QGroupBox - QGridLayout
        ambInfoGridLayout = QGridLayout()
        ambInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambInfoGridLayout.setVerticalSpacing(20)
        ambInfoGroupBox.setLayout(ambInfoGridLayout)
        # railNoNameLabel
        railNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambRailNo"], font=self.font2)
        ambInfoGridLayout.addWidget(railNoNameLabel, 0, 0)
        # railNoLabel
        self.railNoLabel = QLabel("", font=self.font2)
        self.railNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railNoLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.railNoLabel, 0, 1)
        # priorityNameLabel
        priorityNameLabel = QLabel(textSetting.textList["railEditor"]["ambPriority"], font=self.font2)
        ambInfoGridLayout.addWidget(priorityNameLabel, 1, 0)
        # priorityLabel
        self.priorityLabel = QLabel("", font=self.font2)
        self.priorityLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.priorityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priorityLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.priorityLabel, 1, 1)
        # fogNameLabel
        fogNameLabel = QLabel(textSetting.textList["railEditor"]["ambFog"], font=self.font2)
        ambInfoGridLayout.addWidget(fogNameLabel, 2, 0)
        # fogLabel
        self.fogLabel = QLabel("", font=self.font2)
        self.fogLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fogLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fogLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.fogLabel, 2, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setBsAmbModelInfoLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambModelInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambModelInfo"])
        horizontalLayout.addWidget(ambModelInfoGroupBox)
        # QGroupBox - ambModelInfoInLayout
        ambModelInfoInLayout = QVBoxLayout()
        ambModelInfoGroupBox.setLayout(ambModelInfoInLayout)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambModelInfoGridLayout = QGridLayout()
        ambModelInfoGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambModelInfoGridLayout)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelBsSmf"], font=self.font2)
        ambModelInfoGridLayout.addWidget(modelNameLabel, 0, 0)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelNameCombo
        self.modelNameCombo = QComboBox(font=self.font2)
        self.modelNameCombo.addItem("")
        self.modelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.modelNameCombo, 0, 1)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelDetailNoNameLabel
        modelDetailNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelBsDetail"], font=self.font2)
        ambModelInfoGridLayout.addWidget(modelDetailNoNameLabel, 1, 0)
        # QGroupBox - ambModelInfoInLayout - QGridLayout - modelDetailNoLabel
        self.modelDetailNoLabel = QLabel("", font=self.font2)
        self.modelDetailNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.modelDetailNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambModelInfoGridLayout.addWidget(self.modelDetailNoLabel, 1, 1)

        # spacing
        ambModelInfoInLayout.addSpacing(20)

        # QGroupBox - ambModelInfoInLayout - QGridLayout
        ambXyzGridLayout = QGridLayout()
        ambXyzGridLayout.setVerticalSpacing(20)
        ambModelInfoInLayout.addLayout(ambXyzGridLayout)
        # ambPosXNameLabel
        ambPosXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosXNameLabel, 0, 0)
        # ambPosXLabel
        self.ambPosXLabel = QLabel("", font=self.font2)
        self.ambPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosXLabel, 0, 1)
        # ambPosYNameLabel
        ambPosYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosYNameLabel, 0, 2)
        # ambPosYLabel
        self.ambPosYLabel = QLabel("", font=self.font2)
        self.ambPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosYLabel, 0, 3)
        # ambPosZNameLabel
        ambPosZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPosZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosZNameLabel, 0, 4)
        # ambPosZLabel
        self.ambPosZLabel = QLabel("", font=self.font2)
        self.ambPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosZLabel, 0, 5)

        # ambRotXNameLabel
        ambRotXNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotXNameLabel, 1, 0)
        # ambRotXLabel
        self.ambRotXLabel = QLabel("", font=self.font2)
        self.ambRotXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotXLabel, 1, 1)
        # ambRotYNameLabel
        ambRotYNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotYNameLabel, 1, 2)
        # ambRotYLabel
        self.ambRotYLabel = QLabel("", font=self.font2)
        self.ambRotYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotYLabel, 1, 3)
        # ambRotZNameLabel
        ambRotZNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelRotZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambRotZNameLabel, 1, 4)
        # ambRotZLabel
        self.ambRotZLabel = QLabel("", font=self.font2)
        self.ambRotZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambRotZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambRotZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambRotZLabel, 1, 5)

        # perNameLabel
        perNameLabel = QLabel(textSetting.textList["railEditor"]["ambModelPer"], font=self.font2)
        ambXyzGridLayout.addWidget(perNameLabel, 2, 0)
        # perLabel
        self.perLabel = QLabel("", font=self.font2)
        self.perLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.perLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambXyzGridLayout.addWidget(self.perLabel, 2, 1)

        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambInfoLabel"])
        horizontalLayout.addWidget(ambInfoGroupBox)
        # QGroupBox - QGridLayout
        ambInfoGridLayout = QGridLayout()
        ambInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambInfoGridLayout.setVerticalSpacing(20)
        ambInfoGroupBox.setLayout(ambInfoGridLayout)
        # railNoNameLabel
        railNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambRailNo"], font=self.font2)
        ambInfoGridLayout.addWidget(railNoNameLabel, 0, 0)
        # railNoLabel
        self.railNoLabel = QLabel("", font=self.font2)
        self.railNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railNoLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.railNoLabel, 0, 1)
        # posNameLabel
        posNameLabel = QLabel(textSetting.textList["railEditor"]["ambLsPos"], font=self.font2)
        ambInfoGridLayout.addWidget(posNameLabel, 1, 0)
        # posLabel
        self.posLabel = QLabel("", font=self.font2)
        self.posLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.posLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.posLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.posLabel, 1, 1)
        # railPosNameLabel
        railPosNameLabel = QLabel(textSetting.textList["railEditor"]["ambRailPos"], font=self.font2)
        ambInfoGridLayout.addWidget(railPosNameLabel, 0, 2)
        # railPosLabel
        self.railPosLabel = QLabel("", font=self.font2)
        self.railPosLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.railPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPosLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.railPosLabel, 0, 3)
        # modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["railEditor"]["ambLsModel"], font=self.font2)
        ambInfoGridLayout.addWidget(modelNameLabel, 2, 0)
        # modelNameCombo
        self.modelNameCombo = QComboBox(font=self.font2)
        self.modelNameCombo.addItem("-")
        self.modelNameCombo.addItems(self.smfList)
        ambInfoGridLayout.addWidget(self.modelNameCombo, 2, 1, 1, 3)
        # animeNoNameLabel
        animeNoNameLabel = QLabel(textSetting.textList["railEditor"]["ambLsAnime"], font=self.font2)
        ambInfoGridLayout.addWidget(animeNoNameLabel, 1, 2)
        # animeNoLabel
        self.animeNoLabel = QLabel("", font=self.font2)
        self.animeNoLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.animeNoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animeNoLabel.setFixedSize(labelWidth, labelHeight)
        ambInfoGridLayout.addWidget(self.animeNoLabel, 1, 3)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsTrialOldSecondHorizontalLayout(self):
        labelWidth = 66
        labelHeight = 30
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambXyzGroupBox = QGroupBox(textSetting.textList["railEditor"]["railPosXyzInfo"])
        horizontalLayout.addWidget(ambXyzGroupBox)
        # QGroupBox - QGridLayout
        ambXyzGridLayout = QGridLayout()
        ambXyzGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambXyzGridLayout.setVerticalSpacing(20)
        ambXyzGroupBox.setLayout(ambXyzGridLayout)
        # ambPosXNameLabel
        ambPosXNameLabel = QLabel(textSetting.textList["railEditor"]["railPosX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosXNameLabel, 0, 0)
        # ambPosXLabel
        self.ambPosXLabel = QLabel("", font=self.font2)
        self.ambPosXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosXLabel, 0, 1)
        # ambPosYNameLabel
        ambPosYNameLabel = QLabel(textSetting.textList["railEditor"]["railPosY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosYNameLabel, 1, 0)
        # ambPosYLabel
        self.ambPosYLabel = QLabel("", font=self.font2)
        self.ambPosYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosYLabel, 1, 1)
        # ambPosZNameLabel
        ambPosZNameLabel = QLabel(textSetting.textList["railEditor"]["railPosZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambPosZNameLabel, 2, 0)
        # ambPosZLabel
        self.ambPosZLabel = QLabel("", font=self.font2)
        self.ambPosZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPosZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPosZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambPosZLabel, 2, 1)
        # ambDirXNameLabel
        ambDirXNameLabel = QLabel(textSetting.textList["railEditor"]["railDirX"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirXNameLabel, 0, 2)
        # ambDirXLabel
        self.ambDirXLabel = QLabel("", font=self.font2)
        self.ambDirXLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirXLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirXLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirXLabel, 0, 3)
        # ambDirYNameLabel
        ambDirYNameLabel = QLabel(textSetting.textList["railEditor"]["railDirY"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirYNameLabel, 1, 2)
        # ambDirYLabel
        self.ambDirYLabel = QLabel("", font=self.font2)
        self.ambDirYLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirYLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirYLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirYLabel, 1, 3)
        # ambDirZNameLabel
        ambDirZNameLabel = QLabel(textSetting.textList["railEditor"]["railDirZ"], font=self.font2)
        ambXyzGridLayout.addWidget(ambDirZNameLabel, 2, 2)
        # ambDirZLabel
        self.ambDirZLabel = QLabel("", font=self.font2)
        self.ambDirZLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambDirZLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambDirZLabel.setFixedSize(labelWidth, labelHeight)
        ambXyzGridLayout.addWidget(self.ambDirZLabel, 2, 3)

        # QGroupBox
        ambInfo2GroupBox = QGroupBox(textSetting.textList["railEditor"]["railRailInfo"])
        horizontalLayout.addWidget(ambInfo2GroupBox)
        # QGroupBox - QGridLayout
        ambInfo2GridLayout = QGridLayout()
        ambInfo2GridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambInfo2GridLayout.setVerticalSpacing(20)
        ambInfo2GroupBox.setLayout(ambInfo2GridLayout)
        # QGroupBox - QGridLayout - ambNextNameLabel
        ambNextNameLabel = QLabel(textSetting.textList["railEditor"]["railNextRail"], font=self.font2)
        ambInfo2GridLayout.addWidget(ambNextNameLabel, 0, 0)
        # QGroupBox - QGridLayout - ambNextLabel
        self.ambNextLabel = QLabel("", font=self.font2)
        self.ambNextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambNextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambNextLabel.setFixedSize(labelWidth, labelHeight)
        ambInfo2GridLayout.addWidget(self.ambNextLabel, 0, 1)
        # QGroupBox - QGridLayout - ambPrevNameLabel
        ambPrevNameLabel = QLabel(textSetting.textList["railEditor"]["railPrevRail"], font=self.font2)
        ambInfo2GridLayout.addWidget(ambPrevNameLabel, 1, 0)
        # QGroupBox - QGridLayout - ambPrevLabel
        self.ambPrevLabel = QLabel("", font=self.font2)
        self.ambPrevLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.ambPrevLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambPrevLabel.setFixedSize(labelWidth, labelHeight)
        ambInfo2GridLayout.addWidget(self.ambPrevLabel, 1, 1)
        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setLsTrialOldModelInfoLayout(self):
        # horizontalLayout
        horizontalLayout = QHBoxLayout()

        # QGroupBox
        ambModelInfoGroupBox = QGroupBox(textSetting.textList["railEditor"]["railModelKasenInfo"])
        horizontalLayout.addWidget(ambModelInfoGroupBox)
        # QGroupBox - QGridLayout
        ambModelInfoGridLayout = QGridLayout()
        ambModelInfoGridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ambModelInfoGridLayout.setVerticalSpacing(20)
        ambModelInfoGroupBox.setLayout(ambModelInfoGridLayout)
        # leftAmbModelNameLabel
        leftAmbModelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
        ambModelInfoGridLayout.addWidget(leftAmbModelNameLabel, 0, 0)
        # leftAmbModelNameCombo
        self.leftAmbModelNameCombo = QComboBox(font=self.font2)
        self.leftAmbModelNameCombo.addItem("")
        self.leftAmbModelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.leftAmbModelNameCombo, 0, 1)
        # rightAmbModelNameLabel
        rightAmbModelNameLabel = QLabel(textSetting.textList["railEditor"]["railModelLabel"], font=self.font2)
        ambModelInfoGridLayout.addWidget(rightAmbModelNameLabel, 1, 0)
        # rightAmbModelNameCombo
        self.rightAmbModelNameCombo = QComboBox(font=self.font2)
        self.rightAmbModelNameCombo.addItem("")
        self.rightAmbModelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.rightAmbModelNameCombo, 1, 1)
        # kasenchuModelNameLabel
        kasenchuModelNameLabel = QLabel(textSetting.textList["railEditor"]["railKasenchuLabel"], font=self.font2)
        ambModelInfoGridLayout.addWidget(kasenchuModelNameLabel, 0, 2)
        # kasenchuModelNameCombo
        self.kasenchuModelNameCombo = QComboBox(font=self.font2)
        self.kasenchuModelNameCombo.addItem("")
        self.kasenchuModelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.kasenchuModelNameCombo, 0, 3)
        # fixAmbModelNameLabel
        fixAmbModelNameLabel = QLabel(textSetting.textList["railEditor"]["railFixAmbLabel"], font=self.font2)
        ambModelInfoGridLayout.addWidget(fixAmbModelNameLabel, 1, 2)
        # fixAmbModelNameCombo
        self.fixAmbModelNameCombo = QComboBox(font=self.font2)
        self.fixAmbModelNameCombo.addItem("")
        self.fixAmbModelNameCombo.addItems(self.smfList)
        ambModelInfoGridLayout.addWidget(self.fixAmbModelNameCombo, 1, 3)

        # horizontalLayout - stretch
        horizontalLayout.addStretch(1)
        return horizontalLayout

    def setAmbAddInfo(self, ambAddInfoList):
        item = self.ambAddInfoLayout.takeAt(0)
        if item is not None and item.widget():
            item.widget().deleteLater()

        if len(ambAddInfoList) == 0:
            return

        labelWidth = 66
        labelHeight = 30
        newGroupBox = QGroupBox(textSetting.textList["railEditor"]["ambInfo2Label"])
        newGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ambAddInfoLayout.addWidget(newGroupBox)
        ambAddInfoInLayout = QVBoxLayout()
        newGroupBox.setLayout(ambAddInfoInLayout)
        for ambAddInfo in ambAddInfoList:
            ambAddInfoHorizontalLayout = QHBoxLayout()
            ambAddInfoHorizontalLayout.setContentsMargins(5, 10, 5, 10)
            ambAddInfoInLayout.addLayout(ambAddInfoHorizontalLayout)
            for ambAddValue in ambAddInfo:
                ambAddLabel = QLabel("{0}".format(ambAddValue), font=self.font2)
                ambAddLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                ambAddLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ambAddLabel.setFixedSize(labelWidth, labelHeight)
                ambAddInfoHorizontalLayout.addWidget(ambAddLabel)

    def searchAmb(self):
        if not self.ambNoLineEdit.hasAcceptableInput():
            return

        if len(self.ambList) == 0:
            return

        ambNo = int(self.ambNoLineEdit.text())
        if ambNo >= len(self.ambList):
            ambNo = len(self.ambList) - 1
            self.ambNoLineEdit.setText("{0}".format(ambNo))
        ambInfo = self.ambList[ambNo]

        if self.decryptFile.game in ["CS", "RS"]:
            self.typeLabel.setText("{0}".format(ambInfo[0]))
            self.lengthLabel.setText("{0}".format(ambInfo[1]))
            self.railNoLabel.setText("{0}".format(ambInfo[2]))
            self.railPosLabel.setText("{0}".format(ambInfo[3]))
            self.ambBasePosXLabel.setText("{0}".format(ambInfo[4]))
            self.ambBasePosYLabel.setText("{0}".format(ambInfo[5]))
            self.ambBasePosZLabel.setText("{0}".format(ambInfo[6]))
            self.ambBaseRotXLabel.setText("{0}".format(ambInfo[7]))
            self.ambBaseRotYLabel.setText("{0}".format(ambInfo[8]))
            self.ambBaseRotZLabel.setText("{0}".format(ambInfo[9]))
            self.priorityLabel.setText("{0}".format(ambInfo[10]))
            self.fogLabel.setText("{0}".format(ambInfo[11]))

            self.modelNameCombo.setCurrentIndex(ambInfo[12] + 1)
            self.ambPosXLabel.setText("{0}".format(ambInfo[13]))
            self.ambPosYLabel.setText("{0}".format(ambInfo[14]))
            self.ambPosZLabel.setText("{0}".format(ambInfo[15]))
            self.ambDirXLabel.setText("{0}".format(ambInfo[16]))
            self.ambDirYLabel.setText("{0}".format(ambInfo[17]))
            self.ambDirZLabel.setText("{0}".format(ambInfo[18]))
            self.ambRotXLabel.setText("{0}".format(ambInfo[19]))
            self.ambRotYLabel.setText("{0}".format(ambInfo[20]))
            self.ambRotZLabel.setText("{0}".format(ambInfo[21]))
            self.perLabel.setText("{0}".format(ambInfo[22]))

            childCount = ambInfo[23]
            self.setDefaultAmbChildModelInfoLayout(childCount, ambInfo[24:])
        elif self.decryptFile.game == "BS":
            self.railNoLabel.setText("{0}".format(ambInfo[0]))
            self.priorityLabel.setText("{0}".format(ambInfo[1]))
            self.fogLabel.setText("{0}".format(ambInfo[2]))
            self.modelNameCombo.setCurrentIndex(ambInfo[3] + 1)
            self.modelDetailNoLabel.setText("{0}".format(ambInfo[4]))
            self.ambPosXLabel.setText("{0}".format(ambInfo[5]))
            self.ambPosYLabel.setText("{0}".format(ambInfo[6]))
            self.ambPosZLabel.setText("{0}".format(ambInfo[7]))
            self.ambRotXLabel.setText("{0}".format(ambInfo[8]))
            self.ambRotYLabel.setText("{0}".format(ambInfo[9]))
            self.ambRotZLabel.setText("{0}".format(ambInfo[10]))
            self.perLabel.setText("{0}".format(ambInfo[11]))
        elif self.decryptFile.game == "LS":
            self.railNoLabel.setText("{0}".format(ambInfo[0]))
            self.posLabel.setText("{0}".format(ambInfo[1]))
            self.railPosLabel.setText("{0}".format(ambInfo[2]))
            modelNo = ambInfo[3]
            if modelNo != 0:
                modelNo += 1
            self.modelNameCombo.setCurrentIndex(modelNo)
            self.animeNoLabel.setText("{0}".format(ambInfo[4]))
        elif self.decryptFile.game == "LSTrial":
            if self.decryptFile.oldFlag:
                self.ambPosXLabel.setText("{0}".format(ambInfo[0]))
                self.ambPosYLabel.setText("{0}".format(ambInfo[1]))
                self.ambPosZLabel.setText("{0}".format(ambInfo[2]))
                self.ambNextLabel.setText("{0}".format(ambInfo[3]))
                self.ambPrevLabel.setText("{0}".format(ambInfo[4]))
                self.ambDirXLabel.setText("{0}".format(ambInfo[5]))
                self.ambDirYLabel.setText("{0}".format(ambInfo[6]))
                self.ambDirZLabel.setText("{0}".format(ambInfo[7]))
                leftAmbModelNo = ambInfo[8]
                if leftAmbModelNo == -1:
                    leftAmbModelNo = len(self.smfList) + leftAmbModelNo
                leftAmbModelNo += 1
                self.leftAmbModelNameCombo.setCurrentIndex(leftAmbModelNo)

                rightAmbModelNo = ambInfo[9]
                if rightAmbModelNo == -1:
                    rightAmbModelNo = len(self.smfList) + rightAmbModelNo
                rightAmbModelNo += 1
                self.rightAmbModelNameCombo.setCurrentIndex(rightAmbModelNo)

                kasenchuNo = ambInfo[10]
                if kasenchuNo == -1:
                    kasenchuNo = len(self.smfList) + kasenchuNo
                kasenchuNo += 1
                self.kasenchuModelNameCombo.setCurrentIndex(kasenchuNo)

                fixAmbNo = ambInfo[11]
                if fixAmbNo == -1:
                    fixAmbNo = len(self.smfList) + fixAmbNo
                fixAmbNo += 1
                self.fixAmbModelNameCombo.setCurrentIndex(fixAmbNo)
                self.setAmbAddInfo(ambInfo[-1])
            else:
                self.railNoLabel.setText("{0}".format(ambInfo[0]))
                self.posLabel.setText("{0}".format(ambInfo[1]))
                self.railPosLabel.setText("{0}".format(ambInfo[2]))
                modelNo = ambInfo[3]
                if modelNo != 0:
                    modelNo += 1
                self.modelNameCombo.setCurrentIndex(modelNo)
                self.animeNoLabel.setText("{0}".format(ambInfo[4]))

    def extractCsv(self):
        filename = self.decryptFile.filename + "_amb.csv"
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "",
            filename,
            fileTypes
        )
        if not file_path:
            return

        try:
            self.decryptFile.extractAmbCsv(file_path)
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        except PermissionError:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E7"])

    def saveCsv(self):
        fileTypes = "{0} ({1})".format(textSetting.textList["railEditor"]["ambCsvFileType"], "*.csv")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileTypes
        )

        if not file_path:
            return

        ambObj, message = self.decryptFile.loadAmbCsv(file_path)
        if message:
            mb.showerror(title=textSetting.textList["error"], message=message)
            return

        msg = textSetting.textList["infoList"]["I15"].format(ambObj["csvLines"])
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            ambList = ambObj["data"]
            if not self.decryptFile.saveAmbCsv(ambList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I95"])
            self.reloadFunc()
