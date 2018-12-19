from threading import Thread

from PySide2.QtWidgets import QApplication, QLabel, QTextBrowser, QTableWidget, QTableWidgetItem, QHeaderView
from PySide2.QtUiTools import QUiLoader


class UserInterfaceHandler(Thread):
    def __init__(self, master):
        Thread.__init__(self)
        self.master = master
        self.user_interface = None
        self.qt_app = None

    def run(self):
        self.qt_app = QApplication()
        self.user_interface = UserInterface(self)

        self.qt_app.exec_()


class UserInterface:
    def __init__(self, handler):
        self.handler = handler
        self.main_window = QUiLoader().load("gui/main_window.ui")
        self.pi_connection_status_widget = self.main_window.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.main_window.findChild(QLabel, "server_connection_status")
        self.warning_display_widget = self.main_window.findChild(QTextBrowser, "warning_display")
        self.data_table_widget = self.main_window.findChild(QTableWidget, "data_table")
        self.data_table_widget.setColumnCount(4)
        self.data_table_widget.setRowCount(4)

        self.horizontal_header = self.data_table_widget.horizontalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

        self.main_window.show()

    def populate_data_table(self, module_data):
        for row_index, module in enumerate(module_data):
            for column_index, value in enumerate(module):
                table_item = QTableWidgetItem(f"Label:\n{value}")
                self.data_table_widget.setItem(row_index, column_index, table_item)





