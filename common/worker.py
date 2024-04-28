from PyQt5.QtCore import pyqtSignal, QObject, QRunnable


class WorkerSignals(QObject):
    finished = pyqtSignal()


class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.signals = WorkerSignals()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)
        self.signals.finished.emit()