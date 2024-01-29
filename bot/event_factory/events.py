import logging
from vk_api import VkApi
from vk_api.longpoll import Event


class CustomEvent(object):
    """_summary_
    """
    # logger object
    __logger = logging.getLogger("TOASTER")

    # VK api object
    # It is necessary for receipt
    # an additional data of the events
    # and making actions with it
    __api: VkApi = None

    # Raw type of event. VkEventType()
    raw_type: int = None

    # Main event data
    user_id: int = None
    peer_id: int = None
    chat_id: int = None
    datetime: str = None

    # Additional event data
    user_name: str = None
    user_nickname: str = None
    peer_name: str = None

    def __init__(self, raw_event: Event, api: VkApi = None):
        # Setting api object
        self.__api = api

        # Saving original vk event type
        self.raw_type = raw_event.type

        # updating information
        self.user_id = raw_event.user_id
        self.peer_id = raw_event.peer_id
        self.chat_id = raw_event.chat_id
        self.datetime = str(raw_event.datetime)

        # Getting additional event data
        self.__get_additionals()

    def __get_additionals(self):
        if self.__api is not None:
            # parsing additional user info
            user_info = self.__get_userinfo()[0]
            self.user_name = " ".join(
                [
                    user_info["first_name"],
                    user_info["last_name"]
                ]
            )
            self.user_nickname = user_info["domain"]

            # parsing additional peer info
            peer_info = self.__get_peerinfo()
            self.peer_name = peer_info["title"]

        else:
            self.__logger.warning(
                "It was not possible to get additional information from the event."
                "Missing API object."
            )

    def __get_userinfo(self):
        necessary_feilds = [
            "domain",
        ]

        information = self.__api.users.get(
            user_ids=self.user_id,
            fields=necessary_feilds
        )

        return information

    def __get_peerinfo(self):
        information = self.__api.messages.getConversationsById(
            peer_ids=self.peer_id
        )
        information = information["items"][0]["chat_settings"]

        return information

    def _get_api(self):
        return self.__api

    def get_prnt(self) -> str:
        """
        Returns a string representation of the class's attribute dictionary in a convenient form.
        """
        summary = ""
        separator = "-------------------------------------------------\n"

        summary += separator
        for key, value in self.__dict__.items():
            summary += f"{key}: {value} \n"
        summary += separator

        return summary


class MessageEvent(CustomEvent):
    # Message id
    cmid: int = None

    # Message content
    attachments: dict = None
    reply_msg: int = None
    forward_msgs: list = None

    def __init__(self, raw_event: Event, api: VkApi = None):
        super().__init__(raw_event, api)

        self.__get_cmid(raw_event)
        self.__get_content()

    def __get_cmid(self, raw_event: Event):
        self.cmid = raw_event.message_id

    def __get_content(self):
        api = super()._get_api()
        msg = api.messages.getById(
            message_ids=self.cmid,
            extended=1
        )["items"][0]

        self.attachments = msg.get("attachments")
        self.forward_msgs = msg.get("fwd_messages")
        self.reply_msg = msg.get("reply_message")


class ButtonEvent(CustomEvent):
    payload = None
