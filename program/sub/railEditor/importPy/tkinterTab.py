
import program.sub.textSetting as textSetting

from program.sub.railEditor.importPy.tab1.musicWidget import MusicWidget
from program.sub.railEditor.importPy.tab1.trainCountWidget import TrainCountWidget
from program.sub.railEditor.importPy.tab1.railPosWidget import RailPosWidget
from program.sub.railEditor.importPy.tab1.stationNoWidget import StationNoWidget

from program.sub.railEditor.importPy.tab2.else1ListWidget import Else1ListWidget
# from program.railEditor.importPy.tab2.simpleListWidget import SimpleListWidget
# from program.railEditor.importPy.tab2.stationWidget import StationWidget
# from program.railEditor.importPy.tab2.binAnimeListWidget import BinAnimeListWidget

# from program.railEditor.importPy.tab3.smfListWidget import SmfListWidget

# from program.railEditor.importPy.tab4.stationNameWidget import StationNameWidget

# from program.railEditor.importPy.tab5.else2ListWidget import Else2ListWidget

# from program.railEditor.importPy.tab6.cpuWidget import CpuWidget

# from program.railEditor.importPy.tab7.comicScriptWidget import ComicScriptWidget
# from program.railEditor.importPy.tab7.dosansenListWidget import DosansenListWidget

# from program.railEditor.importPy.tab8.railListWidget import RailListWidget

# from program.railEditor.importPy.tab9.else3ListWidget import Else3ListWidget

# from program.railEditor.importPy.tab10.else4ListWidget import Else4ListWidget

# from program.railEditor.importPy.tab11.ambListWidget import AmbListWidget

from PySide6.QtWidgets import (
    QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt


def tab1AllWidget(contentFrame, decryptFile, reloadFunc):
    tab1Layout = QVBoxLayout()
    tab1Layout.setContentsMargins(0, 0, 0, 0)
    tab1Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    contentFrame.setLayout(tab1Layout)

    musicWidget = MusicWidget(decryptFile, reloadFunc)
    tab1Layout.addWidget(musicWidget)
    trainCountWidget = TrainCountWidget(decryptFile, reloadFunc)
    tab1Layout.addWidget(trainCountWidget)
    railPosWidget = RailPosWidget(textSetting.textList["railEditor"]["initPos"], 0, decryptFile, decryptFile.trainList, reloadFunc)
    tab1Layout.addWidget(railPosWidget)

    if decryptFile.game in ["BS", "CS", "RS"]:
        railPos2Widget = RailPosWidget(textSetting.textList["railEditor"]["dummyPos"], 1, decryptFile, decryptFile.trainList2, reloadFunc)
        tab1Layout.addWidget(railPos2Widget)
        railPos3Widget = RailPosWidget(textSetting.textList["railEditor"]["pracOrVsPos"], 2, decryptFile, decryptFile.trainList3, reloadFunc)
        tab1Layout.addWidget(railPos3Widget)
        stationNoWidget = StationNoWidget(0, decryptFile, decryptFile.stationNo, reloadFunc)
        tab1Layout.addWidget(stationNoWidget)

        if decryptFile.game == "BS":
            horizentalLine = QFrame()
            horizentalLine.setFrameShape(QFrame.Shape.HLine)
            horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
            tab1Layout.addWidget(horizentalLine)

            railPos4Widget = RailPosWidget(textSetting.textList["railEditor"]["dummyPos"], 3, decryptFile, decryptFile.trainList4, reloadFunc)
            tab1Layout.addWidget(railPos4Widget)
            stationNo2Widget = StationNoWidget(1, decryptFile, decryptFile.stationNo2, reloadFunc)
            tab1Layout.addWidget(stationNo2Widget)


def tab2AllWidget(contentFrame, decryptFile, reloadFunc):
    tab2Layout = QVBoxLayout()
    tab2Layout.setContentsMargins(0, 0, 0, 0)
    tab2Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    contentFrame.setLayout(tab2Layout)

    else1ListWidget = Else1ListWidget(decryptFile, reloadFunc)
    tab2Layout.addWidget(else1ListWidget)
    # if decryptFile.game in ["BS", "CS", "RS"]:
    #     simpleListFrame = ttkCustomWidget.CustomTtkFrame(frame.interior)
    #     simpleListFrame.pack(anchor=tkinter.NW)
    #     SimpleListWidget(root, simpleListFrame, textSetting.textList["railEditor"]["lightInfo"], decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, rootFrameAppearance, reloadFunc)
    #     if decryptFile.game in ["CS", "RS"]:
    #         SimpleListWidget(root, simpleListFrame, textSetting.textList["railEditor"]["stationInfo"], decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, rootFrameAppearance, reloadFunc)
    #         StationWidget(root, frame.interior, decryptFile, decryptFile.stationList, rootFrameAppearance, reloadFunc)

    # simpleListFrame2 = ttkCustomWidget.CustomTtkFrame(frame.interior)
    # simpleListFrame2.pack(anchor=tkinter.NW)
    # if decryptFile.game in ["BS", "CS", "RS"]:
    #     SimpleListWidget(root, simpleListFrame2, textSetting.textList["railEditor"]["baseBinInfo"], decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, rootFrameAppearance, reloadFunc)
    # BinAnimeListWidget(root, simpleListFrame2, decryptFile, decryptFile.binAnimeList, rootFrameAppearance, reloadFunc)


def tab3AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    SmfListWidget(root, tabFrame, decryptFile, decryptFile.smfList, rootFrameAppearance, reloadFunc, selectId)


def tab4AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    StationNameWidget(root, tabFrame, decryptFile, decryptFile.stationNameList, rootFrameAppearance, reloadFunc, selectId)


def tab5AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else2ListWidget(root, tabFrame, decryptFile, decryptFile.else2List, rootFrameAppearance, reloadFunc)


def tab6AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    CpuWidget(root, tabFrame, decryptFile, decryptFile.cpuList, rootFrameAppearance, reloadFunc, selectId)


def tab7AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    ComicScriptWidget(root, tabFrame, decryptFile, decryptFile.comicScriptList, rootFrameAppearance, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        DosansenListWidget(root, tabFrame, decryptFile, decryptFile.dosansenList, rootFrameAppearance, reloadFunc)


def tab8AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, True, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    RailListWidget(frame.interior, decryptFile, decryptFile.railList, rootFrameAppearance, reloadFunc)


def tab9AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc, selectId):
    Else3ListWidget(root, tabFrame, decryptFile, decryptFile.else3List, rootFrameAppearance, reloadFunc, selectId)


def tab10AllWidget(root, tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    Else4ListWidget(root, tabFrame, decryptFile, decryptFile.else4List, rootFrameAppearance, reloadFunc)


def tab11AllWidget(tabFrame, decryptFile, rootFrameAppearance, reloadFunc):
    frame = ScrollbarFrame(tabFrame, bgColor=rootFrameAppearance.bgColor)
    frame.pack(expand=True, fill=tkinter.BOTH)
    AmbListWidget(frame.interior, decryptFile, decryptFile.ambList, rootFrameAppearance, reloadFunc)
