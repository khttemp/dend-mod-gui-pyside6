import program.sub.textSetting as textSetting

from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel,
    QVBoxLayout, QHBoxLayout, QGridLayout
)

from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt


class CsvWidget(QWidget):
    def __init__(self, headerList, dataList):
        super().__init__()

        font3 = QFont(textSetting.textList["font3"][0], textSetting.textList["font3"][1])
        labelWidth = 80

        # mainLayout
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        for i, header in enumerate(headerList):
            headerLabel = QLabel(header, font=font3)
            headerLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            headerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if i != len(headerList) - 1:
                headerLabel.setFixedWidth(labelWidth)
            mainLayout.addWidget(headerLabel, 0, i)

        for i, dataInfo in enumerate(dataList):
            for j, data in enumerate(dataInfo):
                dataLabel = QLabel(str(data), font=font3)
                dataLabel.setTextFormat(Qt.TextFormat.PlainText)
                dataLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
                if j != len(dataInfo) - 1:
                    dataLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    dataLabel.setFixedWidth(labelWidth)
                mainLayout.addWidget(dataLabel, i + 1, j)


class DescWidget(QWidget):
    def __init__(self, fvtImageInfo, game):
        super().__init__()

        self.LS = 1
        self.BS = 2
        self.CS = 3
        self.RS = 4

        font4 = QFont(textSetting.textList["font4"][0], textSetting.textList["font4"][1])
        # mainLayout
        mainLayout = QHBoxLayout(self)

        # descFrame
        descGridLayout = QGridLayout()
        descGridLayout.setContentsMargins(0, 0, 0, 0)
        descGridLayout.setSpacing(0)
        mainLayout.addLayout(descGridLayout, 1)
        # descFrame - faceNum
        faceNumLabel = QLabel(textSetting.textList["fvtMaker"]["faceNum2"], font=font4)
        faceNumLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        faceNumLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descGridLayout.addWidget(faceNumLabel, 0, 0)
        faceNumDescLabel = QLabel(textSetting.textList["fvtMaker"]["faceNumDesc"], font=font4)
        faceNumDescLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        faceNumDescLabel.setTextFormat(Qt.TextFormat.PlainText)
        descGridLayout.addWidget(faceNumDescLabel, 0, 1)
        # descFrame - faceSize
        faceSizeLabel = QLabel(textSetting.textList["fvtMaker"]["faceSize"], font=font4)
        faceSizeLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        faceSizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descGridLayout.addWidget(faceSizeLabel, 1, 0)
        faceSizeDescLabel = QLabel(textSetting.textList["fvtMaker"]["faceSizeDesc"], font=font4)
        faceSizeDescLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        faceSizeDescLabel.setTextFormat(Qt.TextFormat.PlainText)
        descGridLayout.addWidget(faceSizeDescLabel, 1, 1)
        # descFrame - effect
        effectLabel = QLabel(textSetting.textList["fvtMaker"]["effect"], font=font4)
        effectLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        effectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descGridLayout.addWidget(effectLabel, 2, 0)
        effectDescLabel = QLabel(textSetting.textList["fvtMaker"]["effectDesc"], font=font4)
        effectDescLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        effectDescLabel.setTextFormat(Qt.TextFormat.PlainText)
        descGridLayout.addWidget(effectDescLabel, 2, 1)
        # descFrame - voice
        voiceLabel = QLabel(textSetting.textList["fvtMaker"]["voNum2"], font=font4)
        voiceLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        voiceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descGridLayout.addWidget(voiceLabel, 3, 0)
        voiceDescLabel = QLabel(textSetting.textList["fvtMaker"]["voNumDesc"], font=font4)
        voiceDescLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        voiceDescLabel.setTextFormat(Qt.TextFormat.PlainText)
        descGridLayout.addWidget(voiceDescLabel, 3, 1)
        # descFrame - text
        textLabel = QLabel(textSetting.textList["fvtMaker"]["textTag"], font=font4)
        textLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descGridLayout.addWidget(textLabel, 4, 0)
        textDescLabel = QLabel(textSetting.textList["fvtMaker"]["textTagDesc"], font=font4)
        textDescLabel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        textDescLabel.setTextFormat(Qt.TextFormat.PlainText)
        descGridLayout.addWidget(textDescLabel, 4, 1)

        # imageFrame
        imageLayout = QVBoxLayout()
        imageLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addLayout(imageLayout, 1)

        if game > self.LS:
            if game == self.BS:
                path = fvtImageInfo["BS"]
            elif game == self.CS:
                path = fvtImageInfo["CS"]
            else:
                path = fvtImageInfo["RS"]
            imageLabel = QLabel()
            imageLayout.addWidget(imageLabel)
            pixMap = QPixmap(path)
            imageLabel.setPixmap(pixMap)
