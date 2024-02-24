import logging
from vk_api import VkApi
from tools import (
    timestamp,
    msk_now
)


class BaseEvent(object):
    """Custom description of an event coming from a longpoll server.
    """
    # VK api object
    # It is necessary for receipt
    # an additional data of the events
    # and making actions with it
    __api: VkApi = None

    # logger object
    __logger = logging.getLogger("TOASTER")

    # Event data
    event_id: str = None
    event_type: str = None
    event_raw: any = None
    ts: int = None
    datetime: str = None

    def __init__(self, raw_event: dict, api: VkApi):
        self.event_type = raw_event.get("type")
        self.event_id = raw_event.get("event_id")
        self.event_raw = raw_event

        self.ts = timestamp()
        self.datetime = msk_now()

        self.__api = api


    @property
    def logger(self):
        """Returns the logger object from the parent class.

        Returns:
            Logger: logger object.
        """
        return self.__logger


    @property
    def api(self):
        """Returns the VKontakte API object from the parent class.

        Returns:
            VkApi: vk api object.
        """
        return self.__api


    @property
    def attr_str(self):
        """Returns a string representation of the class's 
        attribute dictionary in a convenient form.
        """
        blacklisted_keys = (
            "_BaseEvent__api",
            "event_raw"
        )
        summary = ""
        separator = "-------------------------------------------------"

        for key, value in self.__dict__.items():
            if key not in blacklisted_keys:
                summary += f"{key}: {value} \n"
        summary += separator

        return summary
