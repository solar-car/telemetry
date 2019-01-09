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
        self.initialize_module_tree(modules)
        self.update_module_tree(modules)

        self.context.show()

        self.qt_app.exec_()

    def initialize_module_tree(self, module_data):
        self.module_tree_widget.setColumnCount(5)
        self.module_tree_widget.setHeaderLabels(["Sensor", "Value", "Min", "Max", "Status"])
        for module in module_data:
            tree_item = QTreeWidgetItem([module.name, "", "", "", ""])
            self.module_tree_widget.addTopLevelItem(tree_item)
            for sensor in module.sensors:
                sub_tree_item = QTreeWidgetItem([sensor, "debug", "debug", "debug", "debug"])
                tree_item.addChild(sub_tree_item)

    def update_module_tree(self, module_data):
        root = self.module_tree_widget.invisibleRootItem()
        modules = self.iterate_over_subitems(root)
        for module in modules:
            sensors = self.iterate_over_subitems(module)
            for sensor in sensors:
                sensor.setData(0, Qt.ItemDataRole.DisplayRole, "test")

    def iterate_over_subitems(self, item):
        subitems = []
        for index in range(item.childCount()):
            subitems.append(item.child(index))

        return subitems



