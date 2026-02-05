import os
import sys
import json


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
