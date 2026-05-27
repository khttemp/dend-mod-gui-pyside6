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
    def __init__(self, groupBoxTitle, imgList, ver):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.imgList = copy.deepcopy(imgList)
        self.dirtyFlag = False
        self.ver = ver

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
            for i in range(len(imgList)):
                imgName = imgList[i]["imgName"]
                if self.ver == 4:
                    dipslayImageInfo = "{0:02d}→{1}, {2}".format(i, imgName, imgList[i]["imgElse"])
                else:
                    dipslayImageInfo = "{0:02d}→{1}".format(i, imgName)
                displayImageList.append(dipslayImageInfo)
        else:
            displayImageList = [textSetting.textList["mdlBin"]["noList"]]
        return displayImageList

    def onItemClicked(self, item):
        self.selectIndex = self.imageListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlBin"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.imgList[self.selectIndex]
        editImageListWidget = EditImageListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], self.ver, "modify", item)
        if editImageListWidget.exec() == QDialog.Accepted:
            self.imgList[self.selectIndex] = editImageListWidget.resultValueInfo
            displayImageList = self.setListboxInfo(self.imgList)
            self.imageListListWidget.clear()
            self.imageListListWidget.addItems(displayImageList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editImageListWidget = EditImageListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], self.ver, "insert")
        if editImageListWidget.exec() == QDialog.Accepted:
            self.imgList.insert(self.selectIndex + editImageListWidget.insertPos, editImageListWidget.resultValueInfo)
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
    def __init__(self, parent, title, ver, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.ver = ver
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.resultValueInfo = {}
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
        imageNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgLabel"], font=self.font2)
        self.imageInfoGridLayout.addWidget(imageNameLabel, 0, 0)
        # layout - QGridLayout - imageNameLineEdit
        self.imageNameLineEdit = QLineEdit(font=self.font2)
        self.imageInfoGridLayout.addWidget(self.imageNameLineEdit, 0, 1)

        if self.mode == "modify":
            self.imageNameLineEdit.setText("{0}".format(item["imgName"]))

        if self.ver == 4:
            # layout - QGridLayout - imageElse1Label
            imageElse1Label = QLabel(textSetting.textList["mdlBin"]["else"] + "1", font=self.font2)
            self.imageInfoGridLayout.addWidget(imageElse1Label, 1, 0)
            # layout - QGridLayout - imageElse1Combo
            self.imageElse1Combo = QComboBox(font=self.font2)
            comboItemList = [str(x) for x in textSetting.textList["mdlBin"]["headerElse1Value"]]
            self.imageElse1Combo.addItems(comboItemList)
            self.imageElse1Combo.setCurrentIndex(-1)
            self.imageElse1Combo.currentIndexChanged.connect(self.imageElseChange)
            self.imageInfoGridLayout.addWidget(self.imageElse1Combo, 1, 1)
            # layout - QGridLayout - imageElse1Label
            imageElse2Label = QLabel(textSetting.textList["mdlBin"]["else"] + "2", font=self.font2)
            self.imageInfoGridLayout.addWidget(imageElse2Label, 2, 0)
            # layout - QGridLayout - imageNameLineEdit
            self.imageElse2LineEdit = QLineEdit(font=self.font2)
            self.imageElse2LineEdit.setValidator(self.integerValidator)
            self.imageInfoGridLayout.addWidget(self.imageElse2LineEdit, 2, 1)
            if self.mode == "modify":
                self.imageElse1Combo.setCurrentIndex(item["imgElse"][0])
                if item["imgElse"][0] != 0:
                    self.imageElse2LineEdit.setText("{0}".format(item["imgElse"][1]))
            else:
                self.imageElse1Combo.setCurrentIndex(0)
                self.imageElse2LineEdit.setText("{0}".format(0))

        if self.mode == "insert":
            if self.ver == 4:
                self.setInsertWidget(3)
            else:
                self.setInsertWidget(1)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def imageElseChange(self):
        if self.imageElse1Combo.currentIndex() == 0:
            self.imageElse2LineEdit.setEnabled(False)
        else:
            self.imageElse2LineEdit.setEnabled(True)

    def setInsertWidget(self, insertRow):
        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.imageInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
        self.imageInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
        self.imageInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueInfo = {}
        if not self.imageNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerImgLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False
        self.resultValueInfo["imgName"] = self.imageNameLineEdit.text()
        self.resultValueInfo["imgElse"] = []

        if self.ver == 4:
            if not self.imageElse2LineEdit.hasAcceptableInput():
                mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                return
            self.resultValueInfo["imgElse"].append(int(self.imageElse1Combo.currentText()))
            if self.imageElse1Combo.currentIndex() != 0:
                self.resultValueInfo["imgElse"].append(int(self.imageElse2LineEdit.text()))

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
            displayImageSizeList = [textSetting.textList["mdlBin"]["noList"]]
        return displayImageSizeList

    def onItemClicked(self, item):
        self.selectIndex = self.imageSizeListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlBin"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.imgSizeList[self.selectIndex]
        editImageSizeListWidget = EditImageSizeListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item)
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
        editImageSizeListWidget = EditImageSizeListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert")
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
        imageIndexNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgIndex"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageIndexNameLabel, 0, 0)
        # layout - QGridLayout - imageIndexLineEdit
        self.imageIndexLineEdit = QLineEdit(font=self.font2)
        self.imageIndexLineEdit.setValidator(self.integerValidator)
        self.lineEditList.append(self.imageIndexLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageIndexLineEdit, 0, 1)

        # layout - QGridLayout - imageXNameLabel
        imageXNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgX"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageXNameLabel, 1, 0)
        # layout - QGridLayout - imageXLineEdit
        self.imageXLineEdit = QLineEdit(font=self.font2)
        self.imageXLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageXLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageXLineEdit, 1, 1)
        # layout - QGridLayout - imageYNameLabel
        imageYNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgY"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageYNameLabel, 2, 0)
        # layout - QGridLayout - imageYLineEdit
        self.imageYLineEdit = QLineEdit(font=self.font2)
        self.imageYLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageYLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageYLineEdit, 2, 1)
        # layout - QGridLayout - imageWidthNameLabel
        imageWidthNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgWidth"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(imageWidthNameLabel, 3, 0)
        # layout - QGridLayout - imageWidthLineEdit
        self.imageWidthLineEdit = QLineEdit(font=self.font2)
        self.imageWidthLineEdit.setValidator(self.numberValidator)
        self.lineEditList.append(self.imageWidthLineEdit)
        self.imageSizeInfoGridLayout.addWidget(self.imageWidthLineEdit, 3, 1)
        # layout - QGridLayout - imageHeightNameLabel
        imageHeightNameLabel = QLabel(textSetting.textList["mdlBin"]["headerImgHeight"], font=self.font2)
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
        insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
        self.imageSizeInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
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


