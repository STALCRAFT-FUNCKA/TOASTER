from typing import Optional, Union, Tuple
from vkbottle import ABCRule, Bot
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from toaster_app.config import GROUP_ID, TOKEN, STAFF_ADMIN_ID, PREFIXES
from toaster_app.data import DataBase


class HandleCommand(ABCRule[BaseMessageMin]):
    def __init__(
            self,
            command_aliases: Optional[Tuple[str]] = None,
            prefixes: Optional[Tuple[str]] = None,
            arg_count=None
    ):
        self.prefixes = prefixes or PREFIXES
        self.command_aliases = command_aliases
        self.args_count = arg_count
        self.sep = " "

        self.bot = Bot(token=TOKEN)

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

                    if (len(args) == self.args_count or self.args_count is None) and all(args):
                        return {"args": args}
                    else:
                        return False

        return False


class AllowAnswer(ABCRule[BaseMessageMin]):
    def __init__(self, allow_reply: bool = False, allow_fwd: bool = False):
        self.use_reply = allow_reply
        self.use_fwd = allow_fwd

        self.bot = Bot(token=TOKEN)

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
    def __init__(self):
        self.bot = Bot(token=TOKEN)

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        try:
            await self.bot.api.messages.delete(
                group_id=GROUP_ID,
                peer_id=message.peer_id,
                cmids=message.conversation_message_id,
                delete_for_all=True
            )
            message.deleted = True

        except Exception as error:
            print("Rule aborted command completion:", error)
            message.deleted = False

        return True


class CheckPermission(ABCRule[BaseMessageMin]):

    def __init__(self, access_to: int = 0):
        self.access_to = access_to

        self.database = DataBase()

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id
        initiator_id = message.from_id

        if initiator_id == STAFF_ADMIN_ID:
            return True

        lvl = self.database.permissions.select(
            ("target_lvl",),
            peer_id=peer_id,
            target_id=initiator_id
        )
        lvl = lvl[0][0] if lvl else 0
        if lvl >= self.access_to:
            return True

        return False


class IgnorePermission(ABCRule[BaseMessageMin]):
    def __init__(self, ignore_from: int = 0, mode: str = "TARGET"):
        self.ignore_from = ignore_from
        self.mode = mode

        self.bot = Bot(token=TOKEN)
        self.database = DataBase()

    def __check_permission(self, peer_id, target_id):
        if target_id == STAFF_ADMIN_ID:
            return False

        lvl = self.database.permissions.select(
            ("target_lvl",),
            peer_id=peer_id,
            target_id=target_id
        )
        lvl = lvl[0][0] if lvl else 0
        if lvl < self.ignore_from:
            return True

    def __check_forward(self, message: BaseMessageMin):
        checked = []
        for msg in message.fwd_messages:
            peer_id = message.peer_id
            target_id = msg.from_id
            checked.append(self.__check_permission(peer_id, target_id))

        return all(checked)

    async def __check_mention(self, message: BaseMessageMin):
        peer_id = message.peer_id
        text = message.text
        screen_name = text[text.find("[") + 1:text.find("|")].replace("id", "")
        target_info = await self.bot.api.users.get(screen_name)
        if target_info:
            target_id = target_info[0].id
            return self.__check_permission(peer_id, target_id)

        return False

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        if self.mode == "TARGET":
            if message.reply_message:
                return self.__check_permission(peer_id, message.reply_message.from_id)

            elif message.fwd_messages:
                return self.__check_forward(message)

            else:
                return await self.__check_mention(message)

        elif self.mode == "SELF":
            return self.__check_permission(peer_id, message.from_id)

        return False


class HandleIn(ABCRule[BaseMessageMin]):

    def __init__(self, handle_log: bool = False, handle_chat: bool = False, send_respond=True):
        self.handle_log = handle_log
        self.handle_chat = handle_chat
        self.send_respond = send_respond

        self.database = DataBase()

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        peer_type = "LOG"
        if self.database.conversations.select(
            ("peer_name",),
            peer_id=peer_id,
            peer_type=peer_type
        ):
            if self.handle_log:
                return True

            else:
                if self.send_respond:
                    title = f"Отказ в исполнении команды. Команда не может быть использована в лог-чате."
                    await message.answer(title)
                return False

        peer_type = "CHAT"
        if self.database.conversations.select(
            ("peer_name",),
            peer_id=peer_id,
            peer_type=peer_type
        ):
            if self.handle_chat:
                return True

            else:
                if self.send_respond:
                    title = f"Отказ в исполнении команды. Команда не может быть использована в беседе."
                    await message.answer(title)
                return False

        return True


class OnlyEnrolled(ABCRule[BaseMessageMin]):
    def __init__(self, send_respond=True):
        self.send_respond = send_respond

        self.database = DataBase()

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        peer_id = message.peer_id

        if self.database.conversations.select(
            ("peer_name",),
            peer_id=peer_id,
            peer_type="LOG"
        ):
            return True

        if self.database.conversations.select(
            ("peer_name",),
            peer_id=peer_id,
            peer_type="CHAT"
        ):
            return True

        if self.send_respond:
            title = f"Отказ в исполнении команды. Беседа не зарегистрирована."
            await message.answer(title)
        return False
