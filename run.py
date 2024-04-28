from common.logger import Logger
from gui.recommender_gui import RecommenderGui


def main():
    app = RecommenderGui(Logger.DEBUG)
    app.run()


if __name__ == "__main__":
    main()
