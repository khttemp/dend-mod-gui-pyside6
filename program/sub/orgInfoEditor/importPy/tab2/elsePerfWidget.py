import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QGridLayout, QLabel,
    QPushButton, QDialog, QCheckBox, QLineEdit, QDialogButtonBox
)
from PySide6.QtGui import QFont, QPalette, QColor, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class ElsePerfWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, elsePerfName, elsePerfTextNameList, elsePerfList, isRequire, defaultData, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elsePerfName = elsePerfName
        self.elsePerfTextNameList = elsePerfTextNameList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        self.reloadWidget = reloadWidget
        fixedWidth = 86
        fixedHeight = 36
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - editButton
        editButton = QPushButton(textSetting.textList["orgInfoEditor"]["SSElsePerfModifyBtn"], font=font2)
        editButton.clicked.connect(self.editElsePerf)
        mainLayout.addWidget(editButton, 0, 0, 1, 2)

        for i in range(len(self.elsePerfTextNameList)):
            # mainLayout - elsePerfNameLabel
            elsePerfNameLabel = QLabel(self.elsePerfTextNameList[i], font=font6)
            elsePerfNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            elsePerfNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elsePerfNameLabel.setFixedHeight(fixedHeight)
            mainLayout.addWidget(elsePerfNameLabel, i + 1, 0)
            # mainLayout - elsePerfLabel
            if self.elsePerfList is not None:
                elsePerfLabel = QLabel("{0}".format(self.elsePerfList[i]), font=font6)
            else:
                elsePerfLabel = QLabel(textSetting.textList["orgInfoEditor"]["noPerf"], font=font6)
            elsePerfLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            elsePerfLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elsePerfLabel.setMinimumSize(fixedWidth, fixedHeight)
            mainLayout.addWidget(elsePerfLabel, i + 1, 1)

            if self.elsePerfName == "rain":
                defDataList = self.defaultData["rain"]
                self.perfTextName = textSetting.textList["orgInfoEditor"]["SSRainLfLabel"]
            elif self.elsePerfName == "carb":
                defDataList = self.defaultData["carb"]
                self.perfTextName = textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"]
            elif self.elsePerfName == "other":
                defDataList = self.defaultData["other"]
                self.perfTextName = textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"]
            elif self.elsePerfName == "huriko":
                defDataList = self.defaultData["huriko"]
                self.perfTextName = textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"]
            elif self.elsePerfName == "oneWheel":
                defDataList = self.defaultData["oneWheel"]
                self.perfTextName = textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"]

            color = QPalette().color(QPalette.WindowText)
            if self.elsePerfList is not None and defDataList is not None:
                if self.elsePerfName == "other":
                    if i in [0, 1, 2, 3]:
                        if self.elsePerfList[i] < defDataList[i]:
                            color = QColor("blue")
                        elif self.elsePerfList[i] > defDataList[i]:
                            color = QColor("red")
                else:
                    if self.elsePerfList[i] < defDataList[i]:
                        color = QColor("blue")
                    elif self.elsePerfList[i] > defDataList[i]:
                        color = QColor("red")
            elif self.elsePerfList is None and defDataList is not None:
                color = QColor("#444444")
            elif self.elsePerfList is not None and defDataList is None:
                color = QColor("green")
            self.setLabelColor(elsePerfNameLabel, elsePerfLabel, color)

    def setLabelColor(self, nameLabel, label, color):
        nameLabelPalette = nameLabel.palette()
        nameLabelPalette.setColor(QPalette.WindowText, color)
        nameLabel.setPalette(nameLabelPalette)
        labelPalette = label.palette()
        labelPalette.setColor(QPalette.WindowText, color)
        label.setPalette(labelPalette)

    def editElsePerf(self):
        editElsePerfInfo = EditElsePerfInfo(self, textSetting.textList["orgInfoEditor"]["SSElsePerfModifyLabel"].format(self.perfTextName), self.trainIndex, self.decryptFile, self.elsePerfName, self.elsePerfTextNameList, self.elsePerfList, self.isRequire, self.defaultData)
        if editElsePerfInfo.exec() == QDialog.Accepted:
            if not self.decryptFile.saveElsePerfList(self.trainIndex, self.elsePerfName, editElsePerfInfo.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
            self.reloadWidget()


class EditElsePerfInfo(QDialog):
    def __init__(self, parent, title, trainIndex, decryptFile, elsePerfName, elsePerfTextNameList, elsePerfList, isRequire, defaultData):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.elsePerfName = elsePerfName
        self.elsePerfTextNameList = elsePerfTextNameList
        self.elsePerfList = elsePerfList
        self.isRequire = isRequire
        self.defaultData = defaultData
        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        integerValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+$"), self)
        numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?"), self)

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=font2)
        layout.addWidget(label)
        # layout - QGridLayout
        elsePerfGridLayout = QGridLayout()
        layout.addLayout(elsePerfGridLayout)
        self.lineEditList = []

        if not self.isRequire:
            # layout - QGridLayout - perfUseLabel
            perfUseLabel = QLabel(textSetting.textList["orgInfoEditor"]["useThisPerfLabel"], font=font2)
            elsePerfGridLayout.addWidget(perfUseLabel, 0, 0)
            # layout - QGridLayout - QCheckBox
            self.useCheck = QCheckBox(font=font2)
            self.useCheck.toggled.connect(self.enablePerfInput)
            elsePerfGridLayout.addWidget(self.useCheck, 0, 1)
            if self.elsePerfList is None:
                self.useCheck.setChecked(False)
            else:
                self.useCheck.setChecked(True)

        for i in range(len(self.elsePerfTextNameList)):
            # layout - QGridLayout - elsePerfNameLabel
            elsePerfNameLabel = QLabel(self.elsePerfTextNameList[i], font=font2)
            elsePerfGridLayout.addWidget(elsePerfNameLabel, i + 1, 0)
            # layout - QGridLayout - elsePerfLineEdit
            elsePerfLineEdit = QLineEdit(font=font2)
            self.lineEditList.append(elsePerfLineEdit)
            elsePerfGridLayout.addWidget(elsePerfLineEdit, i + 1, 1)
            if self.elsePerfName == "other":
                if i in [0, 2, 3]:
                    elsePerfLineEdit.setValidator(integerValidator)
                elif i == 1:
                    elsePerfLineEdit.setValidator(numberValidator)
                elsePerfLineEdit.setText("{0}".format(self.elsePerfList[i]))
            else:
                elsePerfLineEdit.setValidator(numberValidator)
                if self.elsePerfList is not None:
                    elsePerfLineEdit.setText("{0}".format(self.elsePerfList[i]))

            if self.elsePerfName == "rain":
                defDataList = self.defaultData["rain"]
            elif self.elsePerfName == "carb":
                defDataList = self.defaultData["carb"]
            elif self.elsePerfName == "other":
                defDataList = self.defaultData["other"]
            elif self.elsePerfName == "huriko":
                defDataList = self.defaultData["huriko"]
            elif self.elsePerfName == "oneWheel":
                defDataList = self.defaultData["oneWheel"]

            if self.elsePerfName == "other":
                if i in [0, 1, 2, 3]:
                    defaultLabel = QLabel("{0}".format(defDataList[i]), font=font2)
                    elsePerfGridLayout.addWidget(defaultLabel, i + 1, 2)
            elif defDataList is not None:
                defaultLabel = QLabel("{0}".format(defDataList[i]), font=font2)
                elsePerfGridLayout.addWidget(defaultLabel, i + 1, 2)
        self.enablePerfInput()

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def enablePerfInput(self):
        if not self.isRequire:
            usedFlag = self.useCheck.isChecked()
            for lineEdit in self.lineEditList:
                if usedFlag:
                    lineEdit.setEnabled(True)
                else:
                    lineEdit.setEnabled(False)

    def validate(self):
        self.resultValueList = []
        if not self.isRequire and not self.useCheck.isChecked():
            self.resultValueList = None
        else:
            for lineEdit in self.lineEditList:
                if not lineEdit.hasAcceptableInput():
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return
                self.resultValueList.append(lineEdit.text())
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I60"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()
