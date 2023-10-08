from routes.filters.core import *
from vkbottle.bot import Message, BotLabeler
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled


bl = BotLabeler()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def pm_filter(message: Message):
    check = database.settings.select(
        ("setting_status",),
        peer_id=message.peer_id,
        setting_name="Need_PM"
    )
    check = check[0][0]
    check = True if check == 1 else False
    if not check:
        return
    
    reason = "Закрытое ЛС"
    time = 1
    coefficient = "d"

    context = {
        "peer_id": message.peer_id,
        "peer_name": await info.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": 0,
        "initiator_name": "Система",
        "initiator_nametag": "Система",
        "target_id": message.from_id,
        "target_name": await info.user_name(message.from_id, tag=False),
        "target_nametag": await info.user_name(message.from_id, tag=True),
        "command_name": "warn",
        "reason": reason,
        "now_time": converter.now(),
        "target_time": converter.now() + converter.delta(time, coefficient),
        "cmids": [message.conversation_message_id]
    }
    
    pm_opened = await info.user_pm(context.get("target_id"))
    if not pm_opened:
        await processor.warn_proc(context, collapse=True, log=True, respond=True)