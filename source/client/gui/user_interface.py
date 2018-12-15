import sys
from threading import Thread

from PySide2.QtCore import SIGNAL, QObject
from PySide2.QtWidgets import QApplication, QLabel, QTableView
from PySide2.QtSql import QSqlRelationalTableModel
from PySide2.QtUiTools import QUiLoader

class UserInterface(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.front_end = None
        self.back_end = None
        self.qt_app = None

    def update(self, data=None):
        self.back_end.update_data(data)
        self.front_end.refresh()

    def run(self):
        self.back_end = BackEnd()
        self.front_end = FrontEnd()


class FrontEnd:
    def __init__(self):
        self.main_window = QUiLoader().load("main_window.ui")


class BackEnd:
    def __init__(self):
        self.qt_app = QApplication()

    def start_app(self):
        self.qt_app.exec_()
