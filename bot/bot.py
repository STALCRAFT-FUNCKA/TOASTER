"""A file containing a description of the bot's main class with all its functions.
"""
import os
import logging
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent
)
from .event_factory import Router, BaseEvent


class Bot(object):
    """Bot main class.
    """
    # logger object
    __logger = logging.getLogger("TOASTER")

    # VK objects
    __session = None
    __longpoll = None
    api = None

    # Custom event factory
    factory = Router()

    # Event handlers
    trigger_handler = None # if message contains text, attachments,forwards or replies
    action_handler = None # if message contains action
    command_handler = None # if message text starts with COMMAND_PREFIX
    button_handler = None # if message contains payload

    def __init__(self):
        self.__create_session()
        self.__create_longpoll()
        self.__create_api()

    def __create_session(self):
        """Creates VK session with using group acces token.
        """
        self.__session = VkApi(
            token=os.getenv("TOASTER_DEV_TOKEN"),
            api_version="5.199"
        )
        self.__logger.info("Session created.")

    def __create_longpoll(self):
        """Creating connection to longpoll VK server with using VK session object.
        """
        self.__longpoll = VkBotLongPoll(
            vk=self.__session,
            wait=10,
            group_id=os.getenv("TOASTER_DEV_GROUPID")
        )
        self.__logger.info("Connected to longpoll server.")

    def __create_api(self):
        """Gets VK API object. Can be used to execute VK serverside queries.
        """
        self.api = self.__session.get_api()
        self.__logger.info("API object created.")

    def __fabricate_event(self, vk_event: VkBotEvent) -> BaseEvent:
        """The function accesses the router object, which selects according to the event type
        the desired custom event class, after which the function returns a new custom event.

        Args:
            vk_event (VkBotEvent): VK bot longpoll event.

        Returns:
            BaseEvent: Base custom event.
        """
        return self.factory(vk_event, self.api)

    def run(self):
        """Starts listening VK longpoll server.
        """
        self.__logger.info("Starting listening longpoll server...")
        for vk_event in self.__longpoll.listen():
            event = self.__fabricate_event(vk_event)
            if event is not None:
                self.__logger.info(
                    "New event recived: \n %s ", event.attr_str
                )

                self.__handle_event(event)

    @staticmethod
    def __handle_event(event: BaseEvent):
        """Processes an event received as input.
        By processing we mean the use of filters, 
        triggers, command recognition, etc.

        Args:
            event (BaseEvent): Base custom event.
        """
        if event:
            return
