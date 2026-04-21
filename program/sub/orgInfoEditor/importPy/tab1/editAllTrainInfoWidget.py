
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QDialogButtonBox, QPushButton
)
from PySide6.QtGui import QFont

class EditAllTrainInfoDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        # layout
        layout = QVBoxLayout(self)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

#     def __init__(self, master, title, decryptFile, rootFrameAppearance):
#         self.decryptFile = decryptFile
#         self.notchContentCnt = decryptFile.notchContentCnt
#         self.reloadFlag = False
#         super().__init__(master, title, rootFrameAppearance.bgColor)

#     def body(self, master):
#         self.eleLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["perfElement"], width=5, font=textSetting.textList["font2"])
#         self.eleLb.grid(row=0, column=0, sticky=tkinter.N + tkinter.S, padx=3)
#         self.v_ele = tkinter.StringVar()
#         self.eleCb = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_ele, width=24, value=self.decryptFile.trainPerfNameList, state="readonly")
#         self.eleCb.grid(row=0, column=1, sticky=tkinter.N + tkinter.S, padx=3)
#         self.v_ele.set(self.decryptFile.trainPerfNameList[0])

#         self.allLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["orgInfoEditor"]["perfAllTrainLabel"], width=5, font=textSetting.textList["font2"])
#         self.allLb.grid(row=0, column=2, sticky=tkinter.N + tkinter.S, padx=3)

#         self.v_num = tkinter.DoubleVar()
#         self.v_num.set(1.0)
#         self.numEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.v_num, width=6, font=textSetting.textList["font2"], justify="right")
#         self.numEt.grid(row=0, column=3, sticky=tkinter.N + tkinter.S, padx=3)

#         calcList = textSetting.textList["orgInfoEditor"]["perfCalcList"]
#         self.v_ele2 = tkinter.StringVar()
#         self.eleCb2 = ttkCustomWidget.CustomTtkCombobox(master, textvariable=self.v_ele2, font=textSetting.textList["font2"], width=8, value=calcList, state="readonly")
#         self.v_ele2.set(calcList[0])

#         self.eleCb2.grid(row=0, column=4, sticky=tkinter.N + tkinter.S, padx=3)
#         super().body(master)

#     def validate(self):
#         try:
#             result = float(self.v_num.get())
#             if self.eleCb2.current() == 0:
#                 warnMsg = textSetting.textList["infoList"]["I52"]
#             else:
#                 warnMsg = textSetting.textList["infoList"]["I53"]
#             result = mb.askokcancel(title=textSetting.textList["warning"], message=warnMsg, icon="warning", parent=self)

#             if result:
#                 perfIndex = self.eleCb.current()
#                 num = self.v_num.get()

#                 errorMsg = textSetting.textList["errorList"]["E4"]
#                 if not self.decryptFile.saveAllEdit(perfIndex, num, self.eleCb2.current()):
#                     self.decryptFile.printError()
#                     mb.showerror(title=textSetting.textList["saveError"], message=errorMsg)
#                     return False
#                 return True
#         except Exception:
#             errorMsg = textSetting.textList["errorList"]["E3"]
#             mb.showerror(title=textSetting.textList["numberError"], message=errorMsg, parent=self)

#     def apply(self):
#         mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I54"])
#         self.reloadFlag = True