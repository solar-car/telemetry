from threading import Thread

from PySide2.QtWidgets import QApplication, QLabel, QTreeView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader


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
        self.test = 0
        self.path = "main_window.ui"
        self.main_window = QUiLoader().load(self.path)
        self.pi_connection_status_widget = self.main_window.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.main_window.findChild(QLabel, "server_connection_status")

        self.data_tree_model = QStandardItemModel()
        self.data_tree_view = self.main_window.findChild(QTreeView, "tree_view")
        self.data_tree_view.setModel(self.data_tree_model)

        self.set_data_source(self.data_tree_model, data_source)

        self.main_window.show()

    def set_data_source(self, model, source):
        root_item = model.invisibleRootItem()

        for module in source:
            item = QStandardItem(str(self.test))
            root_item.appendRow(item)


        """
        for item in source:
            item = QStandardItem(item)
            root_item.appendRow(item)
            root_item = item
        """

    def update_data(self, new_data):
        pass



