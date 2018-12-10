import sys
from threading import Thread

from PySide2.QtCore import SIGNAL, QObject
from PySide2.QtWidgets import QApplication, QLabel, QTableView
from PySide2.QtSql import QSqlRelationalTableModel


class UserInterface(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.front_end = None
        self.back_end = None

    def update(self, data=None):
        self.back_end.update_data(data)
        self.front_end.refresh()

    def run(self):
        self.back_end = BackEnd()
        self.front_end = FrontEnd(self.back_end)

        while True:
            self.update()

class FrontEnd:
    def __init__(self, back_end):
        self.create_gui(back_end)

    def create_gui(self, back_end):
        app = QApplication()
        label = QLabel("Hello World")
        label.show()
        sys.exit(app.exec_())

    def refresh(self):
        pass


class BackEnd:
    def __init__(self):
        pass

    def update_data(self, data):
        pass