from table.table_model import TableModel

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableView


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 400)
        self._model = TableModel()
        layout = QVBoxLayout(self)
        self._table_view = QTableView()
        layout.addWidget(self._table_view)

    def set_data(self, data):
        self._model.set_data(data)
        self._table_view.setModel(self._model)
