import os
import sys
import json

from program.sub.ssUnity.importPy.excelWidget import ExcelWidget


def resource_path(localDir, relative_path):
    bundle_dir = getattr(sys, "_MEIPASS", localDir)
    return os.path.join(bundle_dir, relative_path)


def readModelInfo(jsonName):
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "importPy")
    path = resource_path(filePath, jsonName)
    f = open(path, "r", encoding="utf-8")
    modelDict = json.load(f)
    f.close()

    railModelInfo = {}
    for model in list(modelDict["railModelInfo"].keys()):
        railModelInfo[model.lower()] = modelDict["railModelInfo"][model]

    ambModelInfo = []
    for model in modelDict["ambModelInfo"]:
        ambModelInfo.append(model.lower())

    return (railModelInfo, ambModelInfo)


def extractDenFile(filePath, fileType, data):
    if fileType == "AudioClip":
        for _, d in data.samples.items():
            w = open(filePath, "wb")
            w.write(d)
            w.close()
        return True

    if os.path.splitext(filePath)[1].lower() != ".xlsx":
        w = open(filePath, "wb")
        w.write(data.script)
        w.close()
        return True
    return False


def extractDenFileByExcel(filePath, data, configPath):
    railModelInfo, ambModelInfo = readModelInfo("model.json")
    excelWidget = ExcelWidget(data.script.tobytes().decode(), filePath, configPath, railModelInfo, ambModelInfo)
    if not excelWidget.extractExcel():
        return (False, excelWidget.errorMessage)
    return (True, excelWidget.warningMessage)


def loadExcelData(filePath, data, configPath):
    railModelInfo, ambModelInfo = readModelInfo("model.json")
    excelWidget = ExcelWidget(data.script.tobytes().decode(), filePath, configPath, railModelInfo, ambModelInfo)
    if not excelWidget.loadExcelAndMerge():
        return (False, {"message":excelWidget.errorMessage})
    return (True, {"message":excelWidget.warningMessage, "data":excelWidget.newLinesObj})


def getScriptData(filePath):
    with open(filePath, "rb") as f:
        return f.read()


def getScriptDataByExcel(newLines):
    return bytearray("\n".join(newLines).encode("utf-8"))


def saveDenFile(data, decryptFile, script):
    data.script = script
    data.save()
    with open(decryptFile.filePath, "wb") as w:
        w.write(decryptFile.env.file.save())
