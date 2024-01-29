"""
A file containing a description of the bot's main class with all its functions.
"""
import os
import logging
from vk_api import VkApi
from vk_api.longpoll import (
    VkLongPoll,
    Event
)
from .event_factory import (
    Router,
    CustomEvent
)


class Bot(object):
    """
    Bot main class.
    """
    __logger = logging.getLogger("TOASTER")

    __session = None
    __longpoll = None
    api = None

    factory = Router()

    def __create_session(self):
        """
        Creates VK session with using group acces token.
        """
        self.__session = VkApi(
            token=os.getenv("TOASTER_DEV_TOKEN"),
            api_version="5.199"
        )
        self.__logger.info("Session created.")

    def __create_longpoll(self):
        """
        Creating connection to longpoll VK server with using VK session object.
        """
        self.__longpoll = VkLongPoll(
            vk=self.__session,
            wait=10,
            group_id=os.getenv("TOASTER_DEV_GROUPID")
        )
        self.__logger.info("Connected to longpoll server.")

    def __create_api(self):
        """
        Gets VK API object. Can be used to execute VK serverside queries.
        """
        self.api = self.__session.get_api()
        self.__logger.info("API object created.")

    def __fabricate_event(self, raw_event: Event) -> CustomEvent:
        """
        The function accesses the router object, which selects according to the event type
        the desired custom event class, after which the function returns a new custom event.

        Args:
            raw_event (Event): VK longpoll event.

        Returns:
            CustomEvent: Base custom event.
        """
        return self.factory(raw_event, self.api)

    def __init__(self):
        self.__create_session()
        self.__create_longpoll()
        self.__create_api()

    def run(self):
        """
        Starts listening VK longpoll server.
        """
        self.__logger.info("Starting listening longpoll server...")
        for raw_event in self.__longpoll.listen():
            event = self.__fabricate_event(raw_event)
            if event is not None:
                self.__logger.info(
                    "New event recived: \n %s ", event.get_prnt()
                )
