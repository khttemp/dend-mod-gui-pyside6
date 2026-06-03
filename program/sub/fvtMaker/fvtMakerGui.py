import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

import program.sub.fvtMaker.fvtMakerProcess as fvtMakerProcess

from program.sub.fvtMaker.importPy.tableWidget import CsvWidget, DescWidget
from program.sub.fvtMaker.importPy.fvtConvert import FvtConvert

from PySide6.QtWidgets import (
    QWidget, QScrollArea, QFrame, QVBoxLayout, QHBoxLayout,
    QGroupBox, QRadioButton, QButtonGroup, QFileDialog
)
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()


class FvtMakerWindow(QWidget):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict
        self.fvtConvertFile = None
        self.LS = 1
        self.BS = 2
        self.CS = 3
        self.RS = 4

        mainLayout = QVBoxLayout(self)
        mainLayout.addSpacing(10)
        # header
        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(30, 0, 30, 0)
        headerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addLayout(headerLayout, 1)

        # header - lsRadio
        lsRadioButton = QRadioButton("Lightning Stage")
        lsRadioButton.toggled.connect(self.radioButtonTrigger)
        headerLayout.addWidget(lsRadioButton)
        # stretch
        headerLayout.addStretch()
        # header - bsRadio
        bsRadioButton = QRadioButton("Burning Stage")
        bsRadioButton.toggled.connect(self.radioButtonTrigger)
        headerLayout.addWidget(bsRadioButton)
        # stretch
        headerLayout.addStretch()
        # header - csRadio
        csRadioButton = QRadioButton("Climax Stage")
        csRadioButton.toggled.connect(self.radioButtonTrigger)
        headerLayout.addWidget(csRadioButton)
        # stretch
        headerLayout.addStretch()
        # header - rsRadio
        rsRadioButton = QRadioButton("Rising Stage")
        rsRadioButton.toggled.connect(self.radioButtonTrigger)
        headerLayout.addWidget(rsRadioButton)

        # RadioGroup
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(lsRadioButton, self.LS)
        self.radioGroup.addButton(bsRadioButton, self.BS)
        self.radioGroup.addButton(csRadioButton, self.CS)
        self.radioGroup.addButton(rsRadioButton, self.RS)

        # groupBoxLayout
        groupBoxLayout = QVBoxLayout()
        mainLayout.addLayout(groupBoxLayout, 20)

        # groupBoxLayout - csvGroupBox
        csvGroupBox = QGroupBox(textSetting.textList["fvtMaker"]["csvLfLabel"])
        groupBoxLayout.addWidget(csvGroupBox, 1)
        # groupBoxLayout - csvGroupBox - csvGroupInLayout
        csvGroupInLayout = QVBoxLayout()
        csvGroupInLayout.setContentsMargins(0, 0, 0, 0)
        csvGroupInLayout.setSpacing(0)
        csvGroupBox.setLayout(csvGroupInLayout)
        # csvScrollArea
        csvScrollArea = QScrollArea()
        csvScrollArea.setWidgetResizable(True)
        csvGroupInLayout.addWidget(csvScrollArea)
        # csvScrollArea - QFrame
        csvScrollAreaFrame = QFrame()
        csvScrollArea.setWidget(csvScrollAreaFrame)
        # csvScrollArea - QFrame - csvLayout
        self.csvLayout = QVBoxLayout()
        csvScrollAreaFrame.setLayout(self.csvLayout)

        # groupBoxLayout - descriptionGroupBox
        descriptionGroupBox = QGroupBox(textSetting.textList["fvtMaker"]["howWrite"])
        groupBoxLayout.addWidget(descriptionGroupBox, 2)
        # groupBoxLayout - descriptionGroupBox - descGroupInLayout
        descGroupInLayout = QVBoxLayout()
        descGroupInLayout.setContentsMargins(0, 0, 0, 0)
        descGroupInLayout.setSpacing(0)
        descriptionGroupBox.setLayout(descGroupInLayout)
        # descScrollArea
        descScrollArea = QScrollArea()
        descScrollArea.setWidgetResizable(True)
        descGroupInLayout.addWidget(descScrollArea)
        # descScrollArea - QFrame
        descScrollAreaFrame = QFrame()
        descScrollArea.setWidget(descScrollAreaFrame)
        # descScrollArea - QFrame - descLayout
        self.descLayout = QVBoxLayout()
        descScrollAreaFrame.setLayout(self.descLayout)

    def radioButtonTrigger(self, isChecked):
        if not isChecked:
            return
        
        self.deleteWidget()
        self.createWidget()

    def deleteWidget(self):
        for i in range(self.csvLayout.count()):
            item = self.csvLayout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if not widget:
                return
            widget.deleteLater()

        for i in range(self.descLayout.count()):
            item = self.descLayout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if not widget:
                return
            widget.deleteLater()

    def createWidget(self):
        game = self.radioGroup.checkedId()
        if game == self.LS:
            fvtInfo = self.importDict["fvtInfo"]["LS"]
        elif game == self.BS:
            fvtInfo = self.importDict["fvtInfo"]["BS"]
        elif game == self.CS:
            fvtInfo = self.importDict["fvtInfo"]["CS"]
        else:
            fvtInfo = self.importDict["fvtInfo"]["RS"]

        headerList, dataList = fvtMakerProcess.getCsvInfo(game, copy.deepcopy(fvtInfo))
        csvWidget = CsvWidget(headerList, dataList)
        self.csvLayout.addWidget(csvWidget)

        descWidget = DescWidget(self.importDict["fvtImageInfo"], game)
        self.descLayout.addWidget(descWidget)

    def openFile(self):
        game = self.radioGroup.checkedId()
        if game == -1:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E13"])
            return

        fileType = "{0} ({1})".format(textSetting.textList["fvtMaker"]["fileType"], "*.csv")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "",
            "",
            fileType
        )

        if not file_path:
            return

        del self.fvtConvertFile
        self.fvtConvertFile = FvtConvert(file_path, game)
        if not self.fvtConvertFile.open():
            self.fvtConvertFile.printError()
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E124"])
            return

        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I13"], icon="warning")
        if result == mb.OK:
            if not self.fvtConvertFile.write():
                self.fvtConvertFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I14"])
