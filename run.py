from common.logger import Logger
from query.query_kaggle import QueryKaggle

LOGGER = Logger('main')


def run():
    LOGGER.info("Running movie recommendation app")

    query = QueryKaggle(log_level=Logger.DEBUG)
    query.execute()
    LOGGER.error("done query?")


if __name__ == "__main__":
    run()
