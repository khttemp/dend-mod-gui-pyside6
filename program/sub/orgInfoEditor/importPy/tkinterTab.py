import program.sub.textSetting as textSetting

from program.sub.orgInfoEditor.importPy.tab1.editOrgButtonWidget import EditOrgButtonWidget
from program.sub.orgInfoEditor.importPy.tab1.notchWidget import NotchWidget
from program.sub.orgInfoEditor.importPy.tab1.perfWidget import PerfWidget
from program.sub.orgInfoEditor.importPy.tab1.hurikoWidget import HurikoWidget
# from program.orgInfoEditor.importPy.tab1.tab1EditWidget import setDefault, extractCsvTrainInfo, saveCsvTrainInfo, editTrain, editAllTrain

# from program.orgInfoEditor.importPy.tab2.countWidget import CountWidget
# from program.orgInfoEditor.importPy.tab2.modelWidget import TrainModelWidget
# from program.orgInfoEditor.importPy.tab2.fixedListWidget import FixedListWidget
# from program.orgInfoEditor.importPy.tab2.fixedList2Widget import FixedList2Widget
# from program.orgInfoEditor.importPy.tab2.elsePerfWidget import ElsePerfWidget

# from program.orgInfoEditor.importPy.tab3.lensListWidget import LensListWidget
# from program.orgInfoEditor.importPy.tab3.tailListWidget import TailListWidget



from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGroupBox, QScrollArea, QFrame, QWidget
)
from PySide6.QtCore import Qt

defaultAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop

def tab1AllWidget(mainLayout, decryptFile, trainIndex, defaultData, reloadFunc):
    trainInfo = decryptFile.trainInfoList[trainIndex]
    if trainInfo is None:
        return
    selectDefaultData = defaultData[trainIndex]

    editOrgButtonWidget = EditOrgButtonWidget(decryptFile, reloadFunc)
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
    perfScrollArea.setWidget(perfContentFrame)

    # perfContentLayout
    perfContentLayout = QVBoxLayout()
    perfContentLayout.setContentsMargins(0, 0, 0, 0)
    perfContentLayout.setSpacing(0)
    perfContentFrame.setLayout(perfContentLayout)

    perf = trainInfo[1]
    perfCnt = len(perf)
    for i in range(perfCnt):
        perfWidget = PerfWidget(decryptFile, decryptFile.trainPerfNameList[i], perf[i], selectDefaultData)
        if decryptFile.trainPerfNameList[i] == "None_Tlk":
            perfWidget.setObjectName("NoneTlkWidget")
        elif decryptFile.trainPerfNameList[i] == "Weight":
            perfWidget.setObjectName("WeightWidget")
        perfContentLayout.addWidget(perfWidget)

    if decryptFile.game in ["CS", "RS"]:
        huriko = trainInfo[2]
        for i in range(len(huriko)):
            hurikoWidget = HurikoWidget(decryptFile, decryptFile.trainHurikoNameList[i], huriko[i], selectDefaultData)
            perfContentLayout.addWidget(hurikoWidget)
    perfContentLayout.addStretch()


