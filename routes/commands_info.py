from config import ALIASES, PREFIXES, PERMISSION_LVL, PERMISSION_ACCESS, QUEUE_TIME
from vkbottle.bot import BotLabeler, Message
from database.proc import InformationProcessor
from typing import Tuple
from utils import *
from .rules import *


bl = BotLabeler()

info = Info()
converter = Converter()
info_processor = InformationProcessor()
ref_processor = ReferenceProcessor()


@bl.chat_message(
    HandleCommand(ALIASES['reference'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['reference']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def reference(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id,
    }

    if args[0] == "all":
        await ref_processor.ref_all_proc(context)

    if args[0] in ALIASES['reference']:
        await ref_processor.info_reference_proc(context)

    if args[0] in ALIASES['chat']:
        await ref_processor.info_reference_proc(context)

    if args[0] in ALIASES['log']:
        await ref_processor.info_reference_proc(context)

    if args[0] in ALIASES['drop']:
        await ref_processor.info_reference_proc(context)

    if args[0] in ALIASES['permission']:
        await ref_processor.info_reference_proc(context)

    if args[0] in ALIASES['settings']:
        await ref_processor.info_reference_proc(context)


@bl.chat_message(
    HandleCommand(ALIASES['info'], PREFIXES, 1),
    CollapseCommand(),
    AnswerCommand(use_reply=False, use_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['info']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def info(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id
    }

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
