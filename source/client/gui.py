from threading import Thread

from PySide2.QtWidgets import QApplication, QLabel, QTreeView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
import PySide2.QtCore


class UserInterfaceHandler(Thread):
    def __init__(self, data_source):
        Thread.__init__(self)
        self.data_source = data_source
        self.user_interface = None
        self.qt_app = None

    def run(self):
        self.qt_app = QApplication()
        self.user_interface = UserInterface(self.data_source)

        self.qt_app.exec_()


class UserInterface:
    def __init__(self, data_source):
        self.path = "main_window.ui"
        self.main_window = QUiLoader().load(self.path)
        self.pi_connection_status_widget = self.main_window.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.main_window.findChild(QLabel, "server_connection_status")

        self.data_tree_model = QStandardItemModel()
        self.data_tree_view = self.main_window.findChild(QTreeView, "tree_view")
        self.set_data_source(self.data_tree_view, self.data_tree_model, data_source)
        self.format_model_table()

        self.main_window.show()

    def format_model_table(self):
        self.data_tree_model.setHeaderData(0, PySide2.QtCore.Qt.Horizontal, "Sensor")
        self.data_tree_model.setHeaderData(1, PySide2.QtCore.Qt.Horizontal, "Min. Value")
        self.data_tree_model.setHeaderData(2, PySide2.QtCore.Qt.Horizontal, "Max Value")

    def set_data_source(self, view, model, source):
        view.setModel(model)

        for module in source:
            top_row = QStandardItem(module.name)
            for input in module.gpio_inputs:
                sensor = QStandardItem(str(input))
                top_row.appendRow(sensor)

            model.appendRow(top_row)

        """
        for item in source:
            item = QStandardItem(item)
            root_item.appendRow(item)
            root_item = item
        """

    def update_data(self, new_data):
        pass



