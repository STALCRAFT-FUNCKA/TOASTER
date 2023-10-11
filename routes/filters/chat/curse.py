"""
File with bot curse filter bot.
"""

from vkbottle.bot import Message, BotLabeler
from routes.filters.core import (
    database,
    com_processor,
    converter,
    informer
)
from routes.rules import (
    IgnorePermission,
    HandleIn,
    OnlyEnrolled
)
from config import CURSE_WORDS

bl = BotLabeler()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def curse_filter(message: Message):
    """
    This function describes the logic behind the curse filter.
    
    Args:
        message (Message): vkbottle message object.
    """
    
    check = database.settings.select(
        ("setting_status",),
        peer_id=message.peer_id,
        setting_name="Filter_Curse"
    )
    check = check[0][0]
    if not check:
        return True

    for word in CURSE_WORDS:
        if word in message.text:
            reason = "Нежелательное слово"
            context = {
                "peer_id": message.peer_id,
                "peer_name": await informer.peer_name(message.peer_id),
                "chat_id": message.chat_id,
                "initiator_id": 0,
                "initiator_name": "Система",
                "initiator_nametag": "Система",
                "command_name": "delete",
                "reason": reason,
                "now_time": converter.now(),
                "cmids": [message.conversation_message_id],
            }

            await com_processor.delete_proc(context, log=True, respond=False)
