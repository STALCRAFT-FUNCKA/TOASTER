from config import ALIASES, PREFIXES, PERMISSION_LVL, PERMISSION_ACCESS, QUEUE_TIME
from vkbottle.bot import BotLabeler, Message
from database.proc import CommandProcessor
from typing import Tuple
from utils import *
from .rules import *


bl = BotLabeler()

info = Info()
converter = Converter()
processor = CommandProcessor()


@bl.chat_message(
    HandleCommand(ALIASES['info'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['info']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def info(message: Message, args: Tuple):
    if args[0] == "permission":
        pass
        # process with context

    if args[0] == "settings":
        pass
        # process with context

    if args[0] == "conversation":
        pass
        # process with context

    if args[0] == "kick":
        pass
        # process with context

    if args[0] == "ban":
        pass
        # process with context

    if args[0] == "mute":
        pass
        # process with context

    if args[0] == "warn":
        pass
        # process with context
