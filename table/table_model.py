import pandas as pd

from PyQt5.QtCore import Qt, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data=pd.DataFrame()):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.index)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def set_data(self, data):
        self._data = data

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if 0 <= row < self.rowCount() and 0 <= col < self.columnCount():
                return str(self._data.iloc[row, col])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section]) if section < len(self._data.columns) else None
            elif orientation == Qt.Vertical:
                return str(section + 1) if section < self.rowCount() else None
        return None
