from src_config import PERMISSION_ACCESS
from usr_config import ALIASES, PREFIXES
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
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['reference']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def reference(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id,
    }

    args_check = [
        (("all",), ref_processor.ref_all_proc(context)),
        (ALIASES['reference'], ref_processor.ref_reference_proc(context)),
        (ALIASES['mark'], ref_processor.ref_mark_proc(context)),
        (ALIASES['setting'], ref_processor.ref_setting_proc(context)),
        (ALIASES['delete'], ref_processor.ref_delete_proc(context)),
        (ALIASES['copy'], ref_processor.ref_copy_proc(context)),
        (ALIASES['terminate'], ref_processor.ref_terminate_proc(context)),
        (ALIASES['kick'], ref_processor.ref_kick_proc(context)),
        (ALIASES['ban'], ref_processor.ref_ban_proc(context)),
        (ALIASES['unban'], ref_processor.ref_unban_proc(context)),
        (ALIASES['mute'], ref_processor.ref_mute_proc(context)),
        (ALIASES['unmute'], ref_processor.ref_unmute_proc(context)),
        (ALIASES['warn'], ref_processor.ref_warn_proc(context)),
        (ALIASES['unwarn'], ref_processor.ref_unwarn_proc(context)),
        (ALIASES['queue'], ref_processor.ref_queue_proc(context)),
        (ALIASES['unqueue'], ref_processor.ref_unqueue_proc(context)),
        (ALIASES['info'], ref_processor.ref_info_proc(context))
    ]

    for name, proc in args_check:
        if args[0] in name:
            await proc


@bl.chat_message(
    HandleCommand(ALIASES['info'], PREFIXES, 1),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['info']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def info(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id
    }

    args_check = [
        (ALIASES['permission'], info_processor.info_permission_proc),
        (ALIASES['setting'], info_processor.info_setting_proc),
        (ALIASES['mark'], info_processor.info_mark_proc),
        (ALIASES['kick'], info_processor.info_kick_proc),
        (ALIASES['ban'], info_processor.info_ban_proc),
        (ALIASES['mute'], info_processor.info_mute_proc),
        (ALIASES['warn'], info_processor.info_warn_proc),
    ]

    for name, proc in args_check:
        if args[0] in name:
            await proc(context)
