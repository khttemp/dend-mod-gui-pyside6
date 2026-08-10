import os
import sys
import json
import platform

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting

importDict = {
    "configPath": "config.ini",
    "window": None,
    "lang": "ja",
    "EXIT_CODE_RESTART": 99
}

if getattr(sys, "frozen", False):
    importDict["rootPath"] = os.path.join(os.path.abspath(os.path.dirname(sys.executable)), "_internal", "data")
else:
    importDict["rootPath"] = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows":
    importDict["configPath"] = os.path.join(os.getenv("APPDATA"), "dend-mod-gui-pyside6", "config.ini")

importDict["lang"] = mainProcess.readLanguageConfig(importDict["configPath"])
readTextFileName = "textSetting_{}.json".format(importDict["lang"])
readTextFilePath = os.path.join(importDict["rootPath"], "program", "sub", readTextFileName)
if not os.path.exists(readTextFilePath):
    readTextFileName = "textSetting_ja.json"
    readTextFilePath = os.path.join(importDict["rootPath"], "program", "sub", readTextFileName)
with open(readTextFilePath, "r", encoding="utf-8") as f:
    textList = json.load(f)
textSetting.textList = {}
textSetting.textList.update(textList)

if __name__ == "__main__":
    import program.main.mainGui as mainGui
    mainGui.guiMain(importDict)
