import os
import sys
from functools import partial

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import QTimer


def clearContainer(importDict):
    window = importDict["window"]

    if hasattr(window, 'container') and window.container:
        window.container.deleteLater()
    window.container = QWidget()
    window.setCentralWidget(window.container)


class MainWindow(QMainWindow):
    def __init__(self, importDict):
        super().__init__()

        self.version = mainProcess.getUpdateVer(importDict)
        self.checkConfig(importDict)
        self.drawMenu(importDict)

        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.checkUpdate(importDict)

    def checkConfig(self, importDict):
        configPath = importDict["configPath"]
        if not os.path.exists(configPath):
            mainProcess.writeDefaultConfig(importDict)

    def drawMenu(self, importDict):
        self.setWindowTitle(textSetting.textList["app"]["title"].format(self.version))
        self.resize(1024, 768)

        self.radio_group = QActionGroup(self)
        self.radio_group.setExclusive(True)

        menubar = self.menuBar()
        progmenu = menubar.addMenu(textSetting.textList["menu"]["program"]["name"])        

        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["SSUnity"], partial(mainProcess.callProgram, importDict, "SSUnity"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["orgInfoEditor"], partial(mainProcess.callProgram, importDict, "orgInfoEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlBin"], partial(mainProcess.callProgram, importDict, "mdlBin"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlinfo"], partial(mainProcess.callProgram, importDict, "mdlinfo"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["comicscript"], partial(mainProcess.callProgram, importDict, "comicscript"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["musicEditor"], partial(mainProcess.callProgram, importDict, "musicEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["fvtMaker"], partial(mainProcess.callProgram, importDict, "fvtMaker"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["railEditor"], partial(mainProcess.callProgram, importDict, "railEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["rsRail"], partial(mainProcess.callProgram, importDict, "rsRail"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["smf"], partial(mainProcess.callProgram, importDict, "smf"))
        progmenu.addSeparator()
        self.createDefaultAction(progmenu, textSetting.textList["menu"]["program"]["exit"], sys.exit)

        filemenu = menubar.addMenu(textSetting.textList["menu"]["file"]["name"])
        self.createDefaultAction(filemenu, textSetting.textList["menu"]["file"]["loadFile"], mainProcess.loadFile)

    def createRadioAction(self, menu, text, callback):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(callback)
        menu.addAction(action)
        self.radio_group.addAction(action)

    def createDefaultAction(self, menu, text, callback):
        action = QAction(text, self)
        action.triggered.connect(callback)
        menu.addAction(action)

    def checkUpdate(self, importDict):
        QTimer.singleShot(100, partial(mainProcess.confirmUpdate, self.version, importDict))


def guiMain(importDict):
    app = QApplication([])
    window = MainWindow(importDict)
    importDict["window"] = window
    window.show()
    sys.exit(app.exec())
