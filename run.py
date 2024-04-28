import sys

from common.logger import Logger
from gui.recommender_gui import RecommenderGui
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = RecommenderGui(Logger.DEBUG)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
