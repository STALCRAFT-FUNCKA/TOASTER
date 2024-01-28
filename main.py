import logging
from bot import Bot

logger = logging.getLogger("TOASTER")

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(name)s | %(levelname)s | %(asctime)s] Message: %(message)s")
stream_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

logger.info("Log messages powered by \"logging\" module.")

TOASTER = Bot()

if __name__ == "__main__":
    TOASTER.run()
