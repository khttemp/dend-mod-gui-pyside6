from functools import partial

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea,
    QFrame, QGridLayout, QLabel,
    QPushButton, QDialog, QLineEdit, QDialogButtonBox, QSizePolicy
)
from PySide6.QtGui import QFont, QPalette, QColor, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class LensListWidget(QWidget):
    def __init__(self, decryptFile, trainIndex, lensList, reloadWidget):
        super().__init__()
        self.decryptFile = decryptFile
        self.trainIndex = trainIndex
        self.lensList = lensList
        self.reloadWidget = reloadWidget
        fixedWidth = 86
        fixedHeight = 36
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        # mainLayout - lensListGroupBox
        lensListGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["lensInfoLabel"])
        mainLayout.addWidget(lensListGroupBox)
        # groupInLayout
        groupInLayout = QVBoxLayout()
        groupInLayout.setContentsMargins(0, 0, 0, 0)
        groupInLayout.setSpacing(0)
        lensListGroupBox.setLayout(groupInLayout)
        # groupInLayout - scrollArea
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        groupInLayout.addWidget(scrollArea)
        # groupInLayout - scrollArea - QFrame
        scrollAreaFrame = QFrame()
        scrollArea.setWidget(scrollAreaFrame)
        # groupInLayout - scrollArea - QFrame - QVBoxLayout
        contentLayout = QVBoxLayout()
        scrollAreaFrame.setLayout(contentLayout)

        # lensCountLayout
        lensCountLayout = QHBoxLayout()
        contentLayout.addLayout(lensCountLayout)
        # lensCountGridLayout
        lensCountGridLayout = QGridLayout()
        lensCountGridLayout.setContentsMargins(0, 0, 0, 0)
        lensCountGridLayout.setSpacing(0)
        lensCountLayout.addLayout(lensCountGridLayout)
        # lensCountGridLayout - lensCountNameLabel
        lensCountNameLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensCntLabel"], font=font6)
        lensCountNameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        lensCountNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lensCountGridLayout.addWidget(lensCountNameLabel, 0, 0)
        # lensCountLabel
        lensCountLabel = QLabel("{0}".format(len(self.lensList)), font=font6)
        lensCountLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        lensCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lensCountLabel.setFixedWidth(fixedWidth)
        lensCountGridLayout.addWidget(lensCountLabel, 0, 1)
        # lensCountButton
        lensCountButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
        lensCountGridLayout.addWidget(lensCountButton, 0, 2)
        # stretch
        lensCountLayout.addStretch()

        for i in range(len(self.lensList)):
            # contentLayout - lensElementLayout
            lensElementLayout = QHBoxLayout()
            contentLayout.addLayout(lensElementLayout)
            # contentLayout - lensElementLayout - buttonLayout
            buttonLayout = QVBoxLayout()
            lensElementLayout.addLayout(buttonLayout)
            # contentLayout - lensElementLayout - buttonLayout - lensElementButton
            lensElementButton = QPushButton(textSetting.textList["orgInfoEditor"]["modifyBtnLabel"], font=font6)
            buttonLayout.addWidget(lensElementButton)
            # stretch
            buttonLayout.addStretch()

            # contentLayout - lensElementLayout - lensInfoLayout
            lensInfoLayout = QVBoxLayout()
            lensInfoLayout.setContentsMargins(0, 0, 0, 0)
            lensInfoLayout.setSpacing(0)
            lensElementLayout.addLayout(lensInfoLayout)
            # lensInfoLayout - nameLayout
            nameLayout = QHBoxLayout()
            lensInfoLayout.addLayout(nameLayout)
            # lensInfoLayout - nameLayout - nameInfoGridLayout
            nameInfoGridLayout = QGridLayout()
            nameInfoGridLayout.setContentsMargins(0, 0, 0, 0)
            nameInfoGridLayout.setSpacing(0)
            nameLayout.addLayout(nameInfoGridLayout)
            # nameTextLabel
            nameTextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensNameLabel"], font=font6)
            nameTextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            nameTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nameTextLabel.setFixedSize(fixedWidth, fixedHeight)
            nameInfoGridLayout.addWidget(nameTextLabel, 0, 0)
            for j in range(2):
                # nameLabel
                nameLabel = QLabel("{0}".format(self.lensList[i][j]), font=font6)
                nameLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                nameLabel.setFixedHeight(fixedHeight)
                nameInfoGridLayout.addWidget(nameLabel, 0, j + 1)
            # stretch
            nameLayout.addStretch()

            # elementLayout
            elementLayout = QHBoxLayout()
            lensInfoLayout.addLayout(elementLayout)
            # elementGridLayout
            elementGridLayout = QGridLayout()
            elementGridLayout.setContentsMargins(0, 0, 0, 0)
            elementGridLayout.setSpacing(0)
            elementLayout.addLayout(elementGridLayout)

            # fTextLabel
            f1TextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensF1Label"], font=font6)
            f1TextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            f1TextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f1TextLabel.setFixedSize(fixedWidth, fixedHeight)
            elementGridLayout.addWidget(f1TextLabel, 0, 0)
            for j in range(2):
                # fLabel
                fLabel = QLabel("{0}".format(self.lensList[i][j + 2]), font=font6)
                fLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                fLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                fLabel.setFixedSize(fixedWidth, fixedHeight)
                elementGridLayout.addWidget(fLabel, 0, j + 1)

            # bTestLabel
            b1TextLabel = QLabel(textSetting.textList["orgInfoEditor"]["lensB1Label"], font=font6)
            b1TextLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            b1TextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b1TextLabel.setFixedSize(fixedWidth, fixedHeight)
            elementGridLayout.addWidget(b1TextLabel, 1, 0)
            for j in range(len(self.lensList[i][4])):
                # bLabel
                bLabel = QLabel("{0}".format(self.lensList[i][4][j]), font=font6)
                bLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                bLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                bLabel.setFixedSize(fixedWidth, fixedHeight)
                elementGridLayout.addWidget(bLabel, 1, j + 1)

            # stretch
            elementLayout.addStretch()
            # stretch
            lensInfoLayout.addStretch()
            # stretch
            lensElementLayout.addStretch()
        # stretch
        contentLayout.addStretch()

    def editLensCnt(self, val):
        result = EditLensCntWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditCntLabel"], self.decryptFile, val, self.rootFrameAppearance)
        if result.reloadFlag:
            if not self.decryptFile.saveLensCnt(self.trainIdx, result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I65"])
            self.reloadFunc()

    def editLensList(self, i, valList):
        result = EditLensWidget(self.frame, textSetting.textList["orgInfoEditor"]["lensEditLabel"], self.decryptFile, valList, self.rootFrameAppearance)
        if result.reloadFlag:
            self.lensList[i] = result.resultValueList
            if not self.decryptFile.saveLensList(self.trainIdx, self.lensList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E14"])
                return
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I66"])
            self.reloadFunc()


# class EditLensCntWidget(CustomSimpleDialog):
#     def __init__(self, master, title, decryptFile, val, rootFrameAppearance):
#         self.decryptFile = decryptFile
#         self.val = val
#         self.resultValue = 0
#         self.reloadFlag = False
#         super().__init__(master, title, rootFrameAppearance.bgColor)

#     def body(self, master):
#         self.resizable(False, False)

#         self.valLb = ttkCustomWidget.CustomTtkLabel(master, text=textSetting.textList["infoList"]["I44"], font=textSetting.textList["font2"], anchor=tkinter.CENTER)
#         self.valLb.pack()

#         self.varLensCnt = tkinter.IntVar()
#         self.varLensCnt.set(self.val)
#         self.valEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varLensCnt, font=textSetting.textList["font2"], width=16)
#         self.valEt.pack()
#         super().body(master)

#     def validate(self):
#         result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)

#         if result:
#             try:
#                 try:
#                     res = int(self.varLensCnt.get())
#                     if res <= 0:
#                         errorMsg = textSetting.textList["errorList"]["E61"].format(1)
#                         mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
#                         return False
#                     self.resultValue = res
#                 except Exception:
#                     errorMsg = textSetting.textList["errorList"]["E60"]
#                     mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
#             except Exception:
#                 errorMsg = textSetting.textList["errorList"]["E14"]
#                 mb.showerror(title=textSetting.textList["error"], message=errorMsg)

#             if self.resultValue < self.val:
#                 msg = textSetting.textList["infoList"]["I20"] + textSetting.textList["infoList"]["I21"]
#                 result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning", parent=self)
#                 if result:
#                     return True
#             else:
#                 return True

#     def apply(self):
#         self.reloadFlag = True


# class EditLensWidget(CustomSimpleDialog):
#     def __init__(self, master, title, decryptFile, lensInfo, rootFrameAppearance):
#         self.decryptFile = decryptFile
#         self.lensInfo = lensInfo
#         self.varList = []
#         self.varCnt = 0
#         self.resultValueList = []
#         self.reloadFlag = False
#         super().__init__(master, title, rootFrameAppearance.bgColor)

#     def body(self, master):
#         self.resizable(False, False)

#         lensInfoLbList = textSetting.textList["orgInfoEditor"]["lensInfoLabelList"]
#         for i in range(len(self.lensInfo)):
#             if i in [0, 1]:
#                 self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
#                 self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
#                 self.varList.append(tkinter.StringVar(value=self.lensInfo[i]))
#                 self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
#                 self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
#                 self.varCnt += 1
#             elif i in [2, 3]:
#                 self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i], font=textSetting.textList["font2"])
#                 self.lensLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
#                 self.varList.append(tkinter.DoubleVar(value=round(float(self.lensInfo[i]), 3)))
#                 self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=self.varList[self.varCnt], font=textSetting.textList["font2"])
#                 self.lensEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
#                 self.varCnt += 1
#             elif i == 4:
#                 varList = []
#                 for j in range(len(self.lensInfo[i])):
#                     self.lensLb = ttkCustomWidget.CustomTtkLabel(master, text=lensInfoLbList[i + j], font=textSetting.textList["font2"])
#                     self.lensLb.grid(row=i + j, column=0, sticky=tkinter.W + tkinter.E)
#                     varList.append(tkinter.IntVar(value=self.lensInfo[i][j]))
#                     self.lensEt = ttkCustomWidget.CustomTtkEntry(master, textvariable=varList[j], font=textSetting.textList["font2"])
#                     self.lensEt.grid(row=i + j, column=1, sticky=tkinter.W + tkinter.E)
#                     self.varCnt += 1
#                 self.varList.append(varList)
#         super().body(master)

#     def validate(self):
#         self.resultValueList = []
#         result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"], parent=self)
#         if result:
#             try:
#                 try:
#                     for i in range(len(self.varList)):
#                         if i in [0, 1]:
#                             res = self.varList[i].get()
#                         elif i in [2, 3]:
#                             res = float(self.varList[i].get())
#                         elif i == 4:
#                             res = []
#                             varList = self.varList[i]
#                             for j in range(len(varList)):
#                                 var = int(varList[j].get())
#                                 res.append(var)
#                         self.resultValueList.append(res)
#                     return True
#                 except Exception:
#                     errorMsg = textSetting.textList["errorList"]["E3"]
#                     mb.showerror(title=textSetting.textList["numberError"], message=errorMsg)
#             except Exception:
#                 errorMsg = textSetting.textList["errorList"]["E14"]
#                 mb.showerror(title=textSetting.textList["error"], message=errorMsg)

#     def apply(self):
#         self.reloadFlag = True
