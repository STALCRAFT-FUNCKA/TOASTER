from typing import List, Optional, Union
from vkbottle import ABCRule, Bot
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from config import GROUP_ID, TOKEN
from DataBase.interface import Connection

bot = Bot(token=TOKEN)
database = Connection('DataBase/database.db')

DEFAULT_PREFIXES = ["!", "/"]
DEFAULT_ALIASES = ["Command", "command"]


class HandleCommand(ABCRule[BaseMessageMin]):
    def __init__(
            self,
            command_aliases: Optional[List[str]] = None,
            prefixes: Optional[List[str]] = None,
            arg_count = 0,
            may_url = False
    ):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_aliases = command_aliases or DEFAULT_ALIASES
        self.args_count = arg_count
        self.sep = " "
        self.may_url = may_url

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        text = message.text

        # Тут игнорируются аргументы, если команда имеет 0 аргументов в настройке
        if self.args_count == 0 and self.sep in text:
            cut = message.text.find(self.sep)
            text = text[0:cut]

        for prefix in self.prefixes:
            for command_text in self.command_aliases:
                command_length = len(prefix + command_text)
                command_length_with_sep = command_length + len(self.sep)
                if text.lower().startswith((prefix + command_text).lower()):
                    # Если команда имеет 0 аргументов в настройке
                    if not self.args_count and len(text) == command_length:
                        return True

                    elif self.args_count:
                        args = message.text[command_length_with_sep:].split(self.sep)
                        if len(args) == self.args_count and all(args):
                            return {"args": args}

                        else:
                            return False

        return False

class AnswerCommand(ABCRule[BaseMessageMin]):

    def __init__(self, use_reply: bool = None, use_fwd: bool = None):
        self.use_reply = use_reply or False
        self.use_fwd = use_fwd or False

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        # Может быть упрощено.
        keyOne, keyTwo = False, False
        if message.reply_message:
            keyOne = True

        if message.fwd_messages:
            keyTwo = True

        return keyOne == self.use_reply or keyTwo == self.use_fwd

class CollapseCommand(ABCRule[BaseMessageMin]):
    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        try:
            await bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=message.peer_id,
                cmids=message.conversation_message_id,
                delete_for_all=True
            )
            message.deleted = True
            return  True
        except Exception:
            message.deleted = False
            return False

class CheckPermission(ABCRule[BaseMessageMin]):

    def __init__(self, access_to: int = 0):
        self.access_to = access_to

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        PeerID = message.peer_id
        UserID = message.from_id

        # TODO: VK admin
        if database.get_permission(peer_id=PeerID, user_id=UserID) >= self.access_to:
            return True

        return False

class IgnorePermission(ABCRule[BaseMessageMin]):

    def __init__(self, ignore_from: int = 0, mode:str = "Target"):
        self.ignore_from = ignore_from
        self.mode = mode

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        PeerID = message.peer_id

        if self.mode == "TARGET":
            if message.reply_message:
                UserID = message.reply_message.from_id
                # TODO: VK admin
                if database.get_permission(peer_id=PeerID, user_id=UserID) < self.ignore_from:
                    return True

            elif message.fwd_messages:
                for msg in message.fwd_messages:
                    UserID = msg.from_id
                    # TODO: VK admin
                    if database.get_permission(peer_id=PeerID, user_id=UserID) < self.ignore_from:
                        return True

        elif self.mode == "SELF":
            UserID = message.from_id
            if database.get_permission(peer_id=PeerID, user_id=UserID) < self.ignore_from:
                return True

        return False

class HandleIn(ABCRule[BaseMessageMin]):

    def __init__(self, handle_log: bool = False, handle_chat: bool = False):
        self.handle_log = handle_log
        self.handle_chat = handle_chat

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id
        destination = "LOG"

        if database.get_conversation(peer_id=peer_id, destination=destination):
            if self.handle_log:
                return True

            else:
                title = f"Отказ в исполнении команды. Команда не может быть использована в лог-чате."
                await message.answer(title)
                return False

        destination = "CHAT"
        if database.get_conversation(peer_id=peer_id, destination=destination):
            if self.handle_chat:
                return True

            else:
                title = f"Отказ в исполнении команды. Команда не может быть использована в беседе."
                await message.answer(title)
                return False

        return True

class OnlyEnrolled(ABCRule[BaseMessageMin]):

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        if database.get_conversation(peer_id=peer_id, destination="LOG"):
                return True

        elif database.get_conversation(peer_id=peer_id, destination="CHAT"):
                return True

        else:
            title = f"Отказ в исполнении команды. Беседа не зарегистрирована."
            await message.answer(title)
            return False