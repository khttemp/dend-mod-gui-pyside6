import os
import platform
import configparser


def _resolveConfigPath():
    configPath = "config.ini"
    if platform.system() == "Windows":
        configPath = os.path.join(os.getenv("APPDATA"), "dend-mod-gui-pyside6", "config.ini")
    return configPath


def _loadLanguage():
    configPath = _resolveConfigPath()
    if os.path.exists(configPath):
        config = configparser.ConfigParser()
        config.read(configPath, encoding="utf-8")
        if config.has_option("LANGUAGE", "lang"):
            return config.get("LANGUAGE", "lang")
    return "ja"


if _loadLanguage() == "en":
    from program.sub.textSetting_en import textList
else:
    from program.sub.textSetting_ja import textList
