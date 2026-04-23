import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
from program.sub.errorLogClass import ErrorLogObj

from program.sub.orgInfoEditor.importPy.tab1.setDefaultWidget import SetDefaultEditDialog
from program.sub.orgInfoEditor.importPy.tab1.editAllTrainInfoWidget import EditAllTrainInfoDialog
import program.sub.orgInfoEditor.importPy.tab1.trainInfoProcess as trainInfoProcess

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QStackedWidget, QPushButton, QDialog,
    QFileDialog
)

mb = customMessageBoxWidget.CustomMessageBox()


class EditOrgButtonWidget(QWidget):
    def __init__(self, decryptFile, defaultData, reloadWidget):
        super().__init__()
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.reloadWidget = reloadWidget
        self.oldGameList = ["RS", "CS", "BS", "LS"]

        buttonLayout = QHBoxLayout(self)
        # setDefaultTrainInfoButton
        self.setDefaultTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"])
        self.setDefaultTrainInfoButton.clicked.connect(self.setDefault)
        buttonLayout.addWidget(self.setDefaultTrainInfoButton, 1)
        # extractCsvTrainInfoButton
        if self.decryptFile.game in self.oldGameList:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractCsv"]
        else:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractText"]
        self.extractCsvTrainInfoButton = QPushButton(extractCsvButtonText)
        self.extractCsvTrainInfoButton.clicked.connect(self.extractCsvTrainInfo)
        buttonLayout.addWidget(self.extractCsvTrainInfoButton, 1)
        # saveCsvTrainInfoButton
        if self.decryptFile.game in self.oldGameList:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["saveCsv"]
        else:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["saveText"]
        self.saveCsvTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["saveText"])
        self.saveCsvTrainInfoButton.clicked.connect(self.saveCsvTrainInfo)
        buttonLayout.addWidget(self.saveCsvTrainInfoButton, 1)
        # editTrainInfoButton
        self.stackButton = QStackedWidget()
        self.stackButton.setFixedHeight(26)
        editTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["trainModify"])
        editTrainInfoButton.clicked.connect(self.editTrainInfo)
        self.stackButton.addWidget(editTrainInfoButton)
        # saveTrainInfoButton
        saveTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["trainSave"])
        saveTrainInfoButton.clicked.connect(self.saveTrainInfo)
        self.stackButton.addWidget(saveTrainInfoButton)
        buttonLayout.addWidget(self.stackButton, 1)
        # editAllTrainInfoButton
        self.editAllTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["allSave"])
        self.editAllTrainInfoButton.clicked.connect(self.editAllTrainInfo)
        buttonLayout.addWidget(self.editAllTrainInfoButton, 1)

    def setDefault(self):
        root = self.window()
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainIndex = trainCombo.currentIndex()
        setDefaultEditDialog = SetDefaultEditDialog(self, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], trainIndex, self.decryptFile, self.defaultData)
        if setDefaultEditDialog.exec() == QDialog.Accepted:
            self.reloadWidget()

    def extractCsvTrainInfo(self):
        root = self.window()
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainIndex = trainCombo.currentIndex()
        if self.decryptFile.game in self.oldGameList:
            filename = self.decryptFile.trainNameList[trainIndex] + ".csv"
            fileTypes = "traininfo_csv (*.csv)"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "",
                filename,
                fileTypes
            )
            if file_path:
                if not self.decryptFile.extractCsvTrainInfo(trainIndex, file_path):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E63"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        else:
            filename = self.decryptFile.trainNameList[trainIndex] + ".txt"
            fileTypes = "traininfo_text (*.txt)"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "",
                filename,
                fileTypes
            )
            if file_path:
                data = self.decryptFile.dataList[self.decryptFile.trainNameList[trainIndex]]
                if not trainInfoProcess.extractTrainInfoByDenFile(file_path, data):
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E64"])
                    return
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I48"])

    def saveCsvTrainInfo(self):
        root = self.window()
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainIndex = trainCombo.currentIndex()
        if self.decryptFile.game in self.oldGameList:
            fileTypes = "traininfo_csv (*.csv)"
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes
            )
            if not file_path:
                return

            if not self.decryptFile.checkCsvResult(file_path):
                mb.showerror(title=textSetting.textList["error"], message=self.decryptFile.error)
                return
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I11"], icon="warning")
            if result == mb.OK:
                if not self.decryptFile.saveCsvTrainInfo(trainIndex):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                    return False
                mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
                self.reloadWidget()
        else:
            fileTypes = "traininfo_text (*.txt)"
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "",
                "",
                fileTypes
            )
            if not file_path:
                return
            
            lines = trainInfoProcess.loadTrainInfoTextFile(file_path)
            resultList = self.decryptFile.decryptLines(lines)
            if resultList is None:
                errorMsg = textSetting.textList["errorList"]["E98"].format(self.decryptFile.error)
                mb.showerror(title=textSetting.textList["error"], message=errorMsg)
                return

            result = mb.askyesno(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
            if result == mb.NO:
                return

            data = self.decryptFile.dataList[self.decryptFile.trainNameList[trainIndex]]
            if not trainInfoProcess.saveTrainInfoDenFile(file_path, data, self.decryptFile):
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
            self.reloadWidget()

    def editTrainInfo(self):
        root = self.window()
        gameCombo = root.findChild(QWidget, "gameCombo")
        gameCombo.setEnabled(False)
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainCombo.setEnabled(False)
        menuCombo = root.findChild(QWidget, "menuCombo")
        menuCombo.setEnabled(False)
        editStageTrainButton = root.findChild(QPushButton, "editStageTrainButton")
        editStageTrainButton.setEnabled(False)

        speedContentFrame = root.findChild(QWidget, "speedContentFrame")
        speedContentLayout = speedContentFrame.layout()
        for i in range(speedContentLayout.count()):
            item = speedContentLayout.itemAt(i)
            if item.widget():
                buttonList = item.widget().findChildren(QPushButton, "")
                for button in buttonList:
                    button.setEnabled(True)

        perfContentFrame = root.findChild(QWidget, "perfContentFrame")
        perfContentLayout = perfContentFrame.layout()
        for i in range(perfContentLayout.count()):
            item = perfContentLayout.itemAt(i)
            if item.widget():
                button = item.widget().findChild(QPushButton, "")
                button.setEnabled(True)
        self.setDefaultTrainInfoButton.setEnabled(False)
        self.extractCsvTrainInfoButton.setEnabled(False)
        self.saveCsvTrainInfoButton.setEnabled(False)
        self.stackButton.setCurrentIndex(1)
        self.editAllTrainInfoButton.setEnabled(False)

    def saveTrainInfo(self):
        valueList = []
        root = self.window()
        gameCombo = root.findChild(QWidget, "gameCombo")
        gameCombo.setEnabled(True)
        trainCombo = root.findChild(QWidget, "trainCombo")
        trainCombo.setEnabled(True)
        menuCombo = root.findChild(QWidget, "menuCombo")
        menuCombo.setEnabled(True)
        editStageTrainButton = root.findChild(QPushButton, "editStageTrainButton")
        editStageTrainButton.setEnabled(True)

        speedContentFrame = root.findChild(QWidget, "speedContentFrame")
        speedContentLayout = speedContentFrame.layout()
        for i in range(speedContentLayout.count()):
            item = speedContentLayout.itemAt(i)
            if item.widget():
                valueList.append(item.widget().speedValue)
                valueList.append(item.widget().tlkValue)
                if self.decryptFile.notchContentCnt > 2:
                    valueList.append(item.widget().soundValue)
                    valueList.append(item.widget().addValue)
                buttonList = item.widget().findChildren(QPushButton, "")
                for button in buttonList:
                    button.setEnabled(False)

        perfContentFrame = root.findChild(QWidget, "perfContentFrame")
        perfContentLayout = perfContentFrame.layout()
        for i in range(len(self.decryptFile.trainPerfNameList)):
            item = perfContentLayout.itemAt(i)
            if item.widget():
                valueList.append(item.widget().perfValue)
                button = item.widget().findChild(QPushButton, "")
                button.setEnabled(False)

        if self.decryptFile.game in ["CS", "RS"]:
            for i in range(2):
                index = len(self.decryptFile.trainPerfNameList)
                item = perfContentLayout.itemAt(index + i)
                if item.widget():
                    valueList.append(item.widget().hurikoValue)
                    button = item.widget().findChild(QPushButton, "")
                    button.setEnabled(False)

        self.setDefaultTrainInfoButton.setEnabled(True)
        self.extractCsvTrainInfoButton.setEnabled(True)
        self.saveCsvTrainInfoButton.setEnabled(True)
        self.stackButton.setCurrentIndex(0)
        self.editAllTrainInfoButton.setEnabled(True)

        trainIndex = trainCombo.currentIndex()
        if not self.decryptFile.saveTrainInfo(trainIndex, valueList):
            self.decryptFile.printError()
            mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
            return

        mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
        self.reloadWidget()

    def editAllTrainInfo(self):
        editAllTrainInfoDialog = EditAllTrainInfoDialog(self, textSetting.textList["orgInfoEditor"]["allSaveLabel"], self.decryptFile)
        if editAllTrainInfoDialog.exec() == QDialog.Accepted:
            self.reloadWidget()
