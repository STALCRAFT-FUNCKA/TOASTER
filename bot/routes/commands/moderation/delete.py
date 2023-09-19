from bot.routes.commands.core import *
from bot.src_config import PERMISSION_ACCESS
from bot.usr_config import ALIASES, PREFIXES
from vkbottle.bot import Message
from bot.routes.rules import *


@bl.chat_message(
    HandleCommand(ALIASES['delete'], PREFIXES, 0),
    CollapseCommand(),
    AllowAnswer(allow_reply=True, allow_fwd=True),
    CheckPermission(access_to=PERMISSION_ACCESS['delete']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def delete(message: Message):
    if message.reply_message is not None:
        cmids = [message.reply_message.conversation_message_id]
    else:
        cmids = [msg.conversation_message_id for msg in message.fwd_messages]

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "delete",
        "now_time": converter.now(),
        "cmids": cmids,
    }

    await com_processor.delete_proc(context, log=True, respond=False)