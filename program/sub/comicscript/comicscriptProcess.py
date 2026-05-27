import os
import sys
import json
import configparser
import requests

import program.sub.textSetting as textSetting


def getGameOption(configPath):
    try:
        configRead = configparser.ConfigParser()
        configRead.read(configPath, encoding="utf-8")
        game = int(configRead.get("COMICSCRIPT_GAME", "mode"))
    except Exception:
        game = 0

    return textSetting.textList["menu"]["comicscript"]["gameList"][game]
