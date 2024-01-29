"""
Main app file.
"""
import logging
from colorama import Fore
from bot import Bot

# Initializing logger
logger = logging.getLogger("TOASTER")

stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    Fore.RED + "[%(name)s | %(levelname)s | %(asctime)s] " + Fore.WHITE +"Message: %(message)s"
)
stream_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

logger.info("Log messages powered by \"logging\" module.")

# Initializing bot (TOASTER)
TOASTER = Bot()

if __name__ == "__main__":
    TOASTER.run()
