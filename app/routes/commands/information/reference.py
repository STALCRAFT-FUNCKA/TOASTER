from ..core import *
from app.src_config import PERMISSION_ACCESS
from app.usr_config import ALIASES, PREFIXES
from vkbottle.bot import Message
from typing import Tuple
from app.routes.rules import *


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
        (ALIASES['information'], ref_processor.ref_info_proc(context))
    ]

    for name, proc in args_check:
        if args[0] in name:
            await proc
