from functools import partial

import program.sub.textSetting as textSetting

from program.sub.orgInfoEditor.importPy.tab1.editOrgButtonWidget import EditOrgButtonWidget
from program.sub.orgInfoEditor.importPy.tab1.notchWidget import NotchWidget
from program.sub.orgInfoEditor.importPy.tab1.perfWidget import PerfWidget
from program.sub.orgInfoEditor.importPy.tab1.hurikoWidget import HurikoWidget

from program.sub.orgInfoEditor.importPy.tab2.notchCountWidget import NotchCountWidget
from program.sub.orgInfoEditor.importPy.tab2.countWidget import CountWidget
from program.sub.orgInfoEditor.importPy.tab2.trainModelWidget import TrainModelWidget
from program.sub.orgInfoEditor.importPy.tab2.editModelWidget import EditModelWidget
from program.sub.orgInfoEditor.importPy.tab2.fixedListWidget import FixedListWidget
from program.sub.orgInfoEditor.importPy.tab2.fixedList2Widget import FixedList2Widget
# from program.orgInfoEditor.importPy.tab2.elsePerfWidget import ElsePerfWidget

from program.sub.orgInfoEditor.importPy.tab3.lensListWidget import LensListWidget
from program.sub.orgInfoEditor.importPy.tab3.tailListWidget import TailListWidget



from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGroupBox, QScrollArea,
    QFrame, QWidget,
)
from PySide6.QtCore import Qt

defaultAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

def tab1AllWidget(mainLayout, decryptFile, trainIndex, defaultData, reloadWidget):
    trainInfo = decryptFile.trainInfoList[trainIndex]
    if trainInfo is None:
        return
    selectDefaultData = defaultData[trainIndex]

    editOrgButtonWidget = EditOrgButtonWidget(decryptFile, defaultData, reloadWidget)
    mainLayout.addWidget(editOrgButtonWidget, 1)

    contentWidget = QWidget()
    mainLayout.addWidget(contentWidget, 12)

    contentInLayout = QHBoxLayout()
    contentWidget.setLayout(contentInLayout)

    # contentLayout - speedGroupBox
    speedGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["speedLfLabel"])
    contentInLayout.addWidget(speedGroupBox, 2)
    # contentLayout - speedGroupBox - QVBoxLayout
    speedInLayout = QVBoxLayout()
    speedInLayout.setContentsMargins(0, 0, 0, 0)
    speedInLayout.setSpacing(0)
    speedGroupBox.setLayout(speedInLayout)
    # contentLayout - speedGroupBox - QVBoxLayout - QScrollArea
    speedScrollArea = QScrollArea()
    speedScrollArea.setWidgetResizable(True)
    speedInLayout.addWidget(speedScrollArea)
    # contentLayout - speedGroupBox - QVBoxLayout - QScrollArea - speedContentFrame
    speedContentFrame = QFrame()
    speedContentFrame.setObjectName("speedContentFrame")
    speedScrollArea.setWidget(speedContentFrame)

    # speedContentLayout
    speedContentLayout = QVBoxLayout()
    speedContentFrame.setLayout(speedContentLayout)

    speed = trainInfo[0]
    notchCnt = len(speed) // decryptFile.notchContentCnt
    for notchIndex in range(notchCnt):
        # speedContentLayout - NotchWidget
        notchWidget = NotchWidget(notchIndex, decryptFile, notchCnt, speed, selectDefaultData)
        speedContentLayout.addWidget(notchWidget)
    speedContentLayout.addStretch()

    # contentLayout - perfGroupBox
    perfGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["perfLfLabel"])
    contentInLayout.addWidget(perfGroupBox, 3)
    # contentLayout - perfGroupBox - QVBoxLayout
    perfInLayout = QVBoxLayout()
    perfInLayout.setContentsMargins(0, 0, 0, 0)
    perfInLayout.setSpacing(0)
    perfGroupBox.setLayout(perfInLayout)
    # contentLayout - perfGroupBox - QVBoxLayout - QScrollArea
    perfScrollArea = QScrollArea()
    perfScrollArea.setWidgetResizable(True)
    perfInLayout.addWidget(perfScrollArea)
    # contentLayout - perfGroupBox - QVBoxLayout - QScrollArea - perfContentFrame
    perfContentFrame = QFrame()
    perfContentFrame.setObjectName("perfContentFrame")
    perfScrollArea.setWidget(perfContentFrame)

    # perfContentLayout
    perfContentLayout = QVBoxLayout()
    perfContentLayout.setContentsMargins(0, 0, 0, 0)
    perfContentLayout.setSpacing(0)
    perfContentFrame.setLayout(perfContentLayout)

    perf = trainInfo[1]
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget = PerfWidget(decryptFile, decryptFile.trainPerfNameList[i], perf[i], selectDefaultData["att"][i])
        if decryptFile.trainPerfNameList[i] == "None_Tlk":
            perfWidget.setObjectName("NoneTlkWidget")
        elif decryptFile.trainPerfNameList[i] == "Weight":
            perfWidget.setObjectName("WeightWidget")
        perfContentLayout.addWidget(perfWidget)

    if decryptFile.game in ["CS", "RS"]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            hurikoWidget = HurikoWidget(decryptFile, decryptFile.trainHurikoNameList[i], huriko[i], selectDefaultData["huriko"][i])
            perfContentLayout.addWidget(hurikoWidget)
    perfContentLayout.addStretch()


