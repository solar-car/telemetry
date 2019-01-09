from PySide2.QtWidgets import QApplication, QLabel, QTreeView

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QTreeWidget, QMainWindow, QTreeWidgetItem


class UserInterface:
    def __init__(self, modules):
        self.qt_app = QApplication()
        self.context = QUiLoader().load("main_window.ui")

        #  References to widgets defined in the .ui file
        self.pi_connection_status_widget = self.context.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.context.findChild(QLabel, "server_connection_status")
        self.module_tree_widget = self.context.findChild(QTreeWidget, "module_tree")
        print(self.module_tree_widget)
        self.initialize_module_tree(modules)

        self.context.show()

        self.qt_app.exec_()

    def initialize_module_tree(self, module_data):
        self.module_tree_widget.setColumnCount(5)
        self.module_tree_widget.setHeaderLabels(["Sensor", "Value", "Min", "Max", "Status"])
        for module in module_data:
            tree_item = QTreeWidgetItem([module.name, "debug", "debug", "debug", "debug"])
            self.module_tree_widget.addTopLevelItem(tree_item)
            for sensor in module.sensors:
                sub_tree_item = QTreeWidgetItem([sensor, "a", "a", "a", "a"])
                tree_item.addChild(sub_tree_item)

    def update_module_tree(self, module_data):
        pass


