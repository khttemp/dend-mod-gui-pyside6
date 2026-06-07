import os
import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from program.sub.rsRail.getMemory.getMemory import GetMemory

from PySide6.QtWidgets import (
    QWidget, QLabel, QScrollArea, QFrame, QVBoxLayout,
    QHBoxLayout, QGroupBox, QGridLayout, QStackedWidget,
    QPushButton, QLineEdit, QFileDialog
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, QTimer

mb = customMessageBoxWidget.CustomMessageBox()


class RsRailWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.memoryObj = None

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])

        mainLayout = QVBoxLayout(self)
        # header
        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(20, 0, 0, 0)
        headerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mainLayout.addLayout(headerLayout, 1)
        # fileNameLabel
        self.fileNameLabel = QLabel("", font=font2)
        self.fileNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.fileNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fileNameLabel.setFixedSize(400, 30)
        headerLayout.addWidget(self.fileNameLabel)

        # groupBoxLayout
        groupBoxLayout = QVBoxLayout()
        mainLayout.addLayout(groupBoxLayout, 20)
        # groupBoxLayout - contentGroupBox
        contentGroupBox = QGroupBox(textSetting.textList["rsRail"]["contents"])
        groupBoxLayout.addWidget(contentGroupBox)
        # groupBoxLayout - contentGroupBox - groupInLayout
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setContentsMargins(10, 0, 10, 0)
        self.contentLayout.setSpacing(0)
        contentGroupBox.setLayout(self.contentLayout)

    def deleteWidget(self):
        while self.contentLayout.count():
            item = self.contentLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def createWidget(self):
        self.createRailPosWidget()
        self.createRailNoWidget()
        self.createAmbNoWidget()
        self.createAmbModelWidget()
    
    def createRailPosWidget(self):
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        railLabelWidth = 90
        buttonWidth = 100
        buttonHeight = 30

        railPosFrame = QFrame()
        railPosFrame.setFixedHeight(85)
        self.contentLayout.addWidget(railPosFrame)
        railPosLayout = QHBoxLayout()
        railPosFrame.setLayout(railPosLayout)

        # rail1pGroupBox
        rail1pGroupBox = QGroupBox(textSetting.textList["rsRail"]["1pRailPos"])
        railPosLayout.addWidget(rail1pGroupBox)
        # rail1pGroupBox - groupInLayout
        rail1pGroupInLayout = QHBoxLayout()
        rail1pGroupInLayout.setContentsMargins(0, 0, 0, 0)
        rail1pGroupInLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rail1pGroupInLayout.setSpacing(0)
        rail1pGroupBox.setLayout(rail1pGroupInLayout)
        # rail1pGroupBox - groupInLayout - label
        self.rail1pRailNumLabel = QLabel("-1", font=font2)
        self.rail1pRailNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rail1pRailNumLabel.setFixedWidth(railLabelWidth)
        rail1pGroupInLayout.addWidget(self.rail1pRailNumLabel)
        self.rail1pRailPosLabel = QLabel("-1", font=font2)
        self.rail1pRailPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rail1pRailPosLabel.setFixedWidth(railLabelWidth)
        rail1pGroupInLayout.addWidget(self.rail1pRailPosLabel)

        # rail2pGroupBox
        rail2pGroupBox = QGroupBox(textSetting.textList["rsRail"]["2pRailPos"])
        railPosLayout.addWidget(rail2pGroupBox)
        # rail1pGroupBox - groupInLayout
        rail2pGroupInLayout = QHBoxLayout()
        rail2pGroupInLayout.setContentsMargins(0, 0, 0, 0)
        rail2pGroupInLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rail2pGroupInLayout.setSpacing(0)
        rail2pGroupBox.setLayout(rail2pGroupInLayout)
        # rail1pGroupBox - groupInLayout - label
        self.rail2pRailNumLabel = QLabel("-1", font=font2)
        self.rail2pRailNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rail2pRailNumLabel.setFixedWidth(railLabelWidth)
        rail2pGroupInLayout.addWidget(self.rail2pRailNumLabel)
        self.rail2pRailPosLabel = QLabel("-1", font=font2)
        self.rail2pRailPosLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rail2pRailPosLabel.setFixedWidth(railLabelWidth)
        rail2pGroupInLayout.addWidget(self.rail2pRailPosLabel)
        # QStackedWidget
        self.railPosStackButton = QStackedWidget()
        railPosSearchButton = QPushButton(textSetting.textList["rsRail"]["trainPosSearchBtnLabel"])
        railPosSearchButton.clicked.connect(self.startSearchRailPos)
        railPosSearchButton.setFixedSize(buttonWidth, buttonHeight)
        self.railPosStackButton.addWidget(railPosSearchButton)
        railPosSearchStopButton = QPushButton(textSetting.textList["rsRail"]["trainPosStopBtnLabel"])
        railPosSearchStopButton.clicked.connect(self.stopSearchRailPos)
        railPosSearchStopButton.setFixedSize(buttonWidth, buttonHeight)
        self.railPosStackButton.addWidget(railPosSearchStopButton)
        self.railPosStackButton.setCurrentIndex(0)
        railPosLayout.addWidget(self.railPosStackButton, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.railPosTimer = QTimer()
        self.railPosTimer.timeout.connect(self.setRailPos)

    def createRailNoWidget(self):
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?"), self)
        labelWidth = 80
        buttonWidth = 80
        buttonHeight = 30

        railNoFrame = QFrame()
        railNoFrame.setFixedHeight(60)
        self.contentLayout.addWidget(railNoFrame)
        railNoLayout = QVBoxLayout()
        railNoFrame.setLayout(railNoLayout)

        railNoInputLayout = QHBoxLayout()
        railNoLayout.addLayout(railNoInputLayout)
        # railNoNameLabel
        railNoNameLabel = QLabel(textSetting.textList["rsRail"]["railNo"], font=font2)
        railNoInputLayout.addWidget(railNoNameLabel)
        # railNoLineEdit
        self.railNoLineEdit = QLineEdit("0", font=font2)
        self.railNoLineEdit.setFixedWidth(labelWidth)
        self.railNoLineEdit.setValidator(integerValidator)
        self.railNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railNoInputLayout.addWidget(self.railNoLineEdit)
        railNoInputLayout.addSpacing(20)
        # railNoSearchButton
        self.railNoSearchButton = QPushButton(textSetting.textList["rsRail"]["railSearchBtnLabel"])
        self.railNoSearchButton.clicked.connect(self.searchInputRailNo)
        self.railNoSearchButton.setFixedSize(buttonWidth, buttonHeight)
        railNoInputLayout.addWidget(self.railNoSearchButton)
        railNoInputLayout.addSpacing(40)

        self.railNoStackButton = QStackedWidget()
        # railNoModifyButton
        railNoModifyButton = QPushButton(textSetting.textList["rsRail"]["railChangeBtnLabel"])
        railNoModifyButton.setEnabled(False)
        railNoModifyButton.clicked.connect(self.modifyInputRailNo)
        railNoModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.railNoStackButton.addWidget(railNoModifyButton)
        # railNoUpdateButton
        railNoSaveButton = QPushButton(textSetting.textList["rsRail"]["saveBtnLabel"])
        railNoSaveButton.clicked.connect(self.saveInputRailNo)
        railNoSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.railNoStackButton.addWidget(railNoSaveButton)
        self.railNoStackButton.setCurrentIndex(0)
        railNoInputLayout.addWidget(self.railNoStackButton, alignment=Qt.AlignmentFlag.AlignVCenter)
        railNoInputLayout.addStretch()

        railNoRsultFrame = QFrame()
        railNoRsultFrame.setFixedSize(750, 90)
        self.contentLayout.addWidget(railNoRsultFrame)
        railNoRsultLayout = QHBoxLayout()
        railNoRsultFrame.setLayout(railNoRsultLayout)
        # railXyzGroupBox
        railXyzGroupBox = QGroupBox(textSetting.textList["rsRail"]["railXyzInfo"])
        railNoRsultLayout.addWidget(railXyzGroupBox)
        # railXyzGroupBox - groupInLayout
        railXyzGroupInLayout = QHBoxLayout()
        railXyzGroupInLayout.setContentsMargins(10, 0, 10, 0)
        railXyzGroupInLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railXyzGroupInLayout.setSpacing(0)
        railXyzGroupBox.setLayout(railXyzGroupInLayout)
        # railXyzGroupBox - groupInLayout - dirXlabel
        railDirXRailNameLabel = QLabel(textSetting.textList["rsRail"]["railDirX"], font=font2)
        railXyzGroupInLayout.addWidget(railDirXRailNameLabel)
        railXyzGroupInLayout.addSpacing(20)
        self.railDirXRailLineEdit = QLineEdit("0.0", font=font2)
        self.railDirXRailLineEdit.setEnabled(False)
        self.railDirXRailLineEdit.setValidator(numberValidator)
        self.railDirXRailLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirXRailLineEdit.setFixedWidth(labelWidth)
        railXyzGroupInLayout.addWidget(self.railDirXRailLineEdit)
        railXyzGroupInLayout.addSpacing(40)
        # railXyzGroupBox - groupInLayout - dirYlabel
        railDirYRailNameLabel = QLabel(textSetting.textList["rsRail"]["railDirY"], font=font2)
        railXyzGroupInLayout.addWidget(railDirYRailNameLabel)
        railXyzGroupInLayout.addSpacing(20)
        self.railDirYRailLineEdit = QLineEdit("0.0", font=font2)
        self.railDirYRailLineEdit.setEnabled(False)
        self.railDirYRailLineEdit.setValidator(numberValidator)
        self.railDirYRailLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirYRailLineEdit.setFixedWidth(labelWidth)
        railXyzGroupInLayout.addWidget(self.railDirYRailLineEdit)
        railXyzGroupInLayout.addSpacing(40)
        # railXyzGroupBox - groupInLayout - dirZlabel
        railDirZRailNameLabel = QLabel(textSetting.textList["rsRail"]["railDirZ"], font=font2)
        railXyzGroupInLayout.addWidget(railDirZRailNameLabel)
        railXyzGroupInLayout.addSpacing(20)
        self.railDirZRailLineEdit = QLineEdit("0.0", font=font2)
        self.railDirZRailLineEdit.setEnabled(False)
        self.railDirZRailLineEdit.setValidator(numberValidator)
        self.railDirZRailLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railDirZRailLineEdit.setFixedWidth(labelWidth)
        railXyzGroupInLayout.addWidget(self.railDirZRailLineEdit)

        # railPerGroupBox
        railPerGroupBox = QGroupBox(textSetting.textList["rsRail"]["railModelPer"])
        railNoRsultLayout.addWidget(railPerGroupBox)
        # railPerGroupBox - groupInLayout
        railPerGroupInLayout = QHBoxLayout()
        railPerGroupInLayout.setContentsMargins(10, 0, 10, 0)
        railPerGroupInLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        railPerGroupInLayout.setSpacing(0)
        railPerGroupBox.setLayout(railPerGroupInLayout)
        # railPerGroupBox - groupInLayout - dirXlabel
        railPerRailNameLabel = QLabel(textSetting.textList["rsRail"]["railPer"], font=font2)
        railPerGroupInLayout.addWidget(railPerRailNameLabel)
        railPerGroupInLayout.addSpacing(20)
        self.railPerRailLineEdit = QLineEdit("0.0", font=font2)
        self.railPerRailLineEdit.setEnabled(False)
        self.railPerRailLineEdit.setValidator(numberValidator)
        self.railPerRailLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.railPerRailLineEdit.setFixedWidth(labelWidth)
        railPerGroupInLayout.addWidget(self.railPerRailLineEdit)
        railNoRsultLayout.addStretch()

    def createAmbNoWidget(self):
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?"), self)
        labelWidth = 80
        lineEditWidth = 100
        buttonWidth = 80
        buttonHeight = 30

        ambNoFrame = QFrame()
        ambNoFrame.setFixedSize(750, 60)
        self.contentLayout.addWidget(ambNoFrame)
        ambNoInputLayout = QHBoxLayout()
        ambNoFrame.setLayout(ambNoInputLayout)

        # ambNoNameLabel
        ambNoNameLabel = QLabel(textSetting.textList["rsRail"]["ambNo"], font=font2)
        ambNoInputLayout.addWidget(ambNoNameLabel)
        # ambNoLineEdit
        self.ambNoLineEdit = QLineEdit("0", font=font2)
        self.ambNoLineEdit.setFixedWidth(labelWidth)
        self.ambNoLineEdit.setValidator(integerValidator)
        self.ambNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambNoInputLayout.addWidget(self.ambNoLineEdit)
        ambNoInputLayout.addSpacing(20)
        # ambNoSearchButton
        self.ambNoSearchButton = QPushButton(textSetting.textList["rsRail"]["ambSearchBtnLabel"])
        self.ambNoSearchButton.clicked.connect(self.searchInputAmbNo)
        self.ambNoSearchButton.setFixedSize(buttonWidth, buttonHeight)
        ambNoInputLayout.addWidget(self.ambNoSearchButton)
        ambNoInputLayout.addSpacing(40)

        self.ambNoStackButton = QStackedWidget()
        # ambNoModifyButton
        ambNoModifyButton = QPushButton(textSetting.textList["rsRail"]["ambChangeBtnLabel"])
        ambNoModifyButton.setEnabled(False)
        ambNoModifyButton.clicked.connect(self.modifyInputAmbNo)
        ambNoModifyButton.setFixedSize(buttonWidth, buttonHeight)
        self.ambNoStackButton.addWidget(ambNoModifyButton)
        # ambNoUpdateButton
        ambNoSaveButton = QPushButton(textSetting.textList["rsRail"]["saveBtnLabel"])
        ambNoSaveButton.clicked.connect(self.saveInputAmbNo)
        ambNoSaveButton.setFixedSize(buttonWidth, buttonHeight)
        self.ambNoStackButton.addWidget(ambNoSaveButton)
        self.ambNoStackButton.setCurrentIndex(0)
        ambNoInputLayout.addWidget(self.ambNoStackButton, alignment=Qt.AlignmentFlag.AlignVCenter)
        ambNoInputLayout.addSpacing(40)
        # ambDelayNameLabel
        ambDelayNameLabel = QLabel(textSetting.textList["rsRail"]["ambRecreateTime"], font=font2)
        ambNoInputLayout.addWidget(ambDelayNameLabel)
        # ambNoLineEdit
        self.ambDelayLineEdit = QLineEdit("0.3", font=font2)
        self.ambDelayLineEdit.setFixedWidth(labelWidth)
        self.ambDelayLineEdit.setValidator(numberValidator)
        self.ambDelayLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ambNoInputLayout.addWidget(self.ambDelayLineEdit)
        ambNoInputLayout.addStretch()

        # ambContent
        ambContentScrollArea = QScrollArea()
        ambContentScrollArea.setWidgetResizable(True)
        self.contentLayout.addWidget(ambContentScrollArea)
        ambContentFrame = QFrame()
        ambContentScrollArea.setWidget(ambContentFrame)
        self.ambContentLayout = QVBoxLayout()
        ambContentFrame.setLayout(self.ambContentLayout)
        # ambParentInfoFrame
        ambParentInfoLayout = QHBoxLayout()
        self.ambContentLayout.addLayout(ambParentInfoLayout)

        # ambParentInfoGroupBox
        ambParentInfoGroupBox = QGroupBox(textSetting.textList["rsRail"]["ambInfoLabel"])
        ambParentInfoGroupBox.setFixedSize(235, 160)
        ambParentInfoLayout.addWidget(ambParentInfoGroupBox)
        # ambParentInfoGroupBox - groupInLayout
        ambParentInfoGroupInLayout = QGridLayout()
        ambParentInfoGroupBox.setLayout(ambParentInfoGroupInLayout)
        self.ambParentLineEditList = []
        # ambLengthNameLabel
        ambLengthNameLabel = QLabel(textSetting.textList["rsRail"]["ambLength"], font=font2)
        ambParentInfoGroupInLayout.addWidget(ambLengthNameLabel, 0, 0)
        # ambLengthLineEdit
        self.ambLengthLineEdit = QLineEdit("0.0", font=font2)
        self.ambLengthLineEdit.setEnabled(False)
        self.ambLengthLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambLengthLineEdit.setFixedWidth(lineEditWidth)
        self.ambLengthLineEdit.setValidator(numberValidator)
        self.ambLengthLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambLengthLineEdit)
        ambParentInfoGroupInLayout.addWidget(self.ambLengthLineEdit, 0, 1)
        # ambRailNoLabel
        ambRailNoLabel = QLabel(textSetting.textList["rsRail"]["ambRailNo"], font=font2)
        ambParentInfoGroupInLayout.addWidget(ambRailNoLabel, 1, 0)
        # ambRailNoLineEdit
        self.ambRailNoLineEdit = QLineEdit("0", font=font2)
        self.ambRailNoLineEdit.setEnabled(False)
        self.ambRailNoLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailNoLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailNoLineEdit.setValidator(integerValidator)
        self.ambRailNoLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailNoLineEdit)
        ambParentInfoGroupInLayout.addWidget(self.ambRailNoLineEdit, 1, 1)
        # ambRailPosLabel
        ambRailPosLabel = QLabel(textSetting.textList["rsRail"]["ambRailPos"], font=font2)
        ambParentInfoGroupInLayout.addWidget(ambRailPosLabel, 2, 0)
        # ambRailPosLineEdit
        self.ambRailPosLineEdit = QLineEdit("0", font=font2)
        self.ambRailPosLineEdit.setEnabled(False)
        self.ambRailPosLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailPosLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailPosLineEdit.setValidator(integerValidator)
        self.ambRailPosLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailPosLineEdit)
        ambParentInfoGroupInLayout.addWidget(self.ambRailPosLineEdit, 2, 1)

        # ambParentBaseGroupBox
        ambParentBaseGroupBox = QGroupBox(textSetting.textList["rsRail"]["ambPosDirInfo"])
        ambParentBaseGroupBox.setFixedSize(380, 160)
        ambParentInfoLayout.addWidget(ambParentBaseGroupBox)
        # ambParentBaseGroupBox - groupInLayout
        ambParentBaseGroupInLayout = QGridLayout()
        ambParentBaseGroupBox.setLayout(ambParentBaseGroupInLayout)
        # ambRailBasePosXLabel
        ambRailBasePosXLabel = QLabel(textSetting.textList["rsRail"]["ambBasePosX"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBasePosXLabel, 0, 0)
        # ambRailBasePosXLineEdit
        self.ambRailBasePosXLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBasePosXLineEdit.setEnabled(False)
        self.ambRailBasePosXLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBasePosXLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBasePosXLineEdit.setValidator(numberValidator)
        self.ambRailBasePosXLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBasePosXLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBasePosXLineEdit, 0, 1)
        # ambRailBasePosYLabel
        ambRailBasePosYLabel = QLabel(textSetting.textList["rsRail"]["ambBasePosY"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBasePosYLabel, 1, 0)
        # ambRailBasePosYLineEdit
        self.ambRailBasePosYLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBasePosYLineEdit.setEnabled(False)
        self.ambRailBasePosYLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBasePosYLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBasePosYLineEdit.setValidator(numberValidator)
        self.ambRailBasePosYLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBasePosYLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBasePosYLineEdit, 1, 1)
        # ambRailBasePosZLabel
        ambRailBasePosZLabel = QLabel(textSetting.textList["rsRail"]["ambBasePosZ"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBasePosZLabel, 2, 0)
        # ambRailBasePosZLineEdit
        self.ambRailBasePosZLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBasePosZLineEdit.setEnabled(False)
        self.ambRailBasePosZLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBasePosZLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBasePosZLineEdit.setValidator(numberValidator)
        self.ambRailBasePosZLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBasePosZLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBasePosZLineEdit, 2, 1)

        # ambRailBaseRotXLabel
        ambRailBaseRotXLabel = QLabel(textSetting.textList["rsRail"]["ambBaseRotX"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBaseRotXLabel, 0, 2)
        # ambRailBaseRotXLineEdit
        self.ambRailBaseRotXLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBaseRotXLineEdit.setEnabled(False)
        self.ambRailBaseRotXLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBaseRotXLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBaseRotXLineEdit.setValidator(numberValidator)
        self.ambRailBaseRotXLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBaseRotXLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBaseRotXLineEdit, 0, 3)
        # ambRailBaseRotYLabel
        ambRailBaseRotYLabel = QLabel(textSetting.textList["rsRail"]["ambBaseRotY"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBaseRotYLabel, 1, 2)
        # ambRailBaseRotYLineEdit
        self.ambRailBaseRotYLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBaseRotYLineEdit.setEnabled(False)
        self.ambRailBaseRotYLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBaseRotYLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBaseRotYLineEdit.setValidator(numberValidator)
        self.ambRailBaseRotYLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBaseRotYLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBaseRotYLineEdit, 1, 3)
        # ambRailBaseRotZLabel
        ambRailBaseRotZLabel = QLabel(textSetting.textList["rsRail"]["ambBaseRotZ"], font=font2)
        ambParentBaseGroupInLayout.addWidget(ambRailBaseRotZLabel, 2, 2)
        # ambRailBaseRotZLineEdit
        self.ambRailBaseRotZLineEdit = QLineEdit("0.0", font=font2)
        self.ambRailBaseRotZLineEdit.setEnabled(False)
        self.ambRailBaseRotZLineEdit.setContentsMargins(10, 0, 10, 0)
        self.ambRailBaseRotZLineEdit.setFixedWidth(lineEditWidth)
        self.ambRailBaseRotZLineEdit.setValidator(numberValidator)
        self.ambRailBaseRotZLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ambParentLineEditList.append(self.ambRailBaseRotZLineEdit)
        ambParentBaseGroupInLayout.addWidget(self.ambRailBaseRotZLineEdit, 2, 3)
        ambParentInfoLayout.addStretch()

    def createAmbModelWidget(self):
        # ambModelInfoGroupBox
        ambModelInfoGroupBox = QGroupBox(textSetting.textList["rsRail"]["ambModelInfo"])
        ambModelInfoGroupBox.setFixedWidth(600)
        self.ambContentLayout.addWidget(ambModelInfoGroupBox)
        ambModelInfoGroupBox.setLayout(self.createAmbModelInfo(self.ambParentLineEditList))

        ambChildModelInfoGroupBox = QGroupBox(textSetting.textList["rsRail"]["ambChildModelInfo"])
        ambChildModelInfoGroupBox.setFixedWidth(600)
        self.ambContentLayout.addWidget(ambChildModelInfoGroupBox)
        # ambModelInfoGroupBox - groupInLayout
        self.ambChildModelGroupInLayout = QVBoxLayout()
        ambChildModelInfoGroupBox.setLayout(self.ambChildModelGroupInLayout)

    def createAmbModelInfo(self, lineEditList, childFlag=False, childNo=None):
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?"), self)
        lineEditWidth = 100

        # ambModelInfoGroupBox - groupInLayout
        ambModelGroupInLayout = QGridLayout()
        if childFlag:
            # ambChildModelNameLabel
            ambChildModelNameLabel = QLabel(textSetting.textList["rsRail"]["ambChildModelSmf"].format(childNo), font=font2)
            ambModelGroupInLayout.addWidget(ambChildModelNameLabel, 0, 0, 1, 4)
        else:
            # ambModelNameLabel
            ambModelNameLabel = QLabel(textSetting.textList["rsRail"]["ambModelSmf"], font=font2)
            ambModelGroupInLayout.addWidget(ambModelNameLabel, 0, 0, 1, 4)

        # ambModelPosXLabel
        ambModelPosXLabel = QLabel(textSetting.textList["rsRail"]["ambModelPosX"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelPosXLabel, 1, 0)
        # ambModelPosXLineEdit
        ambModelPosXLineEdit = QLineEdit("0.0", font=font2)
        ambModelPosXLineEdit.setEnabled(False)
        ambModelPosXLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelPosXLineEdit.setFixedWidth(lineEditWidth)
        ambModelPosXLineEdit.setValidator(numberValidator)
        ambModelPosXLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelPosXLineEdit)
        ambModelGroupInLayout.addWidget(ambModelPosXLineEdit, 1, 1)
        # ambModelPosYLabel
        ambModelPosYLabel = QLabel(textSetting.textList["rsRail"]["ambModelPosY"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelPosYLabel, 1, 2)
        # ambModelPosYLineEdit
        ambModelPosYLineEdit = QLineEdit("0.0", font=font2)
        ambModelPosYLineEdit.setEnabled(False)
        ambModelPosYLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelPosYLineEdit.setFixedWidth(lineEditWidth)
        ambModelPosYLineEdit.setValidator(numberValidator)
        ambModelPosYLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelPosYLineEdit)
        ambModelGroupInLayout.addWidget(ambModelPosYLineEdit, 1, 3)
        # ambModelPosZLabel
        ambModelPosZLabel = QLabel(textSetting.textList["rsRail"]["ambModelPosZ"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelPosZLabel, 1, 4)
        # ambModelPosZLineEdit
        ambModelPosZLineEdit = QLineEdit("0.0", font=font2)
        ambModelPosZLineEdit.setEnabled(False)
        ambModelPosZLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelPosZLineEdit.setFixedWidth(lineEditWidth)
        ambModelPosZLineEdit.setValidator(numberValidator)
        ambModelPosZLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelPosZLineEdit)
        ambModelGroupInLayout.addWidget(ambModelPosZLineEdit, 1, 5)

        # ambModelDirXLabel
        ambModelDirXLabel = QLabel(textSetting.textList["rsRail"]["ambModelDirX"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelDirXLabel, 2, 0)
        # ambModelDirXLineEdit
        ambModelDirXLineEdit = QLineEdit("0.0", font=font2)
        ambModelDirXLineEdit.setEnabled(False)
        ambModelDirXLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelDirXLineEdit.setFixedWidth(lineEditWidth)
        ambModelDirXLineEdit.setValidator(numberValidator)
        ambModelDirXLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelDirXLineEdit)
        ambModelGroupInLayout.addWidget(ambModelDirXLineEdit, 2, 1)
        # ambModelDirYLabel
        ambModelDirYLabel = QLabel(textSetting.textList["rsRail"]["ambModelDirY"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelDirYLabel, 2, 2)
        # ambModelDirYLineEdit
        ambModelDirYLineEdit = QLineEdit("0.0", font=font2)
        ambModelDirYLineEdit.setEnabled(False)
        ambModelDirYLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelDirYLineEdit.setFixedWidth(lineEditWidth)
        ambModelDirYLineEdit.setValidator(numberValidator)
        ambModelDirYLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelDirYLineEdit)
        ambModelGroupInLayout.addWidget(ambModelDirYLineEdit, 2, 3)
        # ambModelDirZLabel
        ambModelDirZLabel = QLabel(textSetting.textList["rsRail"]["ambModelDirZ"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelDirZLabel, 2, 4)
        # ambModelDirZLineEdit
        ambModelDirZLineEdit = QLineEdit("0.0", font=font2)
        ambModelDirZLineEdit.setEnabled(False)
        ambModelDirZLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelDirZLineEdit.setFixedWidth(lineEditWidth)
        ambModelDirZLineEdit.setValidator(numberValidator)
        ambModelDirZLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelDirZLineEdit)
        ambModelGroupInLayout.addWidget(ambModelDirZLineEdit, 2, 5)

        # ambModelRotXLabel
        ambModelRotXLabel = QLabel(textSetting.textList["rsRail"]["ambModelRotX"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelRotXLabel, 3, 0)
        # ambModelRotXLineEdit
        ambModelRotXLineEdit = QLineEdit("0.0", font=font2)
        ambModelRotXLineEdit.setEnabled(False)
        ambModelRotXLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelRotXLineEdit.setFixedWidth(lineEditWidth)
        ambModelRotXLineEdit.setValidator(numberValidator)
        ambModelRotXLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelRotXLineEdit)
        ambModelGroupInLayout.addWidget(ambModelRotXLineEdit, 3, 1)
        # ambModelRotYLabel
        ambModelRotYLabel = QLabel(textSetting.textList["rsRail"]["ambModelRotY"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelRotYLabel, 3, 2)
        # ambModelRotYLineEdit
        ambModelRotYLineEdit = QLineEdit("0.0", font=font2)
        ambModelRotYLineEdit.setEnabled(False)
        ambModelRotYLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelRotYLineEdit.setFixedWidth(lineEditWidth)
        ambModelRotYLineEdit.setValidator(numberValidator)
        ambModelRotYLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelRotYLineEdit)
        ambModelGroupInLayout.addWidget(ambModelRotYLineEdit, 3, 3)
        # ambModelRotZLabel
        ambModelRotZLabel = QLabel(textSetting.textList["rsRail"]["ambModelRotZ"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelRotZLabel, 3, 4)
        # ambModelRotZLineEdit
        ambModelRotZLineEdit = QLineEdit("0.0", font=font2)
        ambModelRotZLineEdit.setEnabled(False)
        ambModelRotZLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelRotZLineEdit.setFixedWidth(lineEditWidth)
        ambModelRotZLineEdit.setValidator(numberValidator)
        ambModelRotZLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelRotZLineEdit)
        ambModelGroupInLayout.addWidget(ambModelRotZLineEdit, 3, 5)

        # ambModelPerLabel
        ambModelPerLabel = QLabel(textSetting.textList["rsRail"]["ambModelPer"], font=font2)
        ambModelGroupInLayout.addWidget(ambModelPerLabel, 4, 0)
        # ambModelPerLineEdit
        ambModelPerLineEdit = QLineEdit("0.0", font=font2)
        ambModelPerLineEdit.setEnabled(False)
        ambModelPerLineEdit.setContentsMargins(10, 0, 10, 0)
        ambModelPerLineEdit.setFixedWidth(lineEditWidth)
        ambModelPerLineEdit.setValidator(numberValidator)
        ambModelPerLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineEditList.append(ambModelPerLineEdit)
        ambModelGroupInLayout.addWidget(ambModelPerLineEdit, 4, 1)
        return ambModelGroupInLayout

    def setRailPos(self):
        try:
            val1PList = self.memoryObj.getRailPos(0)
            if val1PList is not None:
                self.rail1pRailNumLabel.setText("{0}".format(val1PList[0]))
                self.rail1pRailPosLabel.setText("{0}".format(val1PList[1]))
            else:
                self.rail1pRailNumLabel.setText("{0}".format(-1))
                self.rail1pRailPosLabel.setText("{0}".format(-1))
        except Exception:
            self.rail1pRailNumLabel.setText("{0}".format(-1))
            self.rail1pRailPosLabel.setText("{0}".format(-1))

        try:
            val2PList = self.memoryObj.getRailPos(1)
            if val2PList is not None:
                self.rail2pRailNumLabel.setText("{0}".format(val2PList[0]))
                self.rail2pRailPosLabel.setText("{0}".format(val2PList[1]))
            else:
                self.rail2pRailNumLabel.setText("{0}".format(-1))
                self.rail2pRailPosLabel.setText("{0}".format(-1))
        except Exception:
            self.rail2pRailNumLabel.setText("{0}".format(-1))
            self.rail2pRailPosLabel.setText("{0}".format(-1))

    def startSearchRailPos(self):
        self.railPosStackButton.setCurrentIndex(1)
        if not self.railPosTimer.isActive():
            self.railPosTimer.start(1)

    def stopSearchRailPos(self):
        self.railPosStackButton.setCurrentIndex(0)
        self.railPosTimer.stop()

    def searchInputRailNo(self):
        self.railNoStackButton.currentWidget().setEnabled(False)
        self.railDirXRailLineEdit.setText("{0}".format(float(0)))
        self.railDirYRailLineEdit.setText("{0}".format(float(0)))
        self.railDirZRailLineEdit.setText("{0}".format(float(0)))
        self.railPerRailLineEdit.setText("{0}".format(float(0)))

        try:
            valList = self.memoryObj.getRailMemory(int(self.railNoLineEdit.text()))
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E60"])
            return

        if valList is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E79"])
            return

        self.railNoStackButton.currentWidget().setEnabled(True)
        self.railDirXRailLineEdit.setText("{0}".format(round(valList[0], 5)))
        self.railDirYRailLineEdit.setText("{0}".format(round(valList[1], 5)))
        self.railDirZRailLineEdit.setText("{0}".format(round(valList[2], 5)))
        self.railPerRailLineEdit.setText("{0}".format(round(valList[3], 5)))

    def modifyInputRailNo(self):
        self.railNoSearchButton.setEnabled(False)
        self.railNoLineEdit.setEnabled(False)
        self.railNoStackButton.setCurrentIndex(1)
        self.railDirXRailLineEdit.setEnabled(True)
        self.railDirYRailLineEdit.setEnabled(True)
        self.railDirZRailLineEdit.setEnabled(True)
        self.railPerRailLineEdit.setEnabled(True)

    def saveInputRailNo(self):
        railNo = int(self.railNoLineEdit.text())
        message = textSetting.textList["infoList"]["I98"].format(railNo)
        result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
        if result == mb.CANCEL:
            return

        self.railNoSearchButton.setEnabled(True)
        self.railNoLineEdit.setEnabled(True)
        self.railNoStackButton.setCurrentIndex(0)
        self.railNoStackButton.currentWidget().setEnabled(False)
        self.railDirXRailLineEdit.setEnabled(False)
        self.railDirYRailLineEdit.setEnabled(False)
        self.railDirZRailLineEdit.setEnabled(False)
        self.railPerRailLineEdit.setEnabled(False)

        if result == mb.YES:
            valList = []
            try:
                valList.append(float(self.railDirXRailLineEdit.text()))
                valList.append(float(self.railDirYRailLineEdit.text()))
                valList.append(float(self.railDirZRailLineEdit.text()))
                valList.append(float(self.railPerRailLineEdit.text()))
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
                return

            if not self.memoryObj.saveMemory(railNo, valList):
                self.memoryObj.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E80"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I99"].format(railNo))
        else:
            self.searchInputRailNo()

    def searchInputAmbNo(self):
        self.ambNoStackButton.currentWidget().setEnabled(False)
        for lineEdit in self.ambParentLineEditList:
            lineEdit.setEnabled(False)

        try:
            valList = self.memoryObj.getAMBMemory(int(self.ambNoLineEdit.text()))
        except Exception:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E60"])
            return

        if valList is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E81"])
            return

        self.ambNoStackButton.currentWidget().setEnabled(True)
        for i, lineEdit in enumerate(self.ambParentLineEditList):
            if i in [1, 2]:
                lineEdit.setText("{0}".format(valList[i]))
            else:
                lineEdit.setText("{0}".format(round(valList[i], 5)))
        self.setAmbChildModel(valList[-1])

    def setAmbChildModel(self, childValList):
        self.deleteAmbChildModel(self.ambChildModelGroupInLayout)
        self.ambChildModelLineEditList = []
        for idx, childValInfo in enumerate(childValList):
            childLineEditList = []
            self.ambChildModelGroupInLayout.addLayout(self.createAmbModelInfo(childLineEditList, True, idx + 1))
            for i, lineEdit in enumerate(childLineEditList):
                lineEdit.setText("{0}".format(round(childValInfo[i], 5)))
            self.ambChildModelLineEditList.extend(childLineEditList)

            if idx < len(childValList) - 1:
                horizentalLayout = QVBoxLayout()
                self.ambChildModelGroupInLayout.addLayout(horizentalLayout)
                horizentalLine = QFrame()
                horizentalLine.setFrameShape(QFrame.Shape.HLine)
                horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
                horizentalLayout.addWidget(horizentalLine)

    def deleteAmbChildModel(self, inputLayout):
        while inputLayout.count():
            item = inputLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            layout = item.layout()
            if layout is not None:
                self.deleteAmbChildModel(layout)

    def modifyInputAmbNo(self):
        self.ambNoSearchButton.setEnabled(False)
        self.ambNoLineEdit.setEnabled(False)
        self.ambNoStackButton.setCurrentIndex(1)
        for lineEdit in self.ambParentLineEditList:
            lineEdit.setEnabled(True)
        for lineEdit in self.ambChildModelLineEditList:
            lineEdit.setEnabled(True)

    def saveInputAmbNo(self):
        ambNo = int(self.ambNoLineEdit.text())
        message = textSetting.textList["infoList"]["I100"].format(ambNo)
        result = mb.askyesnocancel(title=textSetting.textList["confirm"], message=message, icon="warning")
        if result == mb.CANCEL:
            return

        self.ambNoSearchButton.setEnabled(True)
        self.ambNoLineEdit.setEnabled(True)
        self.ambNoStackButton.setCurrentIndex(0)
        self.ambNoStackButton.currentWidget().setEnabled(False)
        for lineEdit in self.ambParentLineEditList:
            lineEdit.setEnabled(False)
        for lineEdit in self.ambChildModelLineEditList:
            lineEdit.setEnabled(False)

        if result == mb.YES:
            valList = []
            try:
                for i, lineEdit in enumerate(self.ambParentLineEditList):
                    if i in [1, 2]:
                        valList.append(int(lineEdit.text()))
                    else:
                        valList.append(float(lineEdit.text()))

                childList = []
                childInfo = []
                for i, lineEdit in enumerate(self.ambChildModelLineEditList):
                    childInfo.append(float(lineEdit.text()))
                    if i % 10 == 9:
                        childList.append(childInfo)
                        childInfo = []
                valList.append(childList)
            except Exception:
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E3"])
                return

            delay = 0.3
            try:
                delay = float(self.ambDelayLineEdit.text())
            except Exception:
                delay = 0.3

            if not self.memoryObj.saveAMBMemory(ambNo, valList, delay):
                self.memoryObj.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E82"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I101"].format(ambNo))
        else:
            self.searchInputAmbNo()

    def openFile(self):
        fileType = "{0} ({1})".format("DEND_RS_EXE", "*.exe")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )
        if not file_path:
            return

        filename = os.path.basename(file_path)
        self.fileNameLabel.setText("{0}".format(filename))
        del self.memoryObj
        self.memoryObj = GetMemory(file_path)
        if not self.memoryObj.open():
            self.memoryObj.printError()
            mb.showerror(title=textSetting.textList["error"], message=self.memoryObj.error)
            return
        self.deleteWidget()
        self.createWidget()
