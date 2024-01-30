"""File describing classes of custom events.
"""
import logging
from enum import Enum
from datetime import datetime
from vk_api import VkApi



VK_GROUP_ID_DELAY = 2000000000


class EventType(Enum):
    """Enumerate list of vk event types.
    Extended with custom types.
    """
    # vk base event types
    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGE_EVENT = 'message_event'

    MESSAGE_TYPING_STATE = 'message_typing_state'

    MESSAGE_ALLOW = 'message_allow'

    MESSAGE_DENY = 'message_deny'

    PHOTO_NEW = 'photo_new'

    PHOTO_COMMENT_NEW = 'photo_comment_new'
    PHOTO_COMMENT_EDIT = 'photo_comment_edit'
    PHOTO_COMMENT_RESTORE = 'photo_comment_restore'

    PHOTO_COMMENT_DELETE = 'photo_comment_delete'

    AUDIO_NEW = 'audio_new'

    VIDEO_NEW = 'video_new'

    VIDEO_COMMENT_NEW = 'video_comment_new'
    VIDEO_COMMENT_EDIT = 'video_comment_edit'
    VIDEO_COMMENT_RESTORE = 'video_comment_restore'

    VIDEO_COMMENT_DELETE = 'video_comment_delete'

    WALL_POST_NEW = 'wall_post_new'
    WALL_REPOST = 'wall_repost'

    WALL_REPLY_NEW = 'wall_reply_new'
    WALL_REPLY_EDIT = 'wall_reply_edit'
    WALL_REPLY_RESTORE = 'wall_reply_restore'

    WALL_REPLY_DELETE = 'wall_reply_delete'

    BOARD_POST_NEW = 'board_post_new'
    BOARD_POST_EDIT = 'board_post_edit'
    BOARD_POST_RESTORE = 'board_post_restore'

    BOARD_POST_DELETE = 'board_post_delete'

    MARKET_COMMENT_NEW = 'market_comment_new'
    MARKET_COMMENT_EDIT = 'market_comment_edit'
    MARKET_COMMENT_RESTORE = 'market_comment_restore'

    MARKET_COMMENT_DELETE = 'market_comment_delete'

    GROUP_LEAVE = 'group_leave'

    GROUP_JOIN = 'group_join'

    USER_BLOCK = 'user_block'

    USER_UNBLOCK = 'user_unblock'

    POLL_VOTE_NEW = 'poll_vote_new'

    GROUP_OFFICERS_EDIT = 'group_officers_edit'

    GROUP_CHANGE_SETTINGS = 'group_change_settings'

    GROUP_CHANGE_PHOTO = 'group_change_photo'

    VKPAY_TRANSACTION = 'vkpay_transaction'

    # custom event types
    CHAT_INVITE_USER = "chat_invite_user"
    CHAT_KICK_USER = "chat_kick_user"



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



class ChatEvent(BaseEvent):
    """Custom inchat action event.
    """


class ButtonEvent(BaseEvent):
    """Custom callback button event.
    """
