from toaster_app.routes.commands.core import *
from toaster_app.config import PERMISSION_ACCESS, ALIASES, PREFIXES
from vkbottle.bot import Message, BotLabeler
from typing import Tuple
from toaster_app.routes.rules import *


bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['setting'], PREFIXES, 2),
    CollapseCommand(),
    AllowAnswer(allow_reply=False, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['setting']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def setting(message: Message, args: Tuple):
    setting_name = args[0]
    setting_status = args[1]

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "setting",
        "setting_name": setting_name,
        "setting_status": setting_status,
        "now_time": converter.now()
    }

    await com_processor.setting_proc(context, log=True, respond=False)