def tab2AllWidget(mainLayout, decryptFile, trainIndex, defaultData, reloadFunc):
    pass
    # tab_two_frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    # tab_two_frame.pack(anchor=tkinter.NW, fill=tkinter.X)

    # if game in [gameDefine.LS, gameDefine.BS, gameDefine.CS, gameDefine.RS]:
    #     countModelLf = ttkCustomWidget.CustomTtkLabelFrame(tab_two_frame, text=textSetting.textList["orgInfoEditor"]["trainLfLabel"], height=250)
    #     countModelLf.pack(anchor=tkinter.NW, padx=10, pady=5, fill=tkinter.X)
    #     countModelLf.propagate(False)

    #     countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, rootFrameAppearance, reloadFunc)

    #     v_edit = widgetList[0]
    #     v_edit.set(textSetting.textList["orgInfoEditor"]["orgModify"])
    #     edit_hensei_button = ttkCustomWidget.CustomTtkButton(countWidget.countFrame, textvariable=v_edit)
    #     edit_hensei_button.grid(columnspan=3, row=3, column=0, sticky=tkinter.W + tkinter.E, pady=15)

    #     edit_model_button = ttkCustomWidget.CustomTtkButton(countWidget.countFrame, text=textSetting.textList["orgInfoEditor"]["modelInfoModify"])
    #     edit_model_button.grid(columnspan=3, row=4, column=0, sticky=tkinter.W + tkinter.E, pady=5)

    #     sep = ttkCustomWidget.CustomTtkSeparator(countModelLf, orient="vertical")
    #     sep.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=8)

    #     countModelScrollFrame = ScrollbarFrame(countModelLf, True, bgColor=rootFrameAppearance.bgColor)
    #     countModelScrollFrame.pack(expand=True, fill=tkinter.BOTH)

    #     innerButtonList = [
    #         countWidget.notchBtn,
    #         countWidget.henseiBtn,
    #         countWidget.colorBtn,
    #         edit_hensei_button,
    #         edit_model_button,
    #     ]

    #     TrainModelWidget(tabFrame, trainIdx, game, countModelScrollFrame.interior, widgetList, innerButtonList, decryptFile, rootFrameAppearance, reloadFunc)

    #     if game == gameDefine.LS:
    #         elseScrollFrame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    #         elseScrollFrame.pack(expand=True, fill=tkinter.BOTH)
    #         elseFrame = elseScrollFrame.interior

    #         elseFrame2 = elseFrame
    #     else:
    #         elseFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    #         elseFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

    #         elseFrame2 = ttkCustomWidget.CustomTtkFrame(tabFrame)
    #         elseFrame2.pack(anchor=tkinter.NW, fill=tkinter.X)

    #     elseModel = decryptFile.trainModelList[trainIdx]["elseModel"]
    #     else2Model = decryptFile.trainModelList[trainIdx]["else2Model"]

    #     if len(elseModel) > 0:
    #         FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else1", elseModel, 1, rootFrameAppearance, reloadFunc)
    #     FixedListWidget(elseFrame, game, trainIdx, decryptFile, "else2", else2Model, 2, rootFrameAppearance, reloadFunc)

    #     elseList2 = decryptFile.trainModelList[trainIdx]["elseList2"]
    #     FixedList2Widget(elseFrame2, trainIdx, decryptFile, "else3", elseList2, rootFrameAppearance, reloadFunc)
    # else:
    #     trainOrgInfo = decryptFile.trainInfoList[trainIdx]
    #     if trainOrgInfo is None:
    #         return

    #     mainFrame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    #     mainFrame.pack(fill=tkinter.BOTH, expand=True)
    #     scrollMainFrame = ScrollbarFrame(mainFrame, bgColor=rootFrameAppearance.bgColor)
    #     scrollMainFrame.pack(expand=True, fill=tkinter.BOTH)
    #     scrollFrame = scrollMainFrame.interior

    #     countModelLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSTrainLfLabel"])
    #     countModelLf.pack(anchor=tkinter.NW, padx=10, pady=3)

    #     countWidget = CountWidget(tabFrame, trainIdx, game, countModelLf, decryptFile, rootFrameAppearance, reloadFunc)

    #     sidePackFrame = ttkCustomWidget.CustomTtkFrame(scrollFrame)
    #     sidePackFrame.pack(anchor=tkinter.NW)
    #     rainPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSRainLfLabel"])
    #     rainPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, rainPerfLf, "rain", decryptFile.trainRainNameList, trainOrgInfo[2], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

    #     carbPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame, text=textSetting.textList["orgInfoEditor"]["SSCarbLfLabel"])
    #     carbPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, carbPerfLf, "carb", decryptFile.trainCarbNameList, trainOrgInfo[3], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

    #     otherPerfLf = ttkCustomWidget.CustomTtkLabelFrame(scrollFrame, text=textSetting.textList["orgInfoEditor"]["SSOtherLfLabel"])
    #     otherPerfLf.pack(anchor=tkinter.NW, padx=10, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, otherPerfLf, "other", decryptFile.trainOtherNameList, trainOrgInfo[4], True, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

    #     sidePackFrame2 = ttkCustomWidget.CustomTtkFrame(scrollFrame)
    #     sidePackFrame2.pack(anchor=tkinter.NW)
    #     hurikoPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSHurikoLfLabel"])
    #     hurikoPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, hurikoPerfLf, "huriko", decryptFile.trainHurikoNameList, trainOrgInfo[5], False, defaultData, decryptFile, rootFrameAppearance, reloadFunc)

    #     oneWheelPerfLf = ttkCustomWidget.CustomTtkLabelFrame(sidePackFrame2, text=textSetting.textList["orgInfoEditor"]["SSOneWheelLfLabel"])
    #     oneWheelPerfLf.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=8, pady=3)
    #     ElsePerfWidget(tabFrame, trainIdx, game, oneWheelPerfLf, "oneWheel", decryptFile.trainOneWheelNameList, trainOrgInfo[6], False, defaultData, decryptFile, rootFrameAppearance, reloadFunc)


def tab3AllWidget(mainLayout, decryptFile, trainIndex, reloadFunc):
    pass
    # tab3frame = ttkCustomWidget.CustomTtkFrame(tabFrame)
    # tab3frame.pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

    # lensList = decryptFile.trainModelList[trainIdx]["lensList"]
    # LensListWidget(tab3frame, decryptFile, trainIdx, lensList, rootFrameAppearance, reloadFunc)

    # tailList = decryptFile.trainModelList[trainIdx]["tailList"]
    # TailListWidget(tab3frame, decryptFile, trainIdx, tailList, rootFrameAppearance, reloadFunc)