class SmfNameListWidget(QWidget):
    def __init__(self, groupBoxTitle, smfList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.smfList = copy.deepcopy(smfList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        smfNameGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(smfNameGroupBox)
        # mainLayout - QGroupBox - smfNameListLayout
        smfNameListLayout = QVBoxLayout()
        smfNameGroupBox.setLayout(smfNameListLayout)
        # mainLayout - QGroupBox - smfNameListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        smfNameListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - smfNameListLayout - buttonLayout - modifyButton
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

        # mainLayout - QGroupBox - smfNameListLayout - QListWidget
        self.smfNameListListWidget = QListWidget(font=font2)
        displaySmfNameList = self.setListboxInfo(self.smfList)
        self.smfNameListListWidget.addItems(displaySmfNameList)
        self.smfNameListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        smfNameListLayout.addWidget(self.smfNameListListWidget, stretch=1)

    def setListboxInfo(self, smfList):
        displaySmfNameList = []
        if len(smfList) > 0:
            for i in range(len(smfList)):
                dipslaySmfNameInfo = "{0:02d}→{1}".format(i, smfList[i])
                displaySmfNameList.append(dipslaySmfNameInfo)
        else:
            displaySmfNameList = [textSetting.textList["mdlBin"]["noList"]]
        return displaySmfNameList

    def onItemClicked(self, item):
        self.selectIndex = self.smfNameListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlBin"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.smfList[self.selectIndex]
        editSmfNameListWidget = EditSmfNameListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item)
        if editSmfNameListWidget.exec() == QDialog.Accepted:
            self.smfList[self.selectIndex] = editSmfNameListWidget.resultValue
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.smfNameListListWidget.clear()
            self.smfNameListListWidget.addItems(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editSmfNameListWidget = EditSmfNameListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert")
        if editSmfNameListWidget.exec() == QDialog.Accepted:
            self.smfList.insert(self.selectIndex + editSmfNameListWidget.insertPos, editSmfNameListWidget.resultValue)
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.smfNameListListWidget.clear()
            self.smfNameListListWidget.addItems(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.smfList.pop(self.selectIndex)
            displaySmfNameList = self.setListboxInfo(self.smfList)
            self.smfNameListListWidget.clear()
            self.smfNameListListWidget.addItems(displaySmfNameList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditSmfNameListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.resultValue = ""
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.smfNameInfoGridLayout = QGridLayout()
        layout.addLayout(self.smfNameInfoGridLayout)
        # layout - QGridLayout - smfNameLabel
        smfNameLabel = QLabel(textSetting.textList["mdlBin"]["headerSmfLabel"], font=self.font2)
        self.smfNameInfoGridLayout.addWidget(smfNameLabel, 0, 0)
        # layout - QGridLayout - smfNameLineEdit
        self.smfNameLineEdit = QLineEdit(font=self.font2)
        self.smfNameInfoGridLayout.addWidget(self.smfNameLineEdit, 0, 1)

        if self.mode == "modify":
            self.smfNameLineEdit.setText("{0}".format(item))
        else:
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
        self.smfNameInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
        self.smfNameInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
        self.smfNameInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValue = ""
        if not self.smfNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerSmfLabel"])
            mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
            return False

        self.resultValue = self.smfNameLineEdit.text()
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
            displayWavList = [textSetting.textList["mdlBin"]["noList"]]
        return displayWavList

    def onItemClicked(self, item):
        self.selectIndex = self.wavListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlBin"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.wavList[self.selectIndex]
        editWavListWidget = EditWavListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item)
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
        editWavListWidget = EditWavListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert")
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
        wavNameLabel = QLabel(textSetting.textList["mdlBin"]["headerSELabel"], font=self.font2)
        self.wavInfoGridLayout.addWidget(wavNameLabel, 0, 0)
        # layout - QGridLayout - wavNameLineEdit
        self.wavNameLineEdit = QLineEdit(font=self.font2)
        self.wavInfoGridLayout.addWidget(self.wavNameLineEdit, 0, 1)
        # layout - QGridLayout - wavGroupLabel
        wavGroupLabel = QLabel(textSetting.textList["mdlBin"]["headerSEGroup"], font=self.font2)
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
        insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
        self.wavInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
        self.wavInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueList = []
        if not self.wavNameLineEdit.text():
            errorMsg = textSetting.textList["errorList"]["E139"].format(textSetting.textList["mdlBin"]["headerSELabel"])
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


class TgaListWidget(QWidget):
    def __init__(self, groupBoxTitle, tgaList):
        super().__init__()
        self.groupBoxTitle = groupBoxTitle
        self.tgaList = copy.deepcopy(tgaList)
        self.dirtyFlag = False

        font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        font6 = QFont(textSetting.textList["font6"][0], textSetting.textList["font6"][1])

        # mainLayout
        mainLayout = QVBoxLayout(self)
        # mainLayout - QGroupBox
        tgaGroupBox = QGroupBox(groupBoxTitle)
        mainLayout.addWidget(tgaGroupBox)
        # mainLayout - QGroupBox - tgaListLayout
        tgaListLayout = QVBoxLayout()
        tgaGroupBox.setLayout(tgaListLayout)
        # mainLayout - QGroupBox - tgaListLayout - buttonLayout
        buttonLayout = QHBoxLayout()
        tgaListLayout.addLayout(buttonLayout)
        # mainLayout - QGroupBox - tgaListLayout - buttonLayout - modifyButton
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

        # mainLayout - QGroupBox - tgaListLayout - QListWidget
        self.tgaListListWidget = QListWidget(font=font2)
        displayTgaList = self.setListboxInfo(self.tgaList)
        self.tgaListListWidget.addItems(displayTgaList)
        self.tgaListListWidget.itemClicked.connect(self.onItemClicked)
        self.selectIndex = -1
        tgaListLayout.addWidget(self.tgaListListWidget, stretch=1)

    def setListboxInfo(self, tgaList):
        displayTgaList = []
        if len(tgaList) > 0:
            for i in range(len(tgaList)):
                dipslayTgaInfo = "{0:02d}→{1}, {2}".format(i, tgaList[i]["tgaInfo"], tgaList[i]["tgaElse"])
                displayTgaList.append(dipslayTgaInfo)
        else:
            displayTgaList = [textSetting.textList["mdlBin"]["noList"]]
        return displayTgaList

    def onItemClicked(self, item):
        self.selectIndex = self.tgaListListWidget.row(item)
        self.insertButton.setEnabled(True)
        if item.text() == textSetting.textList["mdlBin"]["noList"]:
            self.modifyButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            self.modifyButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def modifyFunc(self):
        item = self.tgaList[self.selectIndex]
        editTgaListWidget = EditTgaListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonModifyLabel"], "modify", item)
        if editTgaListWidget.exec() == QDialog.Accepted:
            self.tgaList[self.selectIndex] = editTgaListWidget.resultValueInfo
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.tgaListListWidget.clear()
            self.tgaListListWidget.addItems(displayTgaList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def insertFunc(self):
        editTgaListWidget = EditTgaListWidget(self, self.groupBoxTitle + textSetting.textList["mdlBin"]["commonInsertLabel"], "insert")
        if editTgaListWidget.exec() == QDialog.Accepted:
            self.tgaList.insert(self.selectIndex + editTgaListWidget.insertPos, editTgaListWidget.resultValueInfo)
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.tgaListListWidget.clear()
            self.tgaListListWidget.addItems(displayTgaList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def deleteFunc(self):
        msg = textSetting.textList["infoList"]["I25"].format(self.selectIndex + 1)
        result = mb.askokcancel(title=textSetting.textList["warning"], message=msg, icon="warning")
        if result == mb.OK:
            self.tgaList.pop(self.selectIndex)
            displayTgaList = self.setListboxInfo(self.tgaList)
            self.tgaListListWidget.clear()
            self.tgaListListWidget.addItems(displayTgaList)
            self.dirtyFlag = True
            self.modifyButton.setEnabled(False)
            self.insertButton.setEnabled(False)
            self.deleteButton.setEnabled(False)


class EditTgaListWidget(QDialog):
    def __init__(self, parent, title, mode, item=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mode = mode
        self.font2 = QFont(textSetting.textList["font2"][0], textSetting.textList["font2"][1])
        self.integerValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+$"), self)
        self.numberValidator = QRegularExpressionValidator(QRegularExpression(r"^\d+(\.\d+)?$"), self)
        self.resultValueInfo = {}
        self.lineEditList = []
        self.insertPos = None

        # layout
        layout = QVBoxLayout(self)
        # layout - Label
        label = QLabel(textSetting.textList["infoList"]["I44"], font=self.font2)
        layout.addWidget(label)
        # layout - QGridLayout
        self.tgaInfoGridLayout = QGridLayout()
        layout.addLayout(self.tgaInfoGridLayout)

        for i in range(2):
            # layout - QGridLayout - tgaName1Label
            tgaNameLabel = QLabel("{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaLabel"], i + 1), font=self.font2)
            self.tgaInfoGridLayout.addWidget(tgaNameLabel, i, 0)
            # layout - QGridLayout - tgaName1LineEdit
            tgaNameLineEdit = QLineEdit(font=self.font2)
            self.lineEditList.append(tgaNameLineEdit)
            self.tgaInfoGridLayout.addWidget(tgaNameLineEdit, i, 1)

        for i in range(2):
            # layout - QGridLayout - tgaElementLabel
            tgaElementLabel = QLabel("{0}{1}".format(textSetting.textList["mdlBin"]["else"], i + 1), font=self.font2)
            self.tgaInfoGridLayout.addWidget(tgaElementLabel, 2 + i, 0)
            # layout - QGridLayout - tgaElementLineEdit
            tgaElementLineEdit = QLineEdit(font=self.font2)
            tgaElementLineEdit.setValidator(self.numberValidator)
            self.lineEditList.append(tgaElementLineEdit)
            self.tgaInfoGridLayout.addWidget(tgaElementLineEdit, 2 + i, 1)

        # layout - QGridLayout - QFrame (colspan=2)
        horizentalLine = QFrame()
        horizentalLine.setFrameShape(QFrame.Shape.HLine)
        horizentalLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.tgaInfoGridLayout.addWidget(horizentalLine, 4, 0, 1, 2)

        for i in range(4):
            # layout - QGridLayout - tgaElementLabel
            tgaElementLabel = QLabel("{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaB"], i + 1), font=self.font2)
            self.tgaInfoGridLayout.addWidget(tgaElementLabel, 5 + i, 0)
            # layout - QGridLayout - tgaElementLineEdit
            tgaElementLineEdit = QLineEdit(font=self.font2)
            tgaElementLineEdit.setValidator(self.integerValidator)
            self.lineEditList.append(tgaElementLineEdit)
            self.tgaInfoGridLayout.addWidget(tgaElementLineEdit, 5 + i, 1)

        # layout - QGridLayout - tgaElsePerLabel
        tgaElsePerLabel = QLabel(textSetting.textList["mdlBin"]["headerTgaPer"], font=self.font2)
        self.tgaInfoGridLayout.addWidget(tgaElsePerLabel, 9, 0)
        # layout - QGridLayout - tgaElementLineEdit
        tgaElsePerLineEdit = QLineEdit(font=self.font2)
        tgaElsePerLineEdit.setValidator(self.integerValidator)
        self.lineEditList.append(tgaElsePerLineEdit)
        self.tgaInfoGridLayout.addWidget(tgaElsePerLineEdit, 9, 1)

        if self.mode == "modify":
            valueList = [
                item["tgaInfo"][0],
                item["tgaInfo"][1],
                item["tgaInfo"][2],
                item["tgaInfo"][3],
                item["tgaElse"][0],
                item["tgaElse"][1],
                item["tgaElse"][2],
                item["tgaElse"][3],
                item["tgaElse"][4]
            ]
            for i, value in enumerate(valueList):
                self.lineEditList[i].setText("{0}".format(value))
        else:
            valueList = [
                "",
                "",
                float(0),
                float(0),
                0,
                0,
                0,
                0,
                0,
            ]
            for i, value in enumerate(valueList):
                self.lineEditList[i].setText("{0}".format(value))
            self.setInsertWidget(10)

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
        self.tgaInfoGridLayout.addWidget(horizentalLine, insertRow, 0, 1, 2)
        # layout - QGridLayout - insertLabel
        insertLabel = QLabel(textSetting.textList["mdlBin"]["posLabel"], font=self.font2)
        self.tgaInfoGridLayout.addWidget(insertLabel, insertRow + 1, 0)
        # layout - QGridLayout - insertCombo
        self.insertCombo = QComboBox(font=self.font2)
        self.insertCombo.addItems(textSetting.textList["mdlBin"]["posValue"])
        self.tgaInfoGridLayout.addWidget(self.insertCombo, insertRow + 1, 1)

    def validate(self):
        self.resultValueInfo = {}
        self.resultValueInfo["tgaInfo"] = []
        self.resultValueInfo["tgaElse"] = []
        for i, lineEdit in enumerate(self.lineEditList):
            if i in [0, 1]:
                elementName = "{0}{1}".format(textSetting.textList["mdlBin"]["headerTgaLabel"], i + 1)
                errorMsg = textSetting.textList["errorList"]["E139"].format(elementName)
                if not lineEdit.text():
                    mb.showerror(title=textSetting.textList["valueError"], message=errorMsg)
                    return False
                self.resultValueInfo["tgaInfo"].append(lineEdit.text())
            else:
                if not lineEdit.hasAcceptableInput():
                    mb.showerror(title=textSetting.textList["numberError"], message=textSetting.textList["errorList"]["E3"])
                    return
                if i in [2, 3]:
                    self.resultValueInfo["tgaInfo"].append(float(lineEdit.text()))
                else:
                    self.resultValueInfo["tgaElse"].append(int(lineEdit.text()))

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
        self.smfList = copy.deepcopy(decryptFile.smfList)
        self.wavList = copy.deepcopy(decryptFile.wavList)
        self.tgaList = copy.deepcopy(decryptFile.tgaList)

        # layout
        layout = QVBoxLayout(self)
        # listLayout
        listLayout = QGridLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(listLayout)
        # listLayout - imageList
        self.imageSimpleList = ImageListWidget(textSetting.textList["mdlBin"]["imgInfo"], self.imgList, decryptFile.ver)
        listLayout.addWidget(self.imageSimpleList, 0, 0)
        # listLayout - imageSizeList
        self.imageSizeSimpleList = ImageSizeListWidget(textSetting.textList["mdlBin"]["imgSizeInfo"], self.imgSizeList)
        listLayout.addWidget(self.imageSizeSimpleList, 0, 1)
        # listLayout - smfList
        self.smfSimpleList = SmfNameListWidget(textSetting.textList["mdlBin"]["smfInfo"], self.smfList)
        listLayout.addWidget(self.smfSimpleList, 0, 2)
        # listLayout - wavList
        self.wavSimpleList = WavListWidget(textSetting.textList["mdlBin"]["seInfo"], self.wavList)
        listLayout.addWidget(self.wavSimpleList, 0, 3)
        ###
        if decryptFile.ver != 1:
            # listLayout - tgaList
            self.tgaSimpleList = TgaListWidget(textSetting.textList["mdlBin"]["tgaInfo"], self.tgaList)
            self.tgaSimpleList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            listLayout.addWidget(self.tgaSimpleList, 1, 0, 1, 4)

        # layout - QDialogButtonBox
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def validate(self):
        result = mb.askokcancel(title=textSetting.textList["warning"], message=textSetting.textList["infoList"]["I7"], icon="warning")
        if result == mb.OK:
            newImgList = self.imageSimpleList.imgList
            newImgSizeList = self.imageSizeSimpleList.imgSizeList
            newSmfList = self.smfSimpleList.smfList
            newWavList = self.wavSimpleList.wavList
            if self.decryptFile.ver != 1:
                newTgaList = self.tgaSimpleList.tgaList
            else:
                newTgaList = self.tgaList

            if not self.decryptFile.saveHeader(newImgList, newImgSizeList, newSmfList, newWavList, newTgaList):
                self.decryptFile.printError()
                mb.showerror(title=textSetting.textList["saveError"], message=textSetting.textList["errorList"]["E4"])
                return False
            return True

    def accept(self):
        ret = False
        ret |= self.imageSimpleList.dirtyFlag
        ret |= self.imageSizeSimpleList.dirtyFlag
        ret |= self.smfSimpleList.dirtyFlag
        ret |= self.wavSimpleList.dirtyFlag
        if self.decryptFile.ver != 1:
            ret |= self.tgaSimpleList.dirtyFlag

        if ret:
            if not self.validate():
                return
            super().accept()
            mb.showinfo(title=textSetting.textList["success"], message=textSetting.textList["infoList"]["I8"])
        else:
            super().accept()
