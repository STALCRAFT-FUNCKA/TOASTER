from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.commands.core import (
    informer,
    converter,
    com_processor
)
from routes.rules import (
    HandleCommand,
    CollapseCommand,
    AllowAnswer,
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
    HandleCommand(ALIASES['copy'], PREFIXES, 0),
    CollapseCommand(),
    AllowAnswer(allow_reply=True, allow_fwd=False),
    CheckPermission(access_to=PERMISSION_ACCESS['copy']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def copy(message: Message):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "copy",
        "now_time": converter.now(),
        "cmids": [message.reply_message.conversation_message_id],
        "copied": message.reply_message.text
    }

    await com_processor.copy_proc(context, log=True, respond=False)
