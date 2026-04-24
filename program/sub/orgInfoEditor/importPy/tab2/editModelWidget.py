import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox,
    QGridLayout, QFrame, QComboBox,
    QStackedWidget, QPushButton, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

mb = customMessageBoxWidget.CustomMessageBox()


class EditModelWidget(QWidget):
    def __init__(self, trainIndex, decryptFile, reloadWidget):
        super().__init__()
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile
        self.reloadWidget = reloadWidget

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - editModelButton
        editModelButton = QPushButton(textSetting.textList["orgInfoEditor"]["modelInfoModify"])
        editModelButton.clicked.connect(self.editModel)
        mainLayout.addWidget(editModelButton)

    def editModel(self):
        editModelDialog = EditModelDialog(self, textSetting.textList["orgInfoEditor"]["editModelLabel"], self.trainIndex, self.decryptFile)
        if editModelDialog.exec() == QDialog.Accepted:
            self.reloadWidget()


class EditModelDialog(QDialog):
    def __init__(self, parent, title, trainIndex, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.trainIndex = trainIndex
        self.decryptFile = decryptFile

        # layout
        layout = QVBoxLayout(self)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    # def body(self, frame):
    #     modelInfo = self.decryptFile.trainModelList[self.trainIdx]
    #     self.henseiCnt = modelInfo["mdlCnt"]

    #     self.btnFrame = ttkCustomWidget.CustomTtkFrame(frame)
    #     self.btnFrame.pack(pady=5)
    #     self.listFrame = ttkCustomWidget.CustomTtkFrame(frame)
    #     self.listFrame.pack()

    #     self.editableNum = len(self.trainWidget.comboList) // modelInfo["mdlCnt"]

    #     self.selectListNum = 0
    #     self.selectIndex = 0
    #     self.selectValue = ""
    #     self.modelInfo = None

    #     self.modifyBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["modify"], style="custom.listbox.TButton", state="disabled", command=self.modify)
    #     self.modifyBtn.grid(padx=10, row=0, column=0, sticky=tkinter.W + tkinter.E)
    #     self.insertBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["insert"], style="custom.listbox.TButton", state="disabled", command=self.insert)
    #     self.insertBtn.grid(padx=10, row=0, column=1, sticky=tkinter.W + tkinter.E)
    #     self.deleteBtn = ttkCustomWidget.CustomTtkButton(self.btnFrame, text=textSetting.textList["delete"], style="custom.listbox.TButton", state="disabled", command=self.delete)
    #     self.deleteBtn.grid(padx=10, row=0, column=2, sticky=tkinter.W + tkinter.E)

    #     self.trackModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvDaishaTitle"])
    #     self.trackModelLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)
    #     self.v_trackModel = tkinter.StringVar(value=modelInfo["trackNames"])
    #     self.trackModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_trackModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
    #     self.trackModelList.grid(row=1, column=0, sticky=tkinter.W + tkinter.E)
    #     self.trackModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 0, self.trackModelList.curselection()))

    #     self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
    #     self.padLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)

    #     self.trainModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvMdlTitle"])
    #     self.trainModelLb.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)
    #     trainModelList = copy.deepcopy(modelInfo["mdlNames"])
    #     trainModelList.pop()
    #     self.v_trainModel = tkinter.StringVar(value=trainModelList)
    #     self.trainModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_trainModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
    #     self.trainModelList.grid(row=1, column=2, sticky=tkinter.W + tkinter.E)
    #     self.trainModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 1, self.trainModelList.curselection()))

    #     self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
    #     self.padLb.grid(row=0, column=3, sticky=tkinter.W + tkinter.E)

    #     self.pantaModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvPantaTitle"])
    #     self.pantaModelLb.grid(row=0, column=4, sticky=tkinter.W + tkinter.E)
    #     pantaModelList = copy.deepcopy(modelInfo["pantaNames"])
    #     pantaModelList.pop()
    #     self.v_pantaModel = tkinter.StringVar(value=pantaModelList)
    #     self.pantaModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_pantaModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
    #     self.pantaModelList.grid(row=1, column=4, sticky=tkinter.W + tkinter.E)
    #     self.pantaModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 2, self.pantaModelList.curselection()))

    #     if self.editableNum == 3:
    #         self.padLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, width=3)
    #         self.padLb.grid(row=0, column=5, sticky=tkinter.W + tkinter.E)

    #         self.colModelLb = ttkCustomWidget.CustomTtkLabel(self.listFrame, font=textSetting.textList["font2"], text=textSetting.textList["orgInfoEditor"]["csvColTitle"])
    #         self.colModelLb.grid(row=0, column=6, sticky=tkinter.W + tkinter.E)
    #         colModelList = copy.deepcopy(modelInfo["colNames"])
    #         colModelList.pop()
    #         self.v_colModel = tkinter.StringVar(value=colModelList)
    #         self.colModelList = tkinter.Listbox(self.listFrame, height=6, font=textSetting.textList["font2"], listvariable=self.v_colModel, bg=self.rootFrameAppearance.bgColor, fg=self.rootFrameAppearance.fgColor)
    #         self.colModelList.grid(row=1, column=6, sticky=tkinter.W + tkinter.E)
    #         self.colModelList.bind("<<ListboxSelect>>", lambda e: self.buttonActive(e, 3, self.colModelList.curselection()))
    #     super().body(frame)

    # def buttonActive(self, event, num, value):
    #     if len(value) == 0:
    #         return
    #     self.selectListNum = num
    #     self.selectIndex = value[0]
    #     if num == 0:
    #         self.selectValue = self.trackModelList.get(value[0])
    #     elif num == 1:
    #         self.selectValue = self.trainModelList.get(value[0])
    #     elif num == 2:
    #         self.selectValue = self.pantaModelList.get(value[0])
    #     elif num == 3:
    #         self.selectValue = self.colModelList.get(value[0])

    #     self.modifyBtn["state"] = "normal"
    #     self.insertBtn["state"] = "normal"
    #     self.deleteBtn["state"] = "normal"

    # def modify(self):
    #     resultObj = CustomAskstring(self, title=textSetting.textList["modify"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
    #     result = resultObj.result

    #     if result:
    #         if self.selectListNum == 0:
    #             self.trackModelList.delete(self.selectIndex)
    #             self.trackModelList.insert(self.selectIndex, result)
    #         elif self.selectListNum == 1:
    #             self.trainModelList.delete(self.selectIndex)
    #             self.trainModelList.insert(self.selectIndex, result)
    #         elif self.selectListNum == 2:
    #             self.pantaModelList.delete(self.selectIndex)
    #             self.pantaModelList.insert(self.selectIndex, result)
    #         elif self.selectListNum == 3:
    #             self.colModelList.delete(self.selectIndex)
    #             self.colModelList.insert(self.selectIndex, result)

    #         self.modifyBtn["state"] = "disabled"
    #         self.insertBtn["state"] = "disabled"
    #         self.deleteBtn["state"] = "disabled"

    # def insert(self):
    #     resultObj = CustomAskstring(self, title=textSetting.textList["insert"], prompt=textSetting.textList["infoList"]["I27"], initialvalue=self.selectValue, bgColor=self.rootFrameAppearance.bgColor)
    #     result = resultObj.result

    #     if result:
    #         if self.selectListNum == 0:
    #             self.trackModelList.insert(tkinter.END, result)
    #         elif self.selectListNum == 1:
    #             self.trainModelList.insert(tkinter.END, result)
    #         elif self.selectListNum == 2:
    #             self.pantaModelList.insert(tkinter.END, result)
    #         elif self.selectListNum == 3:
    #             self.colModelList.insert(tkinter.END, result)

    #         self.modifyBtn["state"] = "disabled"
    #         self.insertBtn["state"] = "disabled"
    #         self.deleteBtn["state"] = "disabled"

    # def delete(self):
    #     selectName = ""

    #     if self.selectListNum == 0:
    #         selectName = textSetting.textList["orgInfoEditor"]["csvDaishaTitle"]
    #         if self.game in [gameDefine.LS, gameDefine.BS]:
    #             if self.trackModelList.size() <= 1:
    #                 mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(1))
    #                 return
    #         elif self.game in [gameDefine.CS, gameDefine.RS]:
    #             if self.trackModelList.size() <= 2:
    #                 mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E67"].format(2))
    #                 return
    #     elif self.selectListNum == 1:
    #         selectName = textSetting.textList["orgInfoEditor"]["csvMdlTitle"]
    #         for i in range(self.henseiCnt):
    #             if self.selectIndex == self.trainWidget.comboList[self.editableNum * i].current():
    #                 mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
    #                 return
    #     elif self.selectListNum == 2:
    #         selectName = textSetting.textList["orgInfoEditor"]["csvPantaTitle"]
    #         for i in range(self.henseiCnt):
    #             if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 1].current():
    #                 mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
    #                 return
    #     elif self.selectListNum == 3:
    #         selectName = textSetting.textList["orgInfoEditor"]["csvColTitle"]
    #         for i in range(self.henseiCnt):
    #             if self.selectIndex == self.trainWidget.comboList[self.editableNum * i + 2].current():
    #                 mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E68"].format(i + 1))
    #                 return

    #     warnMsg = textSetting.textList["infoList"]["I62"].format(selectName, self.selectIndex + 1)
    #     result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

    #     if result:
    #         if self.selectListNum == 0:
    #             self.trackModelList.delete(self.selectIndex)
    #         elif self.selectListNum == 1:
    #             self.trainModelList.delete(self.selectIndex)
    #         elif self.selectListNum == 2:
    #             self.pantaModelList.delete(self.selectIndex)
    #         elif self.selectListNum == 3:
    #             self.colModelList.delete(self.selectIndex)

    #         self.modifyBtn["state"] = "disabled"
    #         self.insertBtn["state"] = "disabled"
    #         self.deleteBtn["state"] = "disabled"

    # def validate(self):
    #     warnMsg = textSetting.textList["infoList"]["I63"]
    #     result = mb.askokcancel(title=textSetting.textList["confirm"], message=warnMsg, icon="warning", parent=self)
    #     if result:
    #         modelInfo = self.decryptFile.trainModelList[self.trainIdx]

    #         newTrackList = []
    #         for i in range(self.trackModelList.size()):
    #             newTrackList.append(self.trackModelList.get(i))
    #         modelInfo["trackNames"] = newTrackList

    #         newTrainList = []
    #         for i in range(self.trainModelList.size()):
    #             newTrainList.append(self.trainModelList.get(i))
    #         newTrainList.append(textSetting.textList["orgInfoEditor"]["noList"])
    #         modelInfo["mdlNames"] = newTrainList

    #         newPantaList = []
    #         for i in range(self.pantaModelList.size()):
    #             newPantaList.append(self.pantaModelList.get(i))
    #         newPantaList.append(textSetting.textList["orgInfoEditor"]["noList"])
    #         modelInfo["pantaNames"] = newPantaList

    #         if self.editableNum == 3:
    #             newColList = []
    #             for i in range(self.colModelList.size()):
    #                 newColList.append(self.colModelList.get(i))
    #             newColList.append(textSetting.textList["orgInfoEditor"]["noList"])
    #             modelInfo["colNames"] = newColList
    #         else:
    #             newColList = []
    #             colName = modelInfo["colNames"][0]
    #             for i in range(self.trainModelList.size()):
    #                 newColList.append(colName)
    #             newColList.append(textSetting.textList["orgInfoEditor"]["noList"])
    #             modelInfo["colNames"] = newColList

    #         if not self.decryptFile.saveModelInfo(self.trainIdx, modelInfo):
    #             self.decryptFile.printError()
    #             errorMsg = textSetting.textList["errorList"]["E4"]
    #             mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
    #             return
    #         return True

    # def apply(self):
    #     mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I64"])
    #     self.reloadFlag = True
