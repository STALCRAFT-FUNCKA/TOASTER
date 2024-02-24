from vk_api import VkApi
from tools.handler import ABCHandler
from db import DataBase


class BaseCommand(ABCHandler):
    """Command handler base class.
    """
    __permission_lvl = 0
    COMMAND_NAME = "None"

    def __init__(self, db: DataBase, api: VkApi):
        self.db = db
        self.api = api


    def log(self):
        """Sends a log of command execution
        in log-convs.
        """
        # TODO: write me


    @property
    def permission(self) -> int:
        """Returns the access level
        to execute the command.

        Returns:
            int: permission lvl.
        """
        return self.__permission_lvl
