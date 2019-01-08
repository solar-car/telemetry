from PySide2.QtWidgets import QApplication, QLabel, QTreeView

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt as Qt


class UserInterfaceHandler:
    def __init__(self, module_data):
        self.qt_app = QApplication()
        self.user_interface = UserInterface(module_data)
        self.qt_app.exec_()


class UserInterface:
    def __init__(self, model):
        #  View widgets
        self.main_window = QUiLoader().load("main_window.ui")
        self.pi_connection_status_widget = self.main_window.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.main_window.findChild(QLabel, "server_connection_status")

        self.tree_view = self.main_window.findChild(QTreeView, "tree_view")
        self.main_window.show()



