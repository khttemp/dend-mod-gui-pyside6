from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt


class CustomMessageBox():
    OK = QMessageBox.StandardButton.Ok
    YES = QMessageBox.StandardButton.Yes
    NO = QMessageBox.StandardButton.No
    CANCEL = QMessageBox.StandardButton.Cancel

    def __init__(self):
        self.msg = None

    def makeMessageBox(self, title, message):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(message)
        self.msg.setWindowFlags((self.msg.windowFlags() & ~Qt.WindowMinMaxButtonsHint) | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

    def showinfo(self, title, message):
        self.makeMessageBox(title, message)
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.exec()

    def showwarning(self, title, message):
        self.makeMessageBox(title, message)
        self.msg.setIcon(QMessageBox.Icon.Warning)
        self.msg.exec()

    def showerror(self, title, message):
        self.makeMessageBox(title, message)
        self.msg.setIcon(QMessageBox.Icon.Critical)
        self.msg.exec()

    def askokcancel(self, title, message):
        self.makeMessageBox(title, message)
        self.msg.setIcon(QMessageBox.Icon.Question)
        self.msg.setStandardButtons(self.OK | self.CANCEL)
        return self.msg.exec()

    def askyesno(self, title, message):
        self.makeMessageBox(title, message)
        self.msg.setIcon(QMessageBox.Icon.Question)
        self.msg.setStandardButtons(self.YES | self.NO)
        return self.msg.exec()