def tab2AllWidget(mainLayout, decryptFile, trainIndex, defaultData, reloadWidget):
    contentWidget = QWidget()
    mainLayout.addWidget(contentWidget)

    contentInLayout = QVBoxLayout()
    contentInLayout.setContentsMargins(0, 0, 0, 0)
    contentInLayout.setSpacing(0)
    contentWidget.setLayout(contentInLayout)

    if decryptFile.game in ["RS", "CS", "BS", "LS"]:
        # trainGroupBox
        trainGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["trainLfLabel"])
        contentInLayout.addWidget(trainGroupBox, 2)
        # trainGroupBox - QHBoxLayout
        trainGroupInLayout = QHBoxLayout()
        trainGroupInLayout.setContentsMargins(0, 0, 0, 0)
        trainGroupInLayout.setSpacing(0)
        trainGroupBox.setLayout(trainGroupInLayout)
        # trainGroupBox - QHBoxLayout - QVBoxLayout
        countLayout = QVBoxLayout()
        countLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trainGroupInLayout.addLayout(countLayout, 2)
        # countLayout - NotchCountWidget
        index = decryptFile.indexList[trainIndex]
        notchNum = decryptFile.byteArr[index]
        notchCountWidget = NotchCountWidget(trainIndex, notchNum, decryptFile, reloadWidget)
        countLayout.addWidget(notchCountWidget)
        # countLayout - CountWidget
        countWidget = CountWidget(trainIndex, decryptFile, reloadWidget)
        countLayout.addWidget(countWidget)

        # trainGroupBox - QHBoxLayout - QFrame
        verticalLine = QFrame()
        verticalLine.setFrameShape(QFrame.Shape.VLine)
        verticalLine.setFrameShadow(QFrame.Shadow.Sunken)
        trainGroupInLayout.addWidget(verticalLine)
        # trainGroupBox - QHBoxLayout - scrollArea
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        trainGroupInLayout.addWidget(scrollArea, 5)
        # trainGroupBox - QHBoxLayout - scrollArea - QFrame
        scrollAreaFrame = QFrame()
        scrollArea.setWidget(scrollAreaFrame)
        # trainGroupBox - QHBoxLayout - scrollArea - QFrame - QVBoxLayout
        trainModelLayout = QVBoxLayout()
        scrollAreaFrame.setLayout(trainModelLayout)

        trainModelWidget = TrainModelWidget(trainIndex, decryptFile, reloadWidget)
        trainModelLayout.addWidget(trainModelWidget)
        # stretch
        trainModelLayout.addStretch()

        # countLayout - spacing
        countLayout.addSpacing(20)
        # countLayout - stackButton
        countLayout.addWidget(trainModelWidget.stackButton)

        editModelWidget = EditModelWidget(trainIndex, decryptFile, reloadWidget)
        # countLayout - spacing
        countLayout.addSpacing(15)
        # countLayout - editModelWidget.editModelButton
        countLayout.addWidget(editModelWidget)
        # countLayout - spacing
        countLayout.addSpacing(10)
        # stretch
        countLayout.addStretch()

        # contentInLayout - otherElementScrollArea
        otherElementScrollArea = QScrollArea()
        otherElementScrollArea.setWidgetResizable(True)
        contentInLayout.addWidget(otherElementScrollArea, 3)
        # contentInLayout - otherElementScrollArea - QFrame
        otherScrollAreaFrame = QFrame()
        otherElementScrollArea.setWidget(otherScrollAreaFrame)
        # contentInLayout - otherElementScrollArea - QFrame - QVBoxLayout
        otherElementLayout = QHBoxLayout()
        otherElementLayout.setContentsMargins(0, 0, 0, 0)
        otherElementLayout.setSpacing(0)
        otherScrollAreaFrame.setLayout(otherElementLayout)

        elseModel = decryptFile.trainModelList[trainIndex]["elseModel"]
        else2Model = decryptFile.trainModelList[trainIndex]["else2Model"]
        elseList2 = decryptFile.trainModelList[trainIndex]["elseList2"]

        if len(elseModel) > 0:
            elseModelFixedListWidget = FixedListWidget(trainIndex, decryptFile, "else1", elseModel, 1, reloadWidget)
            otherElementLayout.addWidget(elseModelFixedListWidget, alignment=defaultAlignment)
        else2ModelFixedListWidget = FixedListWidget(trainIndex, decryptFile, "else2", else2Model, 2, reloadWidget)
        otherElementLayout.addWidget(else2ModelFixedListWidget, alignment=defaultAlignment)
        # elseList2
        fixedList2Widget = FixedList2Widget(trainIndex, decryptFile, "else3", elseList2, reloadWidget)
        otherElementLayout.addWidget(fixedList2Widget, alignment=defaultAlignment)
        # stretch
        otherElementLayout.addStretch()
    else:
        trainOrgInfo = decryptFile.trainInfoList[trainIndex]
        if trainOrgInfo is None:
            return
        # scrollArea
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(scrollArea)
        # scrollArea - QFrame
        scrollAreaFrame = QFrame()
        scrollArea.setWidget(scrollAreaFrame)
        # scrollArea - QFrame - QVBoxLayout
        contentLayout = QVBoxLayout()
        scrollAreaFrame.setLayout(contentLayout)

        # trainGroupBox
        trainGroupBox = QGroupBox(textSetting.textList["orgInfoEditor"]["trainLfLabel"])
        contentLayout.addWidget(trainGroupBox, alignment=defaultAlignment)
        # trainGroupBox - QVBoxLayout
        trainLayout = QVBoxLayout()
        trainLayout.setContentsMargins(0, 0, 0, 0)
        trainLayout.setSpacing(0)
        trainGroupBox.setLayout(trainLayout)
        # trainGroupBox - QVBoxLayout - NotchCountWidget
        trainOrgInfo = decryptFile.trainInfoList[trainIndex]
        speedList = trainOrgInfo[0]
        notchNum = len(speedList) // decryptFile.notchContentCnt
        notchCountWidget = NotchCountWidget(trainIndex, notchNum, decryptFile, reloadWidget)
        trainLayout.addWidget(notchCountWidget)

    #     rainPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
    #     rainPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, rainPerfLf, "rain", decryptFile.trainRainNameList, trainOrgInfo[2], True, defaultData, decryptFile, rootFrameAppearance, reloadWidget)

    #     carbPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
    #     carbPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, carbPerfLf, "carb", decryptFile.trainCarbNameList, trainOrgInfo[3], True, defaultData, decryptFile, rootFrameAppearance, reloadWidget)

    #     otherPerfLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
    #     otherPerfLf.pack(anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, otherPerfLf, "other", decryptFile.trainOtherNameList, trainOrgInfo[4], True, defaultData, decryptFile, rootFrameAppearance, reloadWidget)

    #     sidePackFrame2 = ttkCustomWidget.CustomTtkFrame(scrollFrame)
    #     sidePackFrame2.pack(anchor=tkinter.NW)
    #     hurikoPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
    #     hurikoPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, hurikoPerfLf, "huriko", decryptFile.trainHurikoNameList, trainOrgInfo[5], False, defaultData, decryptFile, rootFrameAppearance, reloadWidget)

    #     oneWheelPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
    #     oneWheelPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, oneWheelPerfLf, "oneWheel", decryptFile.trainOneWheelNameList, trainOrgInfo[6], False, defaultData, decryptFile, rootFrameAppearance, reloadWidget)


def tab3AllWidget(mainLayout, decryptFile, trainIndex, reloadWidget):
    contentWidget = QWidget()
    mainLayout.addWidget(contentWidget)

    contentInLayout = QVBoxLayout()
    contentInLayout.setContentsMargins(0, 0, 0, 0)
    contentInLayout.setSpacing(0)
    contentWidget.setLayout(contentInLayout)

    lensList = decryptFile.trainModelList[trainIndex]["lensList"]
    lensListWidget = LensListWidget(decryptFile, trainIndex, lensList, reloadWidget)
    contentInLayout.addWidget(lensListWidget, 1)

    tailList = decryptFile.trainModelList[trainIndex]["tailList"]
    tailListWidget = TailListWidget(decryptFile, trainIndex, tailList, reloadWidget)
    contentInLayout.addWidget(tailListWidget, 1)
