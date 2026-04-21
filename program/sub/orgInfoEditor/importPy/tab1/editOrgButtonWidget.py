import traceback
import program.sub.textSetting as textSetting
from program.sub.encodingClass import SJISEncodingObject
from program.sub.errorLogClass import ErrorLogObj

from program.sub.orgInfoEditor.importPy.tab1.setDefaultWidget import SetDefaultEditDialog
from program.sub.orgInfoEditor.importPy.tab1.editAllTrainInfoWidget import EditAllTrainInfoDialog

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QDialog
)
from PySide6.QtGui import QFont


class EditOrgButtonWidget(QWidget):
    def __init__(self, decryptFile, reloadWidget):
        super().__init__()
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget
        oldGameList = ["RS", "CS", "BS", "LS"]

        buttonLayout = QHBoxLayout(self)
        # setDefaultTrainInfoButton
        self.setDefaultTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"])
        self.setDefaultTrainInfoButton.clicked.connect(self.setDefault)
        buttonLayout.addWidget(self.setDefaultTrainInfoButton)
        # extractCsvTrainInfoButton
        if self.decryptFile.game in oldGameList:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractCsv"]
        else:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["extractText"]
        self.extractCsvTrainInfoButton = QPushButton(extractCsvButtonText)
        self.extractCsvTrainInfoButton.clicked.connect(self.extractCsvTrainInfo)
        buttonLayout.addWidget(self.extractCsvTrainInfoButton)
        # saveCsvTrainInfoButton
        if self.decryptFile.game in oldGameList:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["saveCsv"]
        else:
            extractCsvButtonText = textSetting.textList["orgInfoEditor"]["saveText"]
        self.saveCsvTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["saveText"])
        self.saveCsvTrainInfoButton.clicked.connect(self.saveCsvTrainInfo)
        buttonLayout.addWidget(self.saveCsvTrainInfoButton)
        # editTrainInfoButton
        self.editTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["trainModify"])
        self.editTrainInfoButton.clicked.connect(self.editTrainInfo)
        buttonLayout.addWidget(self.editTrainInfoButton)
        # editAllTrainInfoButton
        self.editAllTrainInfoButton = QPushButton(textSetting.textList["orgInfoEditor"]["allSave"])
        self.editAllTrainInfoButton.clicked.connect(self.editAllTrainInfo)
        buttonLayout.addWidget(self.editAllTrainInfoButton)

    def setDefault(self):
        setDefaultEditDialog = SetDefaultEditDialog(self, textSetting.textList["orgInfoEditor"]["setDefaultBtnLabel"], self.decryptFile)
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
        pass
        # v_edit = widgetList[0]
        # cb = widgetList[1]
        # menuCb = widgetList[2]
        # edit_stage_train_button = widgetList[3]

        # set_default_train_info_button = innerButtonList[0]
        # extract_csv_train_info_button = innerButtonList[1]
        # save_csv_train_info_button = innerButtonList[2]
        # edit_button = innerButtonList[3]
        # edit_all_button = innerButtonList[4]

        # v_edit.set(textSetting.textList["orgInfoEditor"]["trainSave"])
        # for btn in btnList:
        #     btn["state"] = "normal"

        # edit_button["command"] = lambda: saveTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)
        # cb["state"] = "disabled"
        # menuCb["state"] = "disabled"
        # edit_stage_train_button["state"] = "disabled"

        # set_default_train_info_button["state"] = "disabled"
        # extract_csv_train_info_button["state"] = "disabled"
        # save_csv_train_info_button["state"] = "disabled"
        # edit_all_button["state"] = "disabled"

    def saveTrainInfo(self):
        pass
        # v_edit = widgetList[0]
        # cb = widgetList[1]
        # menuCb = widgetList[2]
        # edit_stage_train_button = widgetList[3]

        # set_default_train_info_button = innerButtonList[0]
        # extract_csv_train_info_button = innerButtonList[1]
        # save_csv_train_info_button = innerButtonList[2]
        # edit_button = innerButtonList[3]

        # v_edit.set(textSetting.textList["orgInfoEditor"]["trainModify"])
        # for btn in btnList:
        #     btn["state"] = "disabled"

        # edit_button["command"] = lambda: editTrain(decryptFile, varList, btnList, widgetList, innerButtonList, reloadFunc)
        # cb["state"] = "readonly"
        # menuCb["state"] = "readonly"
        # edit_stage_train_button["state"] = "normal"

        # set_default_train_info_button["state"] = "normal"
        # extract_csv_train_info_button["state"] = "normal"
        # save_csv_train_info_button["state"] = "normal"

        # trainIdx = cb.current()

        # errorMsg = textSetting.textList["errorList"]["E4"]
        # if not decryptFile.saveTrainInfo(trainIdx, varList):
        #     decryptFile.printError()
        #     mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
        #     return

        # mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I49"])
        # reloadFunc()

    def editAllTrainInfo(self):
        editAllTrainInfoDialog = EditAllTrainInfoDialog(self, textSetting.textList["orgInfoEditor"]["allSaveLabel"], self.decryptFile)
        if editAllTrainInfoDialog.exec() == QDialog.Accepted:
            self.reloadWidget()
