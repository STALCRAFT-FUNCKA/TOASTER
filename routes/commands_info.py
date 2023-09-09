from config import ALIASES, PREFIXES, PERMISSION_ACCESS
from vkbottle.bot import BotLabeler, Message
from database.proc import InformationProcessor, ReferenceProcessor
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
        await ref_processor.ref_reference_proc(context)

    if args[0] in ALIASES['chat']:
        await ref_processor.ref_chat_proc(context)

    if args[0] in ALIASES['log']:
        await ref_processor.ref_log_proc(context)

    if args[0] in ALIASES['drop']:
        await ref_processor.ref_log_proc(context)

    if args[0] in ALIASES['permission']:
        await ref_processor.ref_permission_proc(context)

    if args[0] in ALIASES['setting']:
        await ref_processor.ref_setting_proc(context)

    if args[0] in ALIASES['delete']:
        await ref_processor.ref_delete_proc(context)

    if args[0] in ALIASES['copy']:
        await ref_processor.ref_copy_proc(context)

    if args[0] in ALIASES['terminate']:
        await ref_processor.ref_terminate_proc(context)

    if args[0] in ALIASES['kick']:
        await ref_processor.ref_kick_proc(context)

    if args[0] in ALIASES['ban']:
        await ref_processor.ref_ban_proc(context)

    if args[0] in ALIASES['unban']:
        await ref_processor.ref_unban_proc(context)

    if args[0] in ALIASES['mute']:
        await ref_processor.ref_mute_proc(context)

    if args[0] in ALIASES['unmute']:
        await ref_processor.ref_unmute_proc(context)

    if args[0] in ALIASES['warn']:
        await ref_processor.ref_warn_proc(context)

    if args[0] in ALIASES['unwarn']:
        await ref_processor.ref_unwarn_proc(context)

    if args[0] in ALIASES['queue']:
        await ref_processor.ref_queue_proc(context)

    if args[0] in ALIASES['unqueue']:
        await ref_processor.ref_unqueue_proc(context)

    if args[0] in ALIASES['info']:
        await ref_processor.ref_info_proc(context)


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

    if args[0] in ALIASES['permission']:
        await info_processor.info_permission_proc(context)

    if args[0] in ALIASES['setting']:
        await info_processor.info_setting_proc(context)

    if args[0] in ALIASES['chat']:
        await info_processor.info_chat_proc(context)

    if args[0] in ALIASES['kick']:
        await info_processor.info_kick_proc(context)

    if args[0] in ALIASES['ban']:
        await info_processor.info_ban_proc(context)

    if args[0] in ALIASES['mute']:
        await info_processor.info_mute_proc(context)

    if args[0] in ALIASES['warn']:
        await info_processor.info_warn_proc(context)
