import os
from PySide6.QtWidgets import QFileDialog

class CustomFileDialog():
    def __init__(self):
        self.dialog = QFileDialog()
        self.lastDir = ""

    def getOpenFileName(self, fileType, allow_multiple=False):
        self.dialog.setAcceptMode(QFileDialog.AcceptOpen)

        self.dialog.selectNameFilter("")
        self.dialog.setNameFilter(fileType)
        if self.lastDir:
            self.dialog.setDirectory(self.lastDir)

        if allow_multiple:
            self.dialog.setFileMode(QFileDialog.ExistingFiles)
        else:
            self.dialog.setFileMode(QFileDialog.ExistingFile)

        if self.dialog.exec():
            files = self.dialog.selectedFiles()

            if files:
                self.lastDir = os.path.dirname(files[0])

                if allow_multiple:
                    return files
                else:
                    file_path = files[0]
                    return file_path

        return None

    def getSaveFileName(self, filename, fileType):
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)

        self.dialog.selectNameFilter("")
        self.dialog.setNameFilter(fileType)
        if self.lastDir:
            self.dialog.setDirectory(self.lastDir)

        self.dialog.setFileMode(QFileDialog.ExistingFile)
        self.dialog.selectFile(filename)

        if self.dialog.exec():
            files = self.dialog.selectedFiles()
            if files:
                self.lastDir = os.path.dirname(files[0])
                return files[0]

        return None

    def getExistingDirectory(self):
        self.dialog.setAcceptMode(QFileDialog.AcceptOpen)

        self.dialog.setFileMode(QFileDialog.Directory)
        if self.lastDir:
            self.dialog.setDirectory(self.lastDir)

        if self.dialog.exec():
            files = self.dialog.selectedFiles()

            if files:
                self.lastDir = os.path.dirname(files[0])
                return files[0]

        return None
