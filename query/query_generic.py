from PyQt5.QtCore import pyqtSignal, QObject


class QueryGeneric(QObject):
    """Abstract class for all query implementations."""
    finalized = pyqtSignal(list, str, bool)

    def execute(self, **kwargs):
        raise NotImplementedError

    def finalize(self, name: str, merge: bool):
        raise NotImplementedError
