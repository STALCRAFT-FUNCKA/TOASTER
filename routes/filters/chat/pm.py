"""
File with bot privte message filter bot.
"""

from vkbottle.bot import (
    Message,
    BotLabeler
)
from routes.rules import (
    IgnorePermission,
    HandleIn,
    OnlyEnrolled
)
from routes.filters.core import (
    database,
    informer,
    converter,
    com_processor
)


bl = BotLabeler()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def pm_filter(message: Message):
    """
    This function describes the logic behind the private message filter.
    
    Args:
        message (Message): vkbottle message object.
    """

    check = database.settings.select(
        ("setting_status",),
        peer_id=message.peer_id,
        setting_name="Need_PM"
    )
    check = check[0][0]
    if not check:
        return

    reason = "Закрытое ЛС"
    time = 1
    coefficient = "d"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": 0,
        "initiator_name": "Система",
        "initiator_nametag": "Система",
        "target_id": message.from_id,
        "target_name": await informer.user_name(message.from_id, tag=False),
        "target_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "warn",
        "reason": reason,
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficient),
        "cmids": [message.conversation_message_id]
    }

    pm_opened = await informer.user_pm(context.get("target_id"))
    if not pm_opened:
        await com_processor.warn_proc(context, collapse=True, log=True, respond=True)
