"""
File with /reference bot command.
"""

from typing import Tuple
from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    ref_processor
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    CheckPermission,
    HandleIn,
    AllowAnswer
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)

bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['reference'], PREFIXES),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['reference']),
    HandleIn(handle_log=True, handle_chat=False)
)
async def reference(message: Message, args: Tuple):
    """
    This function describes the logic behind the /refrence command.
    
    Args:
        message (Message): vkbottle message object.
        args (Tuple): tuple of command arguments.
    """

    context = {
        "peer_id": message.peer_id,
        "chat_id": message.chat_id,
    }

    args_check = [
        (ALIASES['reference'], ref_processor.ref_reference_proc),
        (ALIASES['mark'], ref_processor.ref_mark_proc),
        (ALIASES['setting'], ref_processor.ref_setting_proc),
        (ALIASES['delete'], ref_processor.ref_delete_proc),
        (ALIASES['copy'], ref_processor.ref_copy_proc),
        (ALIASES['terminate'], ref_processor.ref_terminate_proc),
        (ALIASES['kick'], ref_processor.ref_kick_proc),
        (ALIASES['ban'], ref_processor.ref_ban_proc),
        (ALIASES['unban'], ref_processor.ref_unban_proc),
        (ALIASES['mute'], ref_processor.ref_mute_proc),
        (ALIASES['unmute'], ref_processor.ref_unmute_proc),
        (ALIASES['warn'], ref_processor.ref_warn_proc),
        (ALIASES['unwarn'], ref_processor.ref_unwarn_proc),
        (ALIASES['queue'], ref_processor.ref_queue_proc),
        (ALIASES['unqueue'], ref_processor.ref_unqueue_proc),
        (ALIASES['info'], ref_processor.ref_info_proc),
        (ALIASES['roll'], ref_processor.ref_roll_proc),
        (ALIASES['say'], ref_processor.ref_say_proc)
    ]
    if not args:
        await ref_processor.ref_all_proc(context)

    if len(args) == 1:
        for name, proc in args_check:
            if args[0] in name:
                await proc(context)
