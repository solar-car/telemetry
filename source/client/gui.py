from PySide2.QtWidgets import QApplication, QLabel, QTreeView

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem


class UserInterface:
    def __init__(self, modules):
        #  View widgets
        self.qt_app = QApplication()
        self.main_window = QUiLoader().load("main_window.ui")
        self.pi_connection_status_widget = self.main_window.findChild(QLabel, "pi_connection_status")
        self.server_connection_status_widget = self.main_window.findChild(QLabel, "server_connection_status")

        self.tree_model = TreeModel(modules)
        self.tree_model.index(1,1)

        self.tree_view = self.main_window.findChild(QTreeView, "tree_view")
        self.tree_view.setModel(self.tree_model)
        self.tree_view.expandAll()
        self.main_window.show()

        self.qt_app.exec_()


    def update_model(self, data):
        pass


class TreeModel(QAbstractItemModel):
    num_columns = 5

    def __init__(self, modules):
        QAbstractItemModel.__init__(self)
        self.root_item = TreeItem()
        self._initialize_data(modules)

    def data(self, qt_index, role=Qt.DisplayRole):
        if not qt_index.isValid() or role != Qt.DisplayRole:
            return None
        else:
            return qt_index.internalPointer().columns[qt_index.column()]

    def index(self, row, column, qt_parent_index=QModelIndex()):
        if not self.hasIndex(row, column, qt_parent_index):
            return QModelIndex()
        if not qt_parent_index.isValid():
            parent = self.root_item
        else:
            parent = qt_parent_index.internalPointer()
        child = parent.children[row]
        if child:
            return self.createIndex(row, column, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child = index.internalPointer()
        parent = child.parent
        if parent == self.root_item:
            return QModelIndex()

        return self.createIndex(parent.row, 0, parent)

    def rowCount(self, qt_parent_index=QModelIndex()):
        if qt_parent_index.column() > 0:
            return 0

        if not qt_parent_index.isValid():
            parent = self.root_item
        else:
            parent = qt_parent_index.internalPointer()

        return len(parent.children)

    def columnCount(self, qt_parent_index=QModelIndex()):
        return self.num_columns

    def _initialize_data(self, modules):
        pass


class TreeItem:
    def __init__(self, parent=None, data=("a", "a", "a", "a")):
        assert len(data) == TreeModel.num_columns - 1, "Invalid column data length."
        self.column_data = [item for item in data]
        self.parent = parent
        self.children = []  # One-dimensional data structure that contains all sub-items
