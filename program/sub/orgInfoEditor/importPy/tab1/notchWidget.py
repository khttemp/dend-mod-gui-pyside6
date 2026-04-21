import program.sub.textSetting as textSetting

from PySide6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QLabel, QPushButton,
    QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class NotchWidget(QWidget):
    def __init__(self, notchIndex, decryptFile, notchCnt, speed, defaultData):
        super().__init__()
        self.notchIndex = notchIndex
        self.decryptFile = decryptFile
        self.notchContentCnt = decryptFile.notchContentCnt
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        rowSpanNum = self.notchContentCnt
        # notchLabel
        notchText = textSetting.textList["orgInfoEditor"]["notchLabel"] + str(notchIndex + 1)
        notchLabel = QLabel(notchText, font=font6)
        notchLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        notchLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(notchLabel, 0, 0, rowSpanNum, 1)

        # try:
        #     color = ""
        #     if self.defaultData[self.cbIdx]["notch"][i] < speed[i]:
        #         color = "red"
        #     elif self.defaultData[self.cbIdx]["notch"][i] > speed[i]:
        #         color = "blue"
        #     else:
        #         color = "black"
        #     speedDefaultValue = self.defaultData[self.cbIdx]["notch"][i]
        # except Exception:
        #     color = "green"
        #     speedDefaultValue = None

        # speedNameLabel
        speedNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchSpeed"], font=font6)
        speedNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        speedNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(speedNameLabel, 0, 1)
        # speedLabel
        speedLabel = QLabel("{0}".format(speed[notchIndex]), font=font6)
        speedLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        speedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(speedLabel, 0, 2)
        # editSpeedButton
        editSpeedButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editSpeedButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(editSpeedButton, 0, 3)

        # try:
        #     color = ""
        #     if self.defaultData[self.cbIdx]["tlk"][i] < speed[notchCnt + i]:
        #         color = "red"
        #     elif self.defaultData[self.cbIdx]["tlk"][i] > speed[notchCnt + i]:
        #         color = "blue"
        #     else:
        #         color = "black"
        #     tlkDefaultValue = self.defaultData[self.cbIdx]["tlk"][i]
        # except Exception:
        #     color = "green"
        #     tlkDefaultValue = None

        # tlkNameLabel
        tlkNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchTlk"], font=font6)
        tlkNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tlkNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(tlkNameLabel, 1, 1)
        # tlkLabel
        tlkLabel = QLabel("{0}".format(speed[notchCnt + notchIndex]), font=font6)
        tlkLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        tlkLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(tlkLabel, 1, 2)
        # editTlkButton
        editTlkButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        editTlkButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        mainLayout.addWidget(editTlkButton, 1, 3)

        if self.notchContentCnt > 2:
            # try:
            #     color = ""
            #     if self.defaultData[self.cbIdx]["soundNum"][i] < speed[notchCnt * 2 + i]:
            #         color = "red"
            #     elif self.defaultData[self.cbIdx]["soundNum"][i] > speed[notchCnt * 2 + i]:
            #         color = "blue"
            #     else:
            #         color = "black"
            #     soundDefaultValue = self.defaultData[self.cbIdx]["soundNum"][i]
            # except Exception:
            #     color = "green"
            #     soundDefaultValue = None

            # soundNameLabel
            soundNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchSound"], font=font6)
            soundNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            soundNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(soundNameLabel, 2, 1)
            # soundLabel
            soundLabel = QLabel("{0}".format(speed[notchCnt*2 + notchIndex]), font=font6)
            soundLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            soundLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(soundLabel, 2, 2)
            # editSoundButton
            editSoundButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            editSoundButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            mainLayout.addWidget(editSoundButton, 2, 3)

            # try:
            #     color = ""
            #     if self.defaultData[self.cbIdx]["add"][i] < speed[notchCnt * 3 + i]:
            #         color = "red"
            #     elif self.defaultData[self.cbIdx]["add"][i] > speed[notchCnt * 3 + i]:
            #         color = "blue"
            #     else:
            #         color = "black"
            #     addDefaultValue = self.defaultData[self.cbIdx]["add"][i]
            # except Exception:
            #     color = "green"
            #     addDefaultValue = None

            # addNameLabel
            addNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["csvNotchAdd"], font=font6)
            addNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            addNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(addNameLabel, 3, 1)
            # addLabel
            addLabel = QLabel("{0}".format(speed[notchCnt*3 + notchIndex]), font=font6)
            addLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            addLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mainLayout.addWidget(addLabel, 3, 2)
            # editAddButton
            editAddButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            editAddButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            mainLayout.addWidget(editAddButton, 3, 3)

        # frame.grid_columnconfigure(0, weight=10)
        # frame.grid_columnconfigure(1, weight=1)
        # frame.grid_columnconfigure(2, weight=1)

    def editVar(self, labelList, var, value, notchName, notchNum, defaultValue, flag=False):
        EditNotchVarInfo(self.root, textSetting.textList["orgInfoEditor"]["valueModify"], labelList, var, value, notchName, notchNum, defaultValue, self.rootFrameAppearance, flag)


