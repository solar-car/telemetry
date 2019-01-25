from threading import Thread

from PySide2.QtWidgets import QApplication, QLabel, QTreeView

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QTreeWidget, QMainWindow, QTreeWidgetItem, QHeaderView, QAction


class UserInterface(Thread):
    def __init__(self, modules):
        Thread.__init__(self)
        self.qt_app = QApplication()
        self.context = QUiLoader().load("Data/main_window.ui")

        #  References to widgets defined in the .ui file
        self.pi_connection_status_widget = self.context.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.context.findChild(QLabel, "server_connection_status")
        self.module_tree_widget = self.context.findChild(QTreeWidget, "module_tree")
        self.initialize_module_tree(modules)
        self.update_module_tree(modules)

        self.menu_readme_action = self.context.findChild(QAction, "open_readme")
        self.menu_readme_action.triggered.connect(MenuActions.action_open_readme)

        self.context.show()

        self.qt_app.exec_()

    def initialize_module_tree(self, module_data):
        self.module_tree_widget.setColumnCount(5)
        self.module_tree_widget.setHeaderLabels(["Sensor", "Value", "Min", "Max", "Status"])

        header = self.module_tree_widget.header()

        for module in module_data:
            tree_item = QTreeWidgetItem([module.name, "", "", "", ""])
            self.module_tree_widget.addTopLevelItem(tree_item)
            tree_item.setExpanded(True)
            for sensor in module.sensors:
                sub_tree_item = QTreeWidgetItem()
                if type(sensor.value) == int:
                    sub_tree_item = QTreeWidgetItem([sensor, str(sensor.value), str(sensor.value), str(sensor.value), ""])
                elif type(sensor.value) == str:
                    sub_tree_item = QTreeWidgetItem([sensor, sensor.value, "", "", ""])
                sensor.gui_reference = sub_tree_item
                tree_item.addChild(sub_tree_item)

    def update_module_tree(self, module_data):
        for module in module_data:
            for sensor in module.sensors:
                sensor.gui_reference.setData(1, Qt.ItemDataRole.DisplayRole, str(sensor.value))
                if type(sensor.value) == int:
                    if sensor.value < int(sensor.gui_reference.data(2, Qt.ItemDataRole.DisplayRole)):
                        sensor.gui_reference.setData(2, Qt.ItemDataRole.DisplayRole, str(sensor.value))

                    elif sensor.value > int(sensor.gui_reference.data(3, Qt.ItemDataRole.DisplayRole)):
                        sensor.gui_reference.setData(3, Qt.ItemDataRole.DisplayRole, str(sensor.value))
                sensor.gui_reference.setData(4, Qt.ItemDataRole.DisplayRole, sensor.status)

    def iterate_over_subitems(self, item):
        subitems = []
        for index in range(item.childCount()):
            subitems.append(item.child(index))

        return subitems


class MenuActions:
    def action_open_readme(self):
        pass

    def action_open_github_repo(self):
        pass

    def action_open_settings(self):
        pass