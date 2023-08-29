from typing import Optional, Union, Tuple
from vkbottle import ABCRule, Bot
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from config import GROUP_ID, TOKEN, STUFF_ADMIN_ID, PREFIXES
from database.sql_interface import Connection

bot = Bot(token=TOKEN)
database = Connection('database/database.db')

DEFAULT_ALIASES = ["Command", "command"]


class HandleCommand(ABCRule[BaseMessageMin]):
    def __init__(
            self,
            command_aliases: Optional[Tuple[str]] = None,
            prefixes: Optional[Tuple[str]] = None,
            arg_count=0
    ):
        self.prefixes = prefixes or PREFIXES
        self.command_aliases = command_aliases or DEFAULT_ALIASES
        self.args_count = arg_count
        self.sep = " "

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        text = message.text

        for prefix in self.prefixes:
            for command_text in self.command_aliases:
                command_length = len(prefix + command_text)
                command_length_with_sep = command_length + len(self.sep)
                if text.lower().startswith((prefix + command_text).lower()):
                    argstxt = message.text[command_length_with_sep:]
                    if argstxt != "":
                        args = argstxt.split(self.sep)
                    else:
                        args = []
                    if len(args) == self.args_count and all(args):
                        return {"args": args}

                    else:
                        return False

        return False


class AnswerCommand(ABCRule[BaseMessageMin]):
    def __init__(self, use_reply: bool = False, use_fwd: bool = False):
        self.use_reply = use_reply
        self.use_fwd = use_fwd

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        # Может быть упрощено.
        if message.reply_message is not None:
            if self.use_reply:
                return True
        else:
            if not self.use_reply:
                return True

        if message.fwd_messages is not None:
            if self.use_fwd:
                return True
        else:
            if not self.use_fwd:
                return True

        return False


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
            return True

        except Exception as error:
            print("Rule aborted command completion:", error)
            message.deleted = False
            return False


class CheckPermission(ABCRule[BaseMessageMin]):

    def __init__(self, access_to: int = 0):
        self.access_to = access_to

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id
        initiator_id = message.from_id

        if initiator_id == STUFF_ADMIN_ID:
            return True

        if database.get_permission(peer_id=peer_id, user_id=initiator_id) >= self.access_to:
            return True

        return False


class IgnorePermission(ABCRule[BaseMessageMin]):

    def __init__(self, ignore_from: int = 0, mode: str = "Target"):
        self.ignore_from = ignore_from
        self.mode = mode

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        if self.mode == "TARGET":
            if message.reply_message:
                target_id = message.reply_message.from_id

                if target_id == STUFF_ADMIN_ID:
                    return True

                if database.get_permission(peer_id=peer_id, user_id=target_id) < self.ignore_from:
                    return True

            elif message.fwd_messages:
                for msg in message.fwd_messages:
                    target_id = msg.from_id

                    if target_id == STUFF_ADMIN_ID:
                        return True

                    if database.get_permission(peer_id=peer_id, user_id=target_id) < self.ignore_from:
                        return True

        elif self.mode == "SELF":
            initiator_id = message.from_id

            if initiator_id == STUFF_ADMIN_ID:
                return True

            if database.get_permission(peer_id=peer_id, user_id=initiator_id) < self.ignore_from:
                return True

        return False


class IgnoreMention(ABCRule[BaseMessageMin]):
    def __init__(self, ignore_from: int = 0):
        self.ignore_from = ignore_from

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        text = message.text
        screen_name = text[text.find("[") + 1:text.find("|")].replace("id", "")
        uid = await bot.api.users.get(screen_name)
        if uid:
            target_id = uid[0].id

            if target_id == STUFF_ADMIN_ID:
                return True

            if database.get_permission(peer_id=peer_id, user_id=target_id) < self.ignore_from:
                return True

        return False


class HandleIn(ABCRule[BaseMessageMin]):

    def __init__(self, handle_log: bool = False, handle_chat: bool = False, send_respond=True):
        self.handle_log = handle_log
        self.handle_chat = handle_chat
        self.send_respond = send_respond

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id
        destination = "LOG"

        if database.get_conversation(peer_id=peer_id, destination=destination):
            if self.handle_log:
                return True

            else:
                if self.send_respond:
                    title = f"Отказ в исполнении команды. Команда не может быть использована в лог-чате."
                    await message.answer(title)
                return False

        destination = "CHAT"
        if database.get_conversation(peer_id=peer_id, destination=destination):
            if self.handle_chat:
                return True

            else:
                if self.send_respond:
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
