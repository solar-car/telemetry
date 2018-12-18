from threading import Thread

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader


class UserInterface(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.front_end = None
        self.back_end = None
        self.qt_app = None

    def run(self):
        self.back_end = BackEnd()
        self.front_end = FrontEnd()
        self.back_end.start_app()


class FrontEnd:
    def __init__(self):
        self.main_window = QUiLoader().load("gui/main_window.ui")
        self.main_window.show()


class BackEnd:
    def __init__(self):
        self.qt_app = QApplication()

    def start_app(self):
        self.qt_app.exec_()
