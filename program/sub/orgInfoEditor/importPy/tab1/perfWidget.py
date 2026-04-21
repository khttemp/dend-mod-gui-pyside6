import program.sub.textSetting as textSetting

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QLabel, QPushButton,
    QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class PerfWidget(QWidget):
    def __init__(self, decryptFile, perfName, perfValue, defaultData):
        super().__init__()
        self.decryptFile = decryptFile
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        fixedWidth = 100
        fixedHeight = 40

        # perfNameLabel
        perfNameLabel = QLabel(perfName, font=font6)
        perfNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        perfNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(perfNameLabel, 0, 0)
        # perfLabel
        perfLabel = QLabel("{0}".format(perfValue), font=font6)
        perfLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        perfLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        perfLabel.setFixedSize(fixedWidth, fixedHeight)
        mainLayout.addWidget(perfLabel, 0, 1)
        # editPerfButton
        editPerfButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editPerfButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(editPerfButton, 0, 2)

        # color = ""
        # if self.defaultData[self.cbIdx]["att"][i] < perf[i]:
        #     color = "red"
        # elif self.defaultData[self.cbIdx]["att"][i] > perf[i]:
        #     color = "blue"
        # else:
        #     color = "black"
        # self.perfNameLb.setFgColor(color)
        # self.perfLb.setFgColor(color)

    def editVar(self, labelList, var, value, defaultValue, flag=False):
        EditPerfVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, defaultValue, self.rootFrameAppearance, flag)


# class EditPerfVarInfo(CustomSimpleDialog):
#     def __init__(self, master, title, labelList, var, value, defaultValue, rootFrameAppearance, flag=False):
#         self.labelList = labelList
#         self.var = var
#         self.value = value
#         self.defaultValue = defaultValue
#         self.flag = flag
#         super().__init__(master, title, rootFrameAppearance.bgColor)

#     def body(self, frame):
#         self.defaultLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
#         self.defaultLb.pack()

#         sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
#         sep.pack(fill=tkinter.X, ipady=5)

#         self.inputLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
#         self.inputLb.pack()

#         self.v_val = tkinter.StringVar()
#         self.v_val.set(self.value)
#         self.inputEt = ttkCustomWidget.CustomTtkEntry(frame, textvariable=self.v_val, font=textSetting.textList["font2"])
#         self.inputEt.pack()
#         super().body(frame)

#     def validate(self):
#         result = self.inputEt.get()
#         if result:
#             try:
#                 if self.flag:
#                     try:
#                         result = int(result)
#                         if result < 0:
#                             errorMsg = textSetting.textList["errorList"]["E61"].format(0)
#                             mb.showerror(title=textSetting.textList["intError"], message=errorMsg)
#                             return False
#                         self.var.set(result)
#                     except Exception:
#                         errorMsg = textSetting.textList["errorList"]["E60"]
#                         mb.showerror(title=textSetting.textList["intError"], message=errorMsg)
#                         return False
#                 else:
#                     try:
#                         result = float(result)
#                         self.var.set(result)
#                     except Exception:
#                         errorMsg = textSetting.textList["errorList"]["E3"]
#                         mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
#                         return False
#             except Exception:
#                 errorMsg = textSetting.textList["errorList"]["E14"]
#                 mb.showerror(title=textSetting.textList["error"], message=errorMsg)
#                 return False

#             if self.defaultValue is not None:
#                 color = ""
#                 if self.defaultValue < result:
#                     color = "red"
#                 elif self.defaultValue > result:
#                     color = "blue"
#                 else:
#                     color = "black"

#                 for label in self.labelList:
#                     label.setFgColor(color)
#             return True
