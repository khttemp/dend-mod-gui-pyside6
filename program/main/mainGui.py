import os
import sys
from functools import partial

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting

import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
import program.sub.ssUnity.ssUnityGui as ssUnityGui

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import QTimer

mb = customMessageBoxWidget.CustomMessageBox()


class MainWindow(QMainWindow):
    def __init__(self, importDict):
        super().__init__()

        self.selectedProgram = None
        self.version = mainProcess.getUpdateVer(importDict)
        self.checkConfig(importDict)
        self.drawMenu(importDict)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

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

        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["SSUnity"], partial(self.callProgram, "SSUnity"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["orgInfoEditor"], partial(self.callProgram, "orgInfoEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlBin"], partial(self.callProgram, "mdlBin"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlinfo"], partial(self.callProgram, "mdlinfo"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["comicscript"], partial(self.callProgram, "comicscript"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["musicEditor"], partial(self.callProgram, "musicEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["fvtMaker"], partial(self.callProgram, "fvtMaker"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["railEditor"], partial(self.callProgram, "railEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["rsRail"], partial(self.callProgram, "rsRail"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["smf"], partial(self.callProgram, "smf"))
        progmenu.addSeparator()
        self.createDefaultAction(progmenu, textSetting.textList["menu"]["program"]["exit"], sys.exit)

        filemenu = menubar.addMenu(textSetting.textList["menu"]["file"]["name"])
        self.createDefaultAction(filemenu, textSetting.textList["menu"]["file"]["loadFile"], self.loadFile)

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

    def clearContainer(self):
        currentWidget = self.stack.currentWidget()
        if currentWidget:
            self.stack.removeWidget(currentWidget)
            currentWidget.deleteLater()

    def callProgram(self, programName):
        self.clearContainer()

        self.selectedProgram = programName
        newWidget = None
        if self.selectedProgram == "SSUnity":
            newWidget = ssUnityGui.SSUnityWindow()

        if newWidget is None:
            return
        self.stack.addWidget(newWidget)
        self.stack.setCurrentWidget(newWidget)

    def loadFile(self):
        if self.selectedProgram is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E1"])
            return


def guiMain(importDict):
    app = QApplication([])
    window = MainWindow(importDict)
    importDict["window"] = window
    window.show()
    sys.exit(app.exec())
