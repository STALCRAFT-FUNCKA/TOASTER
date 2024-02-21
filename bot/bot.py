"""A file containing a description of the bot's main class with all its functions.
"""
import os
import logging
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent
)
from tools.event import BaseEvent
from .router import Router
from .handlers.commands import CommandHandler


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
    command_handler = None # if message text starts with COMMAND_PREFIX
    button_handler = None # if message contains payload

    def __init__(self):
        self.__create_session()
        self.__create_longpoll()
        self.__create_api()
        self.__init_handlers()


    def __init_handlers(self):
        #self.trigger_handler = TriggerHandler(self.api)
        self.command_handler = CommandHandler(self.api)
        #self.button_handler = ButtonHandler(self.api)


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


    def __handle_event(self, event: BaseEvent):
        """Processes an event received as input.
        By processing we mean the use of filters, 
        triggers, command recognition, etc.

        Args:
            event (BaseEvent): Base custom event.
        """
        # Handlers must be placed in order
        # logical descending
        handlers = {
            "message_new": (
                #self.trigger_handler,
                self.command_handler,
            ),
            "button_pressed": (
                # self.button_handler(event),
            )
        }

        interrupted = not all((
            handler(event) for handler in handlers[event.event_type]
        ))

        if interrupted:
            self.__logger.info(
                "Event handled successfully."
            )
        else:
            self.__logger.info(
                "The event did not trigger a single handler."
            )


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
