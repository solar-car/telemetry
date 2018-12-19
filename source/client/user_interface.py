from threading import Thread

from PySide2.QtWidgets import QApplication, QLabel, QTextBrowser, QTableWidget, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader


class UserInterfaceHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
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

        self.populate_data_table([[1, 2, 3]])

        self.main_window.show()

    def populate_data_table(self, modules):
        for row_index, module in enumerate(modules):
            for column_index, value in enumerate(module):
                print(value)
                table_item = QTableWidgetItem(value)
                self.data_table_widget.setItem(row_index, column_index, table_item)





