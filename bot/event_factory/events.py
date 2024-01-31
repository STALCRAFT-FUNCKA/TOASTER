"""File describing classes of custom events.
"""
import logging
from datetime import datetime
from vk_api import VkApi



VK_GROUP_ID_DELAY = 2000000000


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

    def __init__(self, raw_event: dict, api: VkApi):
        self.event_type = raw_event.get("type")
        self.event_id = raw_event.get("event_id")
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
        summary = ""
        separator = "-------------------------------------------------"

        summary += separator + "\n"
        for key, value in self.__dict__.items():
            summary += f"{key}: {value} \n"
        summary += separator

        return summary



class MessageEvent(BaseEvent):
    """Custom message event.
    """
    # message data
    from_id: int = None
    peer_id: int = None
    chat_id: int = None
    cmid: int = None
    timestamp: int = None
    datetime: str = None

    # message content
    text: str = None
    reply: dict = None # dcit form
    forward: list = None # list of dicts
    attachments: list = None # list of dicts
    action: dict = None
    payload: dict = None

    # additional
    from_name = None
    from_nickname: str = None
    peer_name = None

    def __init__(self, raw_event: dict, api: VkApi):
        super().__init__(raw_event, api)

        # building event fields
        self.__get_data(raw_event)
        self.__get_content(raw_event)
        self.__get_additionals()


    def __get_data(self, raw_event: dict):
        message = raw_event.get("object")
        if message is None:
            return

        message = message["message"]

        self.from_id = message.get("from_id")
        self.peer_id = message.get("peer_id")
        self.chat_id = self.peer_id - VK_GROUP_ID_DELAY
        self.cmid = message.get("conversation_message_id")
        self.timestamp = message.get("date")

        if self.timestamp:
            self.datetime = str(datetime.utcfromtimestamp(self.timestamp))


    def __get_content(self, raw_event: dict):
        message = raw_event.get("object")
        if message is None:
            super().logger.warning(
                "Unable to obtain message content." \
                "Missing event object." \
                "<%s|%s}>",
                super().event_id,
                super().event_type
            )
            return

        message = message["message"]

        self.text = message.get("text")
        self.reply = message.get("reply_message")
        self.forward = message.get("fwd_messages")
        self.attachments = message.get("attachments")
        self.action = message.get("action")
        self.action = message.get("payload")


    def __get_additionals(self):
        if super().api is not None:
            user_info = self.__get_userinfo()
            peer_info = self.__get_peerinfo()

            self.from_name = " ".join([
                user_info.get("first_name"),
                user_info.get("last_name")
            ])
            self.from_nickname = user_info.get("domain")
            self.peer_name = peer_info.GET("title")

        else:
            super().logger.warning(
                "Unable to obtain additional" \
                "information about event" \
                "<%s|%s}>." \
                "Missing API object.",
                super().event_id,
                super().event_type
            )


    def __get_userinfo(self):
        necessary_feilds = [
            "domain",
        ]
        user_info = super().api.users.get(
            user_ids=self.from_id,
            fields=necessary_feilds
        )
        if not user_info:
            user_info = {}
            super().logger.warning(
                "Unable to obtain user information." \
                "Bot don't have administrator rights or" \
                "user doesn't exist."
            )
        else:
            user_info = user_info[0]

        return user_info


    def __get_peerinfo(self):
        peer_info = super().api.messages.getConversationsById(
            peer_ids=self.peer_id
        )

        if peer_info.get("count") == 0:
            peer_info = {}
            super().logger.warning(
                "Unable to obtain conversation information." \
                "Bot don't have administrator rights or" \
                "conversation doesn't exist."
            )

        else:
            peer_info = peer_info["items"][0]["chat_settings"]

        return peer_info
