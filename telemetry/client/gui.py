from threading import Thread

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt
import PySide2.QtWidgets as Widgets

from common.thread_handler import Subscriber


class UserInterface(Thread, Subscriber):
    def __init__(self, context, modules_init):
        Thread.__init__(self)
        self.context = context
        self.thread_handler = context.thread_handler
        self.state_handler = context.state_handler
        self.cached_state_handler = None  # Safe to access freely
        self.modules_init = modules_init
        self.settings = context.state_handler.settings

    # Workaround instead of initializing in __init__ to reconcile Python's threading API and QT
    def initialize_qt(self):
        self.qt_app = Widgets.QApplication()
        self.qt_app.aboutToQuit.connect(self.state_handler.quit)

        # Getting reference to GUI items from main_window.ui so that they can be manipulated programmatically
        self.main_window = QUiLoader().load("client/main_window.ui")
        self.connection_status_widget = self.main_window.findChild(Widgets.QLabel, "connection_status")

        self.module_tree_widget = self.main_window.findChild(Widgets.QTreeWidget, "module_tree")
        self.menu_readme_action = self.main_window.findChild(Widgets.QAction, "open_readme")
        self.menu_readme_action.triggered.connect(lambda: print("menu action triggered placeholder"))
        self.main_window.show()

        # Getting reference to GUI items from password_box.ui so that they can be manipulated programmatically
        self.password_box = QUiLoader().load("client/password_box.ui")
        self.password_entry = self.password_box.findChild(Widgets.QLineEdit, "password_entry")
        self.enter_button = self.password_box.findChild(Widgets.QPushButton, "enter_button")
        self.enter_button.clicked.connect(self.handle_password_entry)
        self.password_box.show()

        self.initialize_module_tree(self.modules_init)
        self.update_module_tree(self.modules_init)

    def run(self):
        self.initialize_qt()
        self.thread_handler.add_task(self.context.initialize_networking)
        self.qt_app.exec_()

    def external_update(self, updated_state):
        self.cached_state_handler = updated_state
        self.update_module_tree(self.cached_state_handler.modules)
        self.update_extra_gui_elements()
        print("external update triggered")

    # Setting up the initial data and dimensions of the QTreeWidget for displaying module and sensor data
    def initialize_module_tree(self, module_data):
        # Set the data for the column headers
        self.module_tree_widget.setColumnCount(5)
        self.module_tree_widget.setHeaderLabels(["Sensor", "Value", "Min", "Max", "Status"])

        # Create a new blank root tree item for each module that acts as a container for sensor sub-items
        for module in module_data:
            tree_item = Widgets.QTreeWidgetItem([module.name, "", "", "", ""])
            self.module_tree_widget.addTopLevelItem(tree_item)
            tree_item.setExpanded(True)

            # Create a tree sub-item for each sensor that displays its relevant data
            for sensor in module.sensors:
                sub_tree_item = Widgets.QTreeWidgetItem()

                # Convert int values to string since QT only accepts data as a string
                if type(sensor.value) == int:
                    sub_tree_item = Widgets.QTreeWidgetItem([sensor, str(sensor.value), str(sensor.value), str(sensor.value), ""])
                elif type(sensor.value) == str:
                    sub_tree_item = Widgets.QTreeWidgetItem([sensor, sensor.value, "", "", ""])

                sensor.gui_reference = sub_tree_item
                tree_item.addChild(sub_tree_item)

    # Update each item in the QTreeWidget with new data
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

    def update_extra_gui_elements(self):
        if self.cached_state_handler.connection_status:
            self.connection_status_widget.setText("Connected")
            self.connection_status_widget.setStyleSheet("color: green")
        elif not self.cached_state_handler.connection_status:
            self.connection_status_widget.setText("Not connected")
            self.connection_status_widget.setStyleSheet("color: red")

    # Return the entered password value in the password box and close it
    def handle_password_entry(self):
        data = self.password_entry.text()
        self.password_box.close()
        self.thread_handler.add_task(self.state_handler.update_credentials, data)
