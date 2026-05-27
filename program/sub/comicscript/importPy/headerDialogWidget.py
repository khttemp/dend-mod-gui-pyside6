import copy

import program.sub.textSetting as textSetting
import program.sub.appearance.customMessageBoxWidget as customMessageBoxWidget

from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QDialogButtonBox, QGroupBox,
    QHBoxLayout, QListWidget, QComboBox, QFrame, QGridLayout,
    QLineEdit, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

mb = customMessageBoxWidget.CustomMessageBox()


class ImageListWidget(QWidget):
    def __init__(self, groupBoxTitle, imgList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.imgList = copy.deepcopy(imgList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        imageGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(imageGroupBox)
        # mainLayout - QGroupBox - imageListLayout
        imageListLayout = QVBoxLayout()
        imageGroupBox.setLayout(imageListLayout)
        # mainLayout - QGroupBox - imageListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        imageListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - imageListLayout - buttonLayout - modifyButton
        self.modifyButton = QPushButton(textSetting.textList["modify"], font=font6)
        self.modifyButton.setEnabled(False)
        self.modifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.modifyButton.clicked.connect(self.modifyFunc)
        buttonLayout.addWidget(self.modifyButton)
        # layout - buttonLayout - insertButton
        self.insertButton = QPushButton(textSetting.textList["insert"], font=font6)
        self.insertButton.setEnabled(False)
        self.insertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.insertButton.clicked.connect(self.insertFunc)
        buttonLayout.addWidget(self.insertButton)
        # layout - buttonLayout - deleteButton
        self.deleteButton = QPushButton(textSetting.textList["delete"], font=font6)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.clicked.connect(self.deleteFunc)
        buttonLayout.addWidget(self.deleteButton)

        # mainLayout - QGroupBox - imageListLayout - QListWidget
        self.imageListListWidget = QListWidget(font=font2)
        displayImageList = self.setListboxInfo(self.imgList)
        self.imageListListWidget.addItems(displayImageList)
        self.imageListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        imageListLayout.addWidget(self.imageListListWidget, stretch=1)

    def setListboxInfo(self, imgList):
        displayImageList = []
        if len(imgList) > 0:
            for i, imgName in enumerate(imgList):
                dipslayImageInfo = "{0:02d}→{1}".format(i, imgName)
                displayImageList.append(dipslayImageInfo)
        else:
            displayImageList = [textSetting.textList["comicscript"]["noList"]]
        return displayImageList

    def onItemClicked(self, item):
        self.selectIndex = self.imageListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["comicscript"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.imgList[self.selectIndex]
        editImageListWidget = EditImageListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item)
        if editImageListWidget.exec() == QDialog.Accepted:
            self.imgList[self.selectIndex] = editImageListWidget.resultValue
            displayImageList = self.setListboxInfo(self.imgList)
            self.imageListListWidget.clear()
            self.imageListListWidget.addItems(displayImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editImageListWidget = EditImageListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert")
        if editImageListWidget.exec() == QDialog.Accepted:
            self.imgList.insert(self.selectIndex + editImageListWidget.insertPos, editImageListWidget.resultValue)
            displayImageList = self.setListboxInfo(self.imgList)
            self.imageListListWidget.clear()
            self.imageListListWidget.addItems(displayImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.imgList.pop(self.selectIndex)
            displayImageList = self.setListboxInfo(self.imgList)
            self.imageListListWidget.clear()
            self.imageListListWidget.addItems(displayImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditImageListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.resultValue = ""
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.imageInfoGridLayout = QGridLayout()
        layout.addLayout(self.imageInfoGridLayout)
        # layout - QGridLayout - imageNameLabel
        imageNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgLabel"], font=self.font2)
        self.imageInfoGridLayout.addWidget(imageNameLabel, 0, 0)
        # layout - QGridLayout - imageNameLineEdit
        self.imageNameLineEdit = QLineEdit(font=self.font2)
        self.imageInfoGridLayout.addWidget(self.imageNameLineEdit, 0, 1)

        if self.mode == "modify":
            self.imageNameLineEdit.setText("{0}".format(item))

        if self.mode == "insert":
            self.setInsertWidget(1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.imageInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["comicscript"]["posLabel"], font=self.font2)
        self.imageInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["comicscript"]["posValue"])
        self.imageInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValue = ""
        if not self.imageNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerImgLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValue = self.imageNameLineEdit.text()

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class ImageSizeListWidget(QWidget):
    def __init__(self, groupBoxTitle, imgSizeList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.imgSizeList = copy.deepcopy(imgSizeList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        imageSizeGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(imageSizeGroupBox)
        # mainLayout - QGroupBox - imageSizeListLayout
        imageSizeListLayout = QVBoxLayout()
        imageSizeGroupBox.setLayout(imageSizeListLayout)
        # mainLayout - QGroupBox - imageSizeListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        imageSizeListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - imageSizeListLayout - buttonLayout - modifyButton
        self.modifyButton = QPushButton(textSetting.textList["modify"], font=font6)
        self.modifyButton.setEnabled(False)
        self.modifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.modifyButton.clicked.connect(self.modifyFunc)
        buttonLayout.addWidget(self.modifyButton)
        # layout - buttonLayout - insertButton
        self.insertButton = QPushButton(textSetting.textList["insert"], font=font6)
        self.insertButton.setEnabled(False)
        self.insertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.insertButton.clicked.connect(self.insertFunc)
        buttonLayout.addWidget(self.insertButton)
        # layout - buttonLayout - deleteButton
        self.deleteButton = QPushButton(textSetting.textList["delete"], font=font6)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.clicked.connect(self.deleteFunc)
        buttonLayout.addWidget(self.deleteButton)

        # mainLayout - QGroupBox - imageSizeListLayout - QListWidget
        self.imageSizeListListWidget = QListWidget(font=font2)
        displayImageSizeList = self.setListboxInfo(self.imgSizeList)
        self.imageSizeListListWidget.addItems(displayImageSizeList)
        self.imageSizeListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        imageSizeListLayout.addWidget(self.imageSizeListListWidget, stretch=1)

    def setListboxInfo(self, imgSizeList):
        displayImageSizeList = []
        if len(imgSizeList) > 0:
            for i in range(len(imgSizeList)):
                dipslayImageSizeInfo = "{0:02d}→img{1:02d}, {2}".format(i, imgSizeList[i][0], imgSizeList[i][1])
                displayImageSizeList.append(dipslayImageSizeInfo)
        else:
            displayImageSizeList = [textSetting.textList["comicscript"]["noList"]]
        return displayImageSizeList

    def onItemClicked(self, item):
        self.selectIndex = self.imageSizeListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["comicscript"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.imgSizeList[self.selectIndex]
        editImageSizeListWidget = EditImageSizeListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item)
        if editImageSizeListWidget.exec() == QDialog.Accepted:
            self.imgSizeList[self.selectIndex] = editImageSizeListWidget.resultValueList
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.imageSizeListListWidget.clear()
            self.imageSizeListListWidget.addItems(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editImageSizeListWidget = EditImageSizeListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert")
        if editImageSizeListWidget.exec() == QDialog.Accepted:
            self.imgSizeList.insert(self.selectIndex + editImageSizeListWidget.insertPos, editImageSizeListWidget.resultValueList)
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.imageSizeListListWidget.clear()
            self.imageSizeListListWidget.addItems(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.imgSizeList.pop(self.selectIndex)
            displayImageSizeList = self.setListboxInfo(self.imgSizeList)
            self.imageSizeListListWidget.clear()
            self.imageSizeListListWidget.addItems(displayImageSizeList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditImageSizeListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        self.lineEditList = []
        self.resultValueList = []
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.imageSizeInfoGridLayout = QGridLayout()
        layout.addLayout(self.imageSizeInfoGridLayout)
        # layout - QGridLayout - imageIndexNameLabel
        imageIndexNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgIndex"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageIndexNameLabel, 0, 0)
        # layout - QGridLayout - imageIndexLineEdit
        self.imageIndexLineEdit = QLineEdit(font=self.font2)
        self.imageIndexLineEdit.setValidator(self.integerValidator)
        self.lineEditList.append(self.imageIndexLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageIndexLineEdit, 0, 1)

        # layout - QGridLayout - imageXNameLabel
        imageXNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgX"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageXNameLabel, 1, 0)
        # layout - QGridLayout - imageXLineEdit
        self.imageXLineEdit = QLineEdit(font=self.font2)
        self.imageXLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageXLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageXLineEdit, 1, 1)
        # layout - QGridLayout - imageYNameLabel
        imageYNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgY"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageYNameLabel, 2, 0)
        # layout - QGridLayout - imageYLineEdit
        self.imageYLineEdit = QLineEdit(font=self.font2)
        self.imageYLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageYLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageYLineEdit, 2, 1)
        # layout - QGridLayout - imageWidthNameLabel
        imageWidthNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgWidth"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageWidthNameLabel, 3, 0)
        # layout - QGridLayout - imageWidthLineEdit
        self.imageWidthLineEdit = QLineEdit(font=self.font2)
        self.imageWidthLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageWidthLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageWidthLineEdit, 3, 1)
        # layout - QGridLayout - imageHeightNameLabel
        imageHeightNameLabel = QLabel(textSetting.textList["comicscript"]["headerImgHeight"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageHeightNameLabel, 4, 0)
        # layout - QGridLayout - imageHeightLineEdit
        self.imageHeightLineEdit = QLineEdit(font=self.font2)
        self.imageHeightLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageHeightLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageHeightLineEdit, 4, 1)

        if self.mode == "modify":
            valueList = [
                item[0],
                item[1][0],
                item[1][1],
                item[1][2],
                item[1][3],
            ]
            for i, value in enumerate(valueList):
                self.lineEditList[i].setText("{0}".format(value))
        else:
            valueList = [
                0,
                float(-1),
                float(-1),
                float(-1),
                float(-1),
            ]
            for i, value in enumerate(valueList):
                self.lineEditList[i].setText("{0}".format(value))
            self.setInsertWidget(5)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.imageSizeInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["comicscript"]["posLabel"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["comicscript"]["posValue"])
        self.imageSizeInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        sizeInfo = []
        for i, lineEdit in enumerate(self.lineEditList):
            if not lineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            if i == 0:
                self.resultValueList.append(int(lineEdit.text()))
            else:
                sizeInfo.append(float(lineEdit.text()))
        self.resultValueList.append(sizeInfo)

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class WavListWidget(QWidget):
    def __init__(self, groupBoxTitle, wavList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.wavList = copy.deepcopy(wavList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        wavGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(wavGroupBox)
        # mainLayout - QGroupBox - wavListLayout
        wavListLayout = QVBoxLayout()
        wavGroupBox.setLayout(wavListLayout)
        # mainLayout - QGroupBox - wavListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        wavListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - wavListLayout - buttonLayout - modifyButton
        self.modifyButton = QPushButton(textSetting.textList["modify"], font=font6)
        self.modifyButton.setEnabled(False)
        self.modifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.modifyButton.clicked.connect(self.modifyFunc)
        buttonLayout.addWidget(self.modifyButton)
        # layout - buttonLayout - insertButton
        self.insertButton = QPushButton(textSetting.textList["insert"], font=font6)
        self.insertButton.setEnabled(False)
        self.insertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.insertButton.clicked.connect(self.insertFunc)
        buttonLayout.addWidget(self.insertButton)
        # layout - buttonLayout - deleteButton
        self.deleteButton = QPushButton(textSetting.textList["delete"], font=font6)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.clicked.connect(self.deleteFunc)
        buttonLayout.addWidget(self.deleteButton)

        # mainLayout - QGroupBox - wavListLayout - QListWidget
        self.wavListListWidget = QListWidget(font=font2)
        displayWavList = self.setListboxInfo(self.wavList)
        self.wavListListWidget.addItems(displayWavList)
        self.wavListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        wavListLayout.addWidget(self.wavListListWidget, stretch=1)

    def setListboxInfo(self, wavList):
        displayWavList = []
        if len(wavList) > 0:
            for i in range(len(wavList)):
                dipslayWavInfo = "{0:02d}→{1}, {2}".format(i, wavList[i][0], wavList[i][1])
                displayWavList.append(dipslayWavInfo)
        else:
            displayWavList = [textSetting.textList["comicscript"]["noList"]]
        return displayWavList

    def onItemClicked(self, item):
        self.selectIndex = self.wavListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["comicscript"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.wavList[self.selectIndex]
        editWavListWidget = EditWavListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item)
        if editWavListWidget.exec() == QDialog.Accepted:
            self.wavList[self.selectIndex] = editWavListWidget.resultValueList
            displayWavList = self.setListboxInfo(self.wavList)
            self.wavListListWidget.clear()
            self.wavListListWidget.addItems(displayWavList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editWavListWidget = EditWavListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert")
        if editWavListWidget.exec() == QDialog.Accepted:
            self.wavList.insert(self.selectIndex + editWavListWidget.insertPos, editWavListWidget.resultValueList)
            displayWavList = self.setListboxInfo(self.wavList)
            self.wavListListWidget.clear()
            self.wavListListWidget.addItems(displayWavList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.wavList.pop(self.selectIndex)
            displayWavList = self.setListboxInfo(self.wavList)
            self.wavListListWidget.clear()
            self.wavListListWidget.addItems(displayWavList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditWavListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.resultValueList = []
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.wavInfoGridLayout = QGridLayout()
        layout.addLayout(self.wavInfoGridLayout)
        # layout - QGridLayout - wavNameLabel
        wavNameLabel = QLabel(textSetting.textList["comicscript"]["headerSELabel"], font=self.font2)
        self.wavInfoGridLayout.addWidget(wavNameLabel, 0, 0)
        # layout - QGridLayout - wavNameLineEdit
        self.wavNameLineEdit = QLineEdit(font=self.font2)
        self.wavInfoGridLayout.addWidget(self.wavNameLineEdit, 0, 1)
        # layout - QGridLayout - wavGroupLabel
        wavGroupLabel = QLabel(textSetting.textList["comicscript"]["headerSEGroup"], font=self.font2)
        self.wavInfoGridLayout.addWidget(wavGroupLabel, 1, 0)
        # layout - QGridLayout - wavGroupLineEdit
        self.wavGroupLineEdit = QLineEdit(font=self.font2)
        self.wavGroupLineEdit.setValidator(self.integerValidator)
        self.wavInfoGridLayout.addWidget(self.wavGroupLineEdit, 1, 1)

        if self.mode == "modify":
            self.wavNameLineEdit.setText("{0}".format(item[0]))
            self.wavGroupLineEdit.setText("{0}".format(item[1]))
        else:
            self.wavGroupLineEdit.setText("{0}".format(0))
            self.setInsertWidget(2)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.wavInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["comicscript"]["posLabel"], font=self.font2)
        self.wavInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["comicscript"]["posValue"])
        self.wavInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        if not self.wavNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerSELabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueList.append(self.wavNameLineEdit.text())

        if not self.wavGroupLineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        self.resultValueList.append(int(self.wavGroupLineEdit.text()))

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class BgmListWidget(QWidget):
    def __init__(self, groupBoxTitle, bgmList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.bgmList = copy.deepcopy(bgmList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        bgmGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(bgmGroupBox)
        # mainLayout - QGroupBox - bgmListLayout
        bgmListLayout = QVBoxLayout()
        bgmGroupBox.setLayout(bgmListLayout)
        # mainLayout - QGroupBox - bgmListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        bgmListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - bgmListLayout - buttonLayout - modifyButton
        self.modifyButton = QPushButton(textSetting.textList["modify"], font=font6)
        self.modifyButton.setEnabled(False)
        self.modifyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.modifyButton.clicked.connect(self.modifyFunc)
        buttonLayout.addWidget(self.modifyButton)
        # layout - buttonLayout - insertButton
        self.insertButton = QPushButton(textSetting.textList["insert"], font=font6)
        self.insertButton.setEnabled(False)
        self.insertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.insertButton.clicked.connect(self.insertFunc)
        buttonLayout.addWidget(self.insertButton)
        # layout - buttonLayout - deleteButton
        self.deleteButton = QPushButton(textSetting.textList["delete"], font=font6)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.deleteButton.clicked.connect(self.deleteFunc)
        buttonLayout.addWidget(self.deleteButton)

        # mainLayout - QGroupBox - bgmListLayout - QListWidget
        self.bgmListListWidget = QListWidget(font=font2)
        displayBgmList = self.setListboxInfo(self.bgmList)
        self.bgmListListWidget.addItems(displayBgmList)
        self.bgmListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        bgmListLayout.addWidget(self.bgmListListWidget, stretch=1)

    def setListboxInfo(self, bgmList):
        displayBgmList = []
        if len(bgmList) > 0:
            for i in range(len(bgmList)):
                dipslayBgmInfo = "{0:02d}→{1} [{2}], [{3}, {4}]".format(i, bgmList[i][0], bgmList[i][1], bgmList[i][2], bgmList[i][3])
                displayBgmList.append(dipslayBgmInfo)
        else:
            displayBgmList = [textSetting.textList["comicscript"]["noList"]]
        return displayBgmList

    def onItemClicked(self, item):
        self.selectIndex = self.bgmListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["comicscript"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.bgmList[self.selectIndex]
        editBgmListWidget = EditBgmListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonModifyLabel"], "modify", item)
        if editBgmListWidget.exec() == QDialog.Accepted:
            self.bgmList[self.selectIndex] = editBgmListWidget.resultValueList
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.bgmListListWidget.clear()
            self.bgmListListWidget.addItems(displayBgmList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editBgmListWidget = EditBgmListWidget(self, self.groupBoxTitle + textSetting.textList["comicscript"]["commonInsertLabel"], "insert")
        if editBgmListWidget.exec() == QDialog.Accepted:
            self.bgmList.insert(self.selectIndex + editBgmListWidget.insertPos, editBgmListWidget.resultValueList)
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.bgmListListWidget.clear()
            self.bgmListListWidget.addItems(displayBgmList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.bgmList.pop(self.selectIndex)
            displayBgmList = self.setListboxInfo(self.bgmList)
            self.bgmListListWidget.clear()
            self.bgmListListWidget.addItems(displayBgmList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditBgmListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.numberValidator = QRegularExpressionValidator(QRegularExpression(r"^-?\d+(\.\d+)?$"), self)
        self.resultValueList = []
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.bgmInfoGridLayout = QGridLayout()
        layout.addLayout(self.bgmInfoGridLayout)
        # layout - QGridLayout - bgmNameLabel
        bgmNameLabel = QLabel(textSetting.textList["comicscript"]["headerBGMLabel"], font=self.font2)
        self.bgmInfoGridLayout.addWidget(bgmNameLabel, 0, 0)
        # layout - QGridLayout - bgmNameLineEdit
        self.bgmNameLineEdit = QLineEdit(font=self.font2)
        self.bgmInfoGridLayout.addWidget(self.bgmNameLineEdit, 0, 1)
        # layout - QGridLayout - bgmLoopFlagLabel
        bgmLoopFlagLabel = QLabel(textSetting.textList["comicscript"]["headerBGMLoopFlag"], font=self.font2)
        self.bgmInfoGridLayout.addWidget(bgmLoopFlagLabel, 1, 0)
        # layout - QGridLayout - bgmLoopFlagCombo
        self.bgmLoopFlagCombo = QComboBox(font=self.font2)
        self.bgmLoopFlagCombo.addItems(textSetting.textList["comicscript"]["headerBGMLoopLabelInfo"])
        self.bgmInfoGridLayout.addWidget(self.bgmLoopFlagCombo, 1, 1)
        # layout - QGridLayout - bgmStartLabel
        bgmStartLabel = QLabel(textSetting.textList["comicscript"]["headerBGMStart"], font=self.font2)
        self.bgmInfoGridLayout.addWidget(bgmStartLabel, 2, 0)
        # layout - QGridLayout - bgmStartLineEdit
        self.bgmStartLineEdit = QLineEdit(font=self.font2)
        self.bgmStartLineEdit.setValidator(self.numberValidator)
        self.bgmInfoGridLayout.addWidget(self.bgmStartLineEdit, 2, 1)
        # layout - QGridLayout - bgmLoopStartLabel
        bgmLoopStartLabel = QLabel(textSetting.textList["comicscript"]["headerBGMLoopStart"], font=self.font2)
        self.bgmInfoGridLayout.addWidget(bgmLoopStartLabel, 3, 0)
        # layout - QGridLayout - bgmStartLineEdit
        self.bgmLoopStartLineEdit = QLineEdit(font=self.font2)
        self.bgmLoopStartLineEdit.setValidator(self.numberValidator)
        self.bgmInfoGridLayout.addWidget(self.bgmLoopStartLineEdit, 3, 1)

        if self.mode == "modify":
            self.bgmNameLineEdit.setText("{0}".format(item[0]))
            self.bgmLoopFlagCombo.setCurrentIndex(item[1])
            self.bgmStartLineEdit.setText("{0}".format(item[2]))
            self.bgmLoopStartLineEdit.setText("{0}".format(item[3]))
        else:
            self.bgmLoopFlagCombo.setCurrentIndex(0)
            self.bgmStartLineEdit.setText("{0}".format(float(0)))
            self.bgmLoopStartLineEdit.setText("{0}".format(float(0)))
            self.setInsertWidget(4)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.bgmInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["comicscript"]["posLabel"], font=self.font2)
        self.bgmInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["comicscript"]["posValue"])
        self.bgmInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        if not self.bgmNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["comicscript"]["headerBGMLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueList.append(self.bgmNameLineEdit.text())
        self.resultValueList.append(self.bgmLoopFlagCombo.currentIndex())

        if not self.bgmStartLineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        self.resultValueList.append(float(self.bgmStartLineEdit.text()))

        if not self.bgmLoopStartLineEdit.hasAcceptableInput():
            mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
            return
        self.resultValueList.append(float(self.bgmLoopStartLineEdit.text()))

        if self.mode == "insert":
            self.insertPos = 1
            if self.insertCombo.currentIndex() == 1:
                self.insertPos = 0
        return True

    def accept(self):
        result = mb.askokcancel(title=textSetting.textList["confirm"], message=textSetting.textList["infoList"]["I21"])
        if result != mb.OK:
            return

        if not self.validate():
            return
        super().accept()


class EditHeaderDialog(QDialog):
    def __init__(self, parent, title, decryptFile):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.decryptFile = decryptFile
        self.dirtyFlag = False
        self.imgList = copy.deepcopy(decryptFile.imgList)
        self.imgSizeList = copy.deepcopy(decryptFile.imgSizeList)
        self.seList = copy.deepcopy(decryptFile.seList)
        self.bgmList = copy.deepcopy(decryptFile.bgmList)

        # layout
        layout = QVBoxLayout(self)
        # listLayout
        listLayout = QGridLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(listLayout)
        # listLayout - imageList
        self.imageSimpleList = ImageListWidget(textSetting.textList["comicscript"]["imgInfo"], self.imgList)
        listLayout.addWidget(self.imageSimpleList, 0, 0)
        # listLayout - imageSizeList
        self.imageSizeSimpleList = ImageSizeListWidget(textSetting.textList["comicscript"]["imgSizeInfo"], self.imgSizeList)
        listLayout.addWidget(self.imageSizeSimpleList, 0, 1)
        # listLayout - wavList
        self.wavSimpleList = WavListWidget(textSetting.textList["comicscript"]["seInfo"], self.seList)
        listLayout.addWidget(self.wavSimpleList, 0, 2)
        # listLayout - bgmList
        self.bgmSimpleList = BgmListWidget(textSetting.textList["comicscript"]["bgmInfo"], self.bgmList)
        listLayout.addWidget(self.bgmSimpleList, 0, 3)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        if self.dirtyFlag:
            result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I7"], icon="warning")
            if result:
                newImgList = self.imageSimpleList.imgList
                newImgSizeList = self.imageSizeSimpleList.imgSizeList
                newWavList = self.wavSimpleList.wavList
                newBgmList = self.bgmSimpleList.bgmList
                if not self.decryptFile.saveHeader(newImgList, newImgSizeList, newWavList, newBgmList):
                    self.decryptFile.printError()
                    mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                    return
                return True
        else:
            return True

    def accept(self):
        self.dirtyFlag = False
        self.dirtyFlag |= self.imageSimpleList.dirtyFlag
        self.dirtyFlag |= self.imageSizeSimpleList.dirtyFlag
        self.dirtyFlag |= self.wavSimpleList.dirtyFlag
        self.dirtyFlag |= self.bgmSimpleList.dirtyFlag

        if self.dirtyFlag:
            if not self.validate():
                return
            super().accept()
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I8"])
        else:
            super().accept()
