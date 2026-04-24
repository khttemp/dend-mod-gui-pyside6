import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QComboBox,
    QStackedWidget, QPushButton, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()


class TrainModelWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget
        self.notchContentCnt = decryptFile.notchContentCnt
        self.font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])
        modelInfo = decryptFile.trainModelList[trainIndex]
        fixedWidth = 60

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - trainNumNameLabel
        trainNumNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["modelTrainLabel"], font=self.font6)
        trainNumNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        trainNumNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainNumNameLabel.setFixedWidth(fixedWidth)
        mainLayout.addWidget(trainNumNameLabel, 0, 0)
        # mainLayout - modelNameLabel
        modelNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["modelModelLabel"], font=self.font6)
        modelNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        modelNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modelNameLabel.setFixedWidth(fixedWidth)
        mainLayout.addWidget(modelNameLabel, 1, 0)
        # mainLayout - pantaNameLabel
        if len(modelInfo["pantaNames"]) > 0:
            pantaNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["modelPantaLabel"], font=self.font6)
            pantaNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            pantaNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pantaNameLabel.setFixedWidth(fixedWidth)
            mainLayout.addWidget(pantaNameLabel, 2, 0)
        # mainLayout - colNameLabel
        if len(modelInfo["colList"]) > 0:
            colNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["modelColLabel"], font=self.font6)
            colNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            colNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            colNameLabel.setFixedWidth(fixedWidth)
            mainLayout.addWidget(colNameLabel, 3, 0)

        self.comboList = []

        for i in range(modelInfo["mdlCnt"]):
            # mainLayout - trainNumLabel
            trainNumLabel = QLabel("{0}".format(i + 1), font=self.font6)
            trainNumLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            trainNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(trainNumLabel, 0, i + 1)
            # mainLayout - trainNumCombo
            trainNumCombo = QComboBox(font=self.font6)
            trainNumCombo.addItems(modelInfo["mdlNames"])
            trainNumCombo.setEnabled(False)
            mainLayout.addWidget(trainNumCombo, 1, i + 1)
            if modelInfo["mdlList"][i] == -1:
                trainNumCombo.setCurrentIndex(len(modelInfo["mdlNames"]) - 1)
            else:
                trainNumCombo.setCurrentIndex(modelInfo["mdlList"][i])
            self.comboList.append(trainNumCombo)
            # mainLayout - pantaCombo
            if len(modelInfo["pantaNames"]) > 0:
                pantaCombo = QComboBox(font=self.font6)
                pantaCombo.addItems(modelInfo["pantaNames"])
                pantaCombo.setEnabled(False)
                mainLayout.addWidget(pantaCombo, 2, i + 1)
                if modelInfo["pantaList"][i] == -1:
                    pantaCombo.setCurrentIndex(len(modelInfo["pantaNames"]) - 1)
                else:
                    pantaCombo.setCurrentIndex(modelInfo["pantaList"][i])
                self.comboList.append(pantaCombo)
            # mainLayout - colCombo
            if len(modelInfo["colList"]) > 0:
                colCombo = QComboBox(font=self.font6)
                colCombo.addItems(modelInfo["colNames"])
                colCombo.setEnabled(False)
                mainLayout.addWidget(colCombo, 3, i + 1)
                if modelInfo["colList"][i] == -1:
                    colCombo.setCurrentIndex(len(modelInfo["colNames"]) - 1)
                else:
                    colCombo.setCurrentIndex(modelInfo["colList"][i])
                self.comboList.append(colCombo)

        # stackButton
        self.stackButton = QStackedWidget()
        self.stackButton.setFixedHeight(28)
        # stackButton - editHenseiButton
        editHenseiButton = QPushButton(textSetting.textList["orgInfoEditor"]["orgModify"])
        editHenseiButton.clicked.connect(self.editHenseiTrain)
        self.stackButton.addWidget(editHenseiButton)
        # LSはパンタ情報がない場合、修正不可
        if self.decryptFile.game == "LS":
            if len(modelInfo["pantaNames"]) == 0:
                editHenseiButton.setEnabled(False)
        # countLayout - stackButton - saveHenseiButton
        saveHenseiButton = QPushButton(textSetting.textList["orgInfoEditor"]["trainSave"])
        saveHenseiButton.clicked.connect(self.saveHenseiTrain)
        self.stackButton.addWidget(saveHenseiButton)
        self.stackButton.setCurrentIndex(0)

    def editHenseiTrain(self):
        root = self.window()
        gameCombo = root.findChild(QWidget, "gameCombo")
        gameCombo.setEnabled(False)
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainCombo.setEnabled(False)
        menuCombo = root.findChild(QWidget, "menuCombo")
        menuCombo.setEnabled(False)
        editStageTrainButton = root.findChild(QPushButton, "editStageTrainButton")
        editStageTrainButton.setEnabled(False)

        self.stackButton.setCurrentIndex(1)

        for idx, combo in enumerate(self.comboList):
            if self.decryptFile.game == "LS":
                if idx % 3 == 1:
                    combo.setEnabled(True)
            elif self.decryptFile.game in ["BS", "CS"]:
                if idx % 3 != 2:
                    combo.setEnabled(True)
            else:
                combo.setEnabled(True)

    def saveHenseiTrain(self):
        root = self.window()
        gameCombo = root.findChild(QWidget, "gameCombo")
        gameCombo.setEnabled(True)
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainCombo.setEnabled(True)
        menuCombo = root.findChild(QWidget, "menuCombo")
        menuCombo.setEnabled(True)
        editStageTrainButton = root.findChild(QPushButton, "editStageTrainButton")
        editStageTrainButton.setEnabled(True)

        comboValueList = []
        for idx, combo in enumerate(self.comboList):
            # LSの場合、パンタのみ変更可能
            if self.decryptFile.game == "LS":
                if idx % 3 != 1:
                    continue
            # BS、CSの場合、モデル・パンタのみ変更可能
            elif self.decryptFile.game in ["BS", "CS"]:
                if idx % 3 == 2:
                    continue
            idx = combo.currentIndex()
            if idx == combo.count() - 1:
                idx = 255
            comboValueList.append(idx)

        if not self.decryptFile.saveHensei(self.trainIndex, comboValueList):
            self.decryptFile.printError()
            errorMsg = textSetting.textList["errorList"]["E4"]
            mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
            return
        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I55"])
        self.reloadWidget()
