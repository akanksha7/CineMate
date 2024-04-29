import sys
import argparse

from common.logger import Logger
from gui.recommender_gui import RecommenderGui
from PyQt5.QtWidgets import QApplication


def _parse_args():
    parser = argparse.ArgumentParser(description="Recommender Application")
    parser.add_argument(
        "-l", "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default="debug",
        help="Set the logger level (default: DEBUG)",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    log_level = getattr(Logger, args.log_level.upper())
    app = QApplication(sys.argv)
    window = RecommenderGui(log_level)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
