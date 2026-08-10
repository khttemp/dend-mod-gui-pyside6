import os
import sys
import json
import glob
import platform

import program.main.mainProcess as mainProcess
import program.sub.textSetting as textSetting

importDict = {
    "configPath": "config.ini",
    "window": None,
    "lang": "ja",
    "langList": [["日本語", "ja"]],
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
findFlag = False

importDict["langList"] = [["日本語", "ja"]]
textSetting.textList = {}

readTextFilePath = os.path.join(importDict["rootPath"], "program", "sub", "textSetting_*.json")
findTextFileList = glob.glob(readTextFilePath)
for textFile in findTextFileList:
    with open(textFile, "r", encoding="utf-8") as f:
        textList = json.load(f)
    if textList["langCode"] != "ja":
        importDict["langList"].append([textList["langTitle"], textList["langCode"]])
    if os.path.basename(textFile).lower() == readTextFileName.lower():
        findFlag = True
        textSetting.textList.update(textList)

if not findFlag:
    importDict["lang"] = "ja"
    readTextFilePath = os.path.join(importDict["rootPath"], "program", "sub", "textSetting_ja.json")
    with open(textFile, "r", encoding="utf-8") as f:
        textList = json.load(f)
    textSetting.textList.update(textList)

if __name__ == "__main__":
    import program.main.mainGui as mainGui
    mainGui.guiMain(importDict)
