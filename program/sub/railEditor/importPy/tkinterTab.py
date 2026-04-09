
import program.sub.textSetting as textSetting

from program.sub.railEditor.importPy.tab1.musicWidget import MusicWidget
from program.sub.railEditor.importPy.tab1.trainCountWidget import TrainCountWidget
from program.sub.railEditor.importPy.tab1.railPosWidget import RailPosWidget
from program.sub.railEditor.importPy.tab1.stationNoWidget import StationNoWidget

from program.sub.railEditor.importPy.tab2.else1ListWidget import Else1ListWidget
from program.sub.railEditor.importPy.tab2.simpleListWidget import SimpleListWidget
from program.sub.railEditor.importPy.tab2.stationAmbWidget import StationAmbWidget
from program.sub.railEditor.importPy.tab2.binAnimeListWidget import BinAnimeListWidget

from program.sub.railEditor.importPy.tab3.smfListWidget import SmfListWidget

from program.sub.railEditor.importPy.tab4.stationNameWidget import StationNameWidget

from program.sub.railEditor.importPy.tab5.else2ListWidget import Else2ListWidget

# from program.railEditor.importPy.tab6.cpuWidget import CpuWidget

# from program.railEditor.importPy.tab7.comicScriptWidget import ComicScriptWidget
# from program.railEditor.importPy.tab7.dosansenListWidget import DosansenListWidget

# from program.railEditor.importPy.tab8.railListWidget import RailListWidget

# from program.railEditor.importPy.tab9.else3ListWidget import Else3ListWidget

# from program.railEditor.importPy.tab10.else4ListWidget import Else4ListWidget

# from program.railEditor.importPy.tab11.ambListWidget import AmbListWidget

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

defaultAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop


def tab1AllWidget(contentFrame, decryptFile, reloadFunc):
    tab1Layout = QVBoxLayout()
    tab1Layout.setContentsMargins(0, 0, 0, 0)
    tab1Layout.setAlignment(defaultAlignment)
    contentFrame.setLayout(tab1Layout)

    musicWidget = MusicWidget(decryptFile, reloadFunc)
    tab1Layout.addWidget(musicWidget, alignment=defaultAlignment)
    trainCountWidget = TrainCountWidget(decryptFile, reloadFunc)
    tab1Layout.addWidget(trainCountWidget, alignment=defaultAlignment)
    railPosWidget = RailPosWidget(textSetting.textList["railEditor"]["initPos"], 0, decryptFile, decryptFile.trainList, reloadFunc)
    tab1Layout.addWidget(railPosWidget, alignment=defaultAlignment)

    if decryptFile.game in ["BS", "CS", "RS"]:
        railPos2Widget = RailPosWidget(textSetting.textList["railEditor"]["dummyPos"], 1, decryptFile, decryptFile.trainList2, reloadFunc)
        tab1Layout.addWidget(railPos2Widget, alignment=defaultAlignment)
        railPos3Widget = RailPosWidget(textSetting.textList["railEditor"]["pracOrVsPos"], 2, decryptFile, decryptFile.trainList3, reloadFunc)
        tab1Layout.addWidget(railPos3Widget, alignment=defaultAlignment)
        stationNoWidget = StationNoWidget(0, decryptFile, decryptFile.stationNo, reloadFunc)
        tab1Layout.addWidget(stationNoWidget, alignment=defaultAlignment)

        if decryptFile.game == "BS":
            horizentalLine = QFrame()
            horizentalLine.setFrameShape(QFrame.Shape.HLine)
            horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
            tab1Layout.addWidget(horizentalLine)

            railPos4Widget = RailPosWidget(textSetting.textList["railEditor"]["dummyPos"], 3, decryptFile, decryptFile.trainList4, reloadFunc)
            tab1Layout.addWidget(railPos4Widget, alignment=defaultAlignment)
            stationNo2Widget = StationNoWidget(1, decryptFile, decryptFile.stationNo2, reloadFunc)
            tab1Layout.addWidget(stationNo2Widget, alignment=defaultAlignment)


def tab2AllWidget(contentFrame, decryptFile, reloadFunc):
    tab2Layout = QVBoxLayout()
    tab2Layout.setContentsMargins(0, 0, 0, 0)
    tab2Layout.setAlignment(defaultAlignment)
    contentFrame.setLayout(tab2Layout)

    else1ListWidget = Else1ListWidget(decryptFile, reloadFunc)
    tab2Layout.addWidget(else1ListWidget, alignment=defaultAlignment)
    if decryptFile.game in ["BS", "CS", "RS"]:
        simpleListLayout = QHBoxLayout()
        simpleListLayout.setAlignment(defaultAlignment)
        tab2Layout.addLayout(simpleListLayout)
        lightListWidget = SimpleListWidget(textSetting.textList["railEditor"]["lightInfo"], decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, reloadFunc)
        simpleListLayout.addWidget(lightListWidget, alignment=defaultAlignment)
        if decryptFile.game in ["CS", "RS"]:
            pngListWidget = SimpleListWidget(textSetting.textList["railEditor"]["stationInfo"], decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, reloadFunc)
            simpleListLayout.addWidget(pngListWidget, alignment=defaultAlignment)
            stationAmbWidget = StationAmbWidget(decryptFile, reloadFunc)
            tab2Layout.addWidget(stationAmbWidget, alignment=defaultAlignment)

    simpleListLayout2 = QHBoxLayout()
    simpleListLayout2.setAlignment(defaultAlignment)
    tab2Layout.addLayout(simpleListLayout2)
    if decryptFile.game in ["BS", "CS", "RS"]:
        baseBinListWidget = SimpleListWidget(textSetting.textList["railEditor"]["baseBinInfo"], decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, reloadFunc)
        simpleListLayout2.addWidget(baseBinListWidget, alignment=defaultAlignment)
    binAnimeListWidget = BinAnimeListWidget(decryptFile, reloadFunc)
    simpleListLayout2.addWidget(binAnimeListWidget, alignment=defaultAlignment)


def tab3AllWidget(contentFrame, decryptFile, reloadFunc, selectId):
    tab3Layout = QVBoxLayout()
    tab3Layout.setContentsMargins(0, 0, 0, 0)
    contentFrame.setLayout(tab3Layout)

    smfListWidget = SmfListWidget(decryptFile, reloadFunc, selectId)
    tab3Layout.addWidget(smfListWidget)


def tab4AllWidget(contentFrame, decryptFile, reloadFunc, selectId):
    tab4Layout = QVBoxLayout()
    tab4Layout.setContentsMargins(0, 0, 0, 0)
    contentFrame.setLayout(tab4Layout)

    stationNameWidget = StationNameWidget(decryptFile, reloadFunc, selectId)
    tab4Layout.addWidget(stationNameWidget)


def tab5AllWidget(contentFrame, decryptFile, reloadFunc):
    tab5Layout = QVBoxLayout()
    tab5Layout.setContentsMargins(0, 0, 0, 0)
    contentFrame.setLayout(tab5Layout)

    else2ListWidget = Else2ListWidget(decryptFile, reloadFunc)
    tab5Layout.addWidget(else2ListWidget, alignment=defaultAlignment)


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
