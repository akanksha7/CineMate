import os
import pandas as pd

from common.base_dataset import BaseDataset
from common.logger import Logger
from ui.ui_importwidget import Ui_ImportWidget

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog


class ImportWidget(QWidget):
    done = pyqtSignal(BaseDataset)

    def __init__(self, log_level=Logger.INFO):
        super().__init__()
        # Initialize ui
        self.ui = Ui_ImportWidget()
        self.ui.setupUi(self)

        # Setup logging
        self._log_level = log_level
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)

        # Connect signals
        self.ui.file.pressed.connect(self._open_file_browser)
        self.ui.startImport.pressed.connect(self._start_import)

    def _open_file_browser(self) -> None:
        """Open a file browser to select file."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.ui.label.setText(file_path)

    def _start_import(self) -> None:
        """Import clicked. Read the file and try to create a BaseDataset."""
        if os.path.isfile(self.ui.label.text()):
            try:
                # TODO should probably thread this because import files could be large
                dataset = BaseDataset(self.ui.label.text().split('/')[-1].split('.')[0])
                dataset.df = pd.read_csv(self.ui.label.text())
                self.done.emit(dataset)
                self.close()
            except Exception as e:
                self._logger.error(f"Unable to convert file to dataframe: {self.ui.label.text()}")
                self._logger.error(e)
        else:
            self._logger.info('Not a valid file path')
