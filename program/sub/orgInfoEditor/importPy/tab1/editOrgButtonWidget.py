import traceback
import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
from program.sub.errorLogClass import ErrorLogObj

from program.sub.orgInfoEditor.importPy.tab1.setDefaultWidget import SetDefaultEditDialog
from program.sub.orgInfoEditor.importPy.tab1.editAllTrainInfoWidget import EditAllTrainInfoDialog

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QStackedWidget, QPushButton, QDialog
)

mb = customMessageBoxWidget.CustomMessageBox()


class EditOrgButtonWidget(QWidget):
    def __init__(self, decryptFile, defaultData, reloadWidget):
        super().__init__()
        self.decryptFile = decryptFile
        self.defaultData = defaultData
        self.reloadWidget = reloadWidget
        oldGameList = ["RS", "CS", "BS", "LS"]

        buttonLayout = QHBoxLayout(self)
        # setDefaultTrainInfoButton
        self.setDefaultTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"])
        self.setDefaultTrainInfoButton.clicked.connect(self.setDefault)
        buttonLayout.addWidget(self.setDefaultTrainInfoButton, 1)
        # extractCsvTrainInfoButton
        if self.decryptFile.game in oldGameList:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractCsv"]
        else:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractText"]
        self.extractCsvTrainInfoButton = QPushButton(extractCsvButtonText)
        self.extractCsvTrainInfoButton.clicked.connect(self.extractCsvTrainInfo)
        buttonLayout.addWidget(self.extractCsvTrainInfoButton, 1)
        # saveCsvTrainInfoButton
        if self.decryptFile.game in oldGameList:
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
        setDefaultEditDialog = SetDefaultEditDialog(self, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], self.decryptFile, self.defaultData)
        if setDefaultEditDialog.exec() == QDialog.Accepted:
            self.reloadWidget()

        # result = SetDefaultEdit(tabFrame, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], decryptFile, game, trainIdx, defaultData, rootFrameAppearance)
        # if result.reloadFlag:
        #     reloadFunc()

    def extractCsvTrainInfo(self):
        pass
        # filename = decryptFile.trainNameList[trainIdx]
        # if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        #     file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="csv", filetypes=[("traininfo_csv", "*.csv")])
        #     errorMsg = textSetting.textList["errorList"]["E63"]
        #     if file_path:
        #         if not decryptFile.extractCsvTrainInfo(trainIdx, file_path):
        #             decryptFile.printError()
        #             mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        #             return False
        #         mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I10"])
        # else:
        #     file_path = fd.asksaveasfilename(initialfile=filename, defaultextension="txt", filetypes=[("traininfo_text", "*.txt")])
        #     errorMsg = textSetting.textList["errorList"]["E64"]
        #     if file_path:
        #         try:
        #             data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
        #             w = open(file_path, "wb")
        #             w.write(data.script)
        #             w.close()
        #             mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I48"])
        #         except Exception:
        #             errObj.write(traceback.format_exc())
        #             mb.showerror(title=textSetting.textList["error"], message=errorMsg)

    def saveCsvTrainInfo(self):
        pass
        # if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
        #     file_path = fd.askopenfilename(defaultextension="csv", filetypes=[("traindata_csv", "*.csv")])
        #     if not file_path:
        #         return
        #     csvLines = None
        #     try:
        #         f = open(file_path, "r", encoding="utf-8-sig")
        #         csvLines = f.readlines()
        #         f.close()
        #     except UnicodeDecodeError:
        #         f = open(file_path, "r", encoding=encObj.enc)
        #         csvLines = f.readlines()
        #         f.close()

        #     if not decryptFile.checkCsvResult(csvLines):
        #         mb.showerror(title=textSetting.textList["error"], message=decryptFile.error)
        #         return
        #     warnMsg = textSetting.textList["infoList"]["I11"]
        #     result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning")

        #     if result:
        #         errorMsg = textSetting.textList["errorList"]["E14"]
        #         if not decryptFile.saveCsvTrainInfo(trainIdx):
        #             decryptFile.printError()
        #             mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        #             return False
        #         mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
        #         reloadFunc()
        # else:
        #     file_path = fd.askopenfilename(filetypes=[("traininfo_text", "*.txt")])
        #     if not file_path:
        #         return
            
        #     f = open(file_path, "r", encoding="utf-8")
        #     lines = f.readlines()
        #     f.close()
        #     resultList = decryptFile.decryptLines(lines)
        #     if resultList is None:
        #         errorMsg = textSetting.textList["errorList"]["E98"].format(decryptFile.error)
        #         mb.showerror(title=textSetting.textList["error"], message=errorMsg)
        #         return

        #     result = mb.askquestion(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I50"], icon="warning")
        #     if result == "no":
        #         return

        #     try:
        #         data = decryptFile.dataList[decryptFile.trainNameList[trainIdx]]
        #         with open(file_path, "rb") as f:
        #             data.script = f.read()
        #         data.save()
        #         with open(decryptFile.filePath, "wb") as w:
        #             w.write(decryptFile.env.file.save())
        #         mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I51"])
        #         reloadFunc()
        #     except Exception:
        #         errObj.write(traceback.format_exc())
        #         mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])

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
