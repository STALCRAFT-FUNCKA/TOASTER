"""
File with /hate_soloma bot command.
"""

from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    informer,
    converter,
    fun_processor
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    CheckPermission,
    HandleIn,
    OnlyEnrolled
)
from config import (
    PERMISSION_ACCESS,
    ALIASES,
    PREFIXES
)

bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['hate_soloma'], PREFIXES, 0),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['hate_soloma']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def hate_soloma(message: Message):
    """
    This function describes the logic behind the /hate_soloma command.
    
    Args:
        message (Message): vkbottle message object.
    """

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "hate_soloma",
        "now_time": converter.now(),
    }

    await fun_processor.fun_hate_soloma_proc(context, respond=False)