# class EditNotchVarInfo(CustomSimpleDialog):
#     def __init__(self, master, title, labelList, var, value, notchName, notchNum, defaultValue, rootFrameAppearance, flag=False):
#         self.labelList = labelList
#         self.master = master
#         self.var = var
#         self.value = value
#         self.notchName = notchName
#         self.notchNum = notchNum
#         self.defaultValue = defaultValue
#         self.flag = flag
#         super().__init__(master, title, rootFrameAppearance.bgColor)

#     def body(self, frame):
#         self.defaultLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["defaultValueLabel"] + str(self.defaultValue), font=textSetting.textList["font2"])
#         self.defaultLb.pack()

#         sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
#         sep.pack(fill=tkinter.X, ipady=5)

#         self.v_calcMinSpeed = tkinter.DoubleVar()
#         self.v_calcMinSpeed.set(0.0)
#         if self.notchName == "tlk":
#             calcMinSpeedLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["orgInfoEditor"]["calcMinSpeedLabel"].format(self.notchNum, self.notchNum + 1), font=textSetting.textList["font2"])
#             calcMinSpeedLb.pack()
#             calcMinSpeedValue = ttkCustomWidget.CustomTtkLabel(frame, textvariable=self.v_calcMinSpeed, font=textSetting.textList["font2"])
#             calcMinSpeedValue.pack()
#             sep = ttkCustomWidget.CustomTtkSeparator(frame, orient="horizontal")
#             sep.pack(fill=tkinter.X, ipady=5)

#         self.inputLb = ttkCustomWidget.CustomTtkLabel(frame, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"])
#         self.inputLb.pack()

#         self.v_val = tkinter.StringVar()
#         self.v_val.set(self.value)
#         self.inputEt = ttkCustomWidget.CustomTtkEntry(frame, textvariable=self.v_val, font=textSetting.textList["font2"])
#         self.inputEt.pack()
#         if self.notchName == "tlk":
#             self.inputEt.bind("<KeyRelease>", self.calcMinSpeedHandler)
#             self.calcMinSpeed()
#         super().body(frame)

#     def calcMinSpeedHandler(self, event):
#         self.calcMinSpeed()

#     def calcMinSpeed(self):
#         try:
#             inputTlk = float(self.v_val.get())
#         except Exception:
#             inputTlk = float(self.value)

#         notchPerfFrame = self.master.winfo_children()[1]
#         perfLabelFrame = notchPerfFrame.winfo_children()[1]
#         perfAllFrame = perfLabelFrame.winfo_children()[0]
#         perfCanvas = perfAllFrame.winfo_children()[1]
#         perfCanvasInFrame = perfCanvas.winfo_children()[0]

#         weightIdx = -1
#         noneTlkIdx = -1
#         perfWidgetList = perfCanvasInFrame.winfo_children()
#         for i in range(len(perfWidgetList) // 3):
#             nameLabel = perfWidgetList[3 * i]
#             if nameLabel["text"] == "Weight":
#                 weightIdx = i
#             if nameLabel["text"] == "None_Tlk":
#                 noneTlkIdx = i

#         weight = float(perfWidgetList[3 * weightIdx + 1]["text"])
#         noneTlk = float(perfWidgetList[3 * noneTlkIdx + 1]["text"])
#         minSpeed = ((weight - inputTlk) / noneTlk)
#         if minSpeed < 0:
#             minSpeed = 0
#         minSpeed = round(minSpeed * 60 / 1.11, 3)
#         self.v_calcMinSpeed.set(minSpeed)

#     def validate(self):
#         result = self.inputEt.get()
#         if result:
#             try:
#                 if self.flag:
#                     try:
#                         result = int(result)
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
