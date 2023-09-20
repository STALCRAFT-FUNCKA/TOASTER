from app.routes.commands.core import *
from app.src_config import PERMISSION_ACCESS
from app.usr_config import ALIASES, PREFIXES
from vkbottle.bot import Message
from typing import Tuple
from app.routes.rules import *


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
