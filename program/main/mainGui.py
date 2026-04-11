import os
import sys
from functools import partial

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting

import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget
import program.sub.ssUnity.ssUnityGui as ssUnityGui
import program.sub.railEditor.railEditorGui as railEditorGui

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMenu
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import QTimer

mb = customMessageBoxWidget.CustomMessageBox()


class MainWindow(QMainWindow):
    def __init__(self, importDict):
        super().__init__()
        self.importDict = importDict

        self.selectedProgram = None
        self.version = mainProcess.getUpdateVer(self.importDict["rootPath"])
        self.onlineVersion = mainProcess.getOnlineUpdateVer(self.importDict["configPath"])
        self.checkConfig()
        self.drawMenu()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        QTimer.singleShot(100, self.checkUpdate)

    def checkConfig(self):
        configPath = self.importDict["configPath"]
        if not os.path.exists(configPath):
            mainProcess.writeDefaultConfig(configPath)

    def drawMenu(self):
        self.setWindowTitle(textSetting.textList["app"]["title"].format(self.version))
        self.resize(1024, 768)

        self.radio_group = QActionGroup(self)
        self.radio_group.setExclusive(True)

        menubar = self.menuBar()
        progmenu = menubar.addMenu(textSetting.textList["menu"]["program"]["name"])

        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["SSUnity"], self.radio_group, partial(self.callProgram, "SSUnity"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["orgInfoEditor"], self.radio_group, partial(self.callProgram, "orgInfoEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlBin"], self.radio_group, partial(self.callProgram, "mdlBin"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["mdlinfo"], self.radio_group, partial(self.callProgram, "mdlinfo"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["comicscript"], self.radio_group, partial(self.callProgram, "comicscript"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["musicEditor"], self.radio_group, partial(self.callProgram, "musicEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["fvtMaker"], self.radio_group, partial(self.callProgram, "fvtMaker"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["railEditor"], self.radio_group, partial(self.callProgram, "railEditor"))
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["rsRail"], self.radio_group, partial(self.callProgram, "rsRail"))
        progmenu.addSeparator()
        self.createRadioAction(progmenu, textSetting.textList["menu"]["program"]["smf"], self.radio_group, partial(self.callProgram, "smf"))
        progmenu.addSeparator()
        self.createDefaultAction(progmenu, textSetting.textList["menu"]["program"]["exit"], sys.exit)

        filemenu = menubar.addMenu(textSetting.textList["menu"]["file"]["name"])
        self.createDefaultAction(filemenu, textSetting.textList["menu"]["file"]["loadFile"], self.loadFile)

        self.configMenu = None
        self.configActionDict = {}

    def createRadioAction(self, menu, text, radioGroup, callback):
        action = QAction(text, self)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(callback)
        menu.addAction(action)
        radioGroup.addAction(action)
        return action

    def createDefaultAction(self, menu, text, callback):
        action = QAction(text, self)
        action.triggered.connect(callback)
        menu.addAction(action)

    def checkUpdate(self):
        if self.onlineVersion == "":
            return
        if self.onlineVersion == self.version:
            return

        msg = textSetting.textList["update"]["message"].format(self.onlineVersion)
        result = mb.askyesno(title=textSetting.textList["update"]["title"], message=msg)
        if result == mb.YES:
            mainProcess.openReleases()

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
            newWidget = ssUnityGui.SSUnityWindow(self.importDict)
        elif self.selectedProgram == "railEditor":
            newWidget = railEditorGui.RailEditorWindow(self.importDict)

        self.setConfigMenu(self.selectedProgram)

        if newWidget is None:
            return
        self.stack.addWidget(newWidget)
        self.stack.setCurrentWidget(newWidget)

    def setConfigMenu(self, selectedProgram):
        if self.configMenu:
            self.menuBar().removeAction(self.configMenu.menuAction())
            self.configMenu = None

        if selectedProgram in ["SSUnity", "railEditor"]:
            self.configMenu = self.addXlsxWriteOptionMenu()
            self.menuBar().addMenu(self.configMenu)

    def addXlsxWriteOptionMenu(self):
        configPath = self.importDict["configPath"]

        configMenu = QMenu(textSetting.textList["menu"]["SSUnity"]["name"], self)
        modelRadioGroup = QActionGroup(self)
        modelRadioGroup.setExclusive(True)
        self.configActionDict["model"] = []
        modelAction1 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["model1"], modelRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "model", 0))
        modelAction2 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["model2"], modelRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "model", 1))
        self.configActionDict["model"].append(modelAction1)
        self.configActionDict["model"].append(modelAction2)
        configMenu.addSeparator()

        flagRadioGroup = QActionGroup(self)
        flagRadioGroup.setExclusive(True)
        self.configActionDict["flag"] = []
        flagAction1 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["flag1"], flagRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "flag", 0))
        flagAction2 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["flag2"], flagRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "flag", 1))
        self.configActionDict["flag"].append(flagAction1)
        self.configActionDict["flag"].append(flagAction2)
        configMenu.addSeparator()

        ambReadRadioGroup = QActionGroup(self)
        ambReadRadioGroup.setExclusive(True)
        self.configActionDict["amb"] = []
        ambAction1 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["ambRead1"], ambReadRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "amb", 0))
        ambAction2 = self.createRadioAction(configMenu, textSetting.textList["menu"]["SSUnity"]["write"]["ambRead2"], ambReadRadioGroup, partial(mainProcess.writeXlsxConfig, configPath, "amb", 1))
        self.configActionDict["amb"].append(ambAction1)
        self.configActionDict["amb"].append(ambAction2)

        model, flag, amb = mainProcess.readXlsxWriteConfig(configPath)
        self.configActionDict["model"][model].setChecked(True)
        self.configActionDict["flag"][flag].setChecked(True)
        self.configActionDict["amb"][amb].setChecked(True)

        return configMenu

    def loadFile(self):
        if self.selectedProgram is None:
            mb.showerror(title=textSetting.textList["error"], message=textSetting.textList["errorList"]["E1"])
            return

        currentWidget = self.stack.currentWidget()
        if currentWidget:
            currentWidget.openFile()


def guiMain(importDict):
    app = QApplication([])
    window = MainWindow(importDict)
    importDict["window"] = window
    window.show()
    sys.exit(app.exec())
