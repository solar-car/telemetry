import sys
from PySide2.QtCore import SIGNAL, QObject
from PySide2.QtWidgets import QApplication, QLabel, QTableView
from PySide2.QtSql import QSqlRelationalTableModel


class UserInterface:
    def __init__(self):
        self.back_end = BackEnd()
        self.front_end = FrontEnd(self.back_end)

    def update(self, data):
        self.back_end.update_data(data)
        self.front_end.refresh()


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