from vkbottle.bot import Message
from bot.usr_config import ALLOWED_URL, ALLOWED_DOMAIN, CRITICAL_URL, CRITICAL_DOMAIN
from bot.routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from urlextract import URLExtract


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def url_filter(message: Message):
    extractor = URLExtract()
    urls = extractor.find_urls(message.text)
    urls = [url.split("//")[-1] for url in urls]
    domains = [url.split("/")[0] for url in urls]
    content = ((domains[i], urls[i]) for i in range(len(urls)))

    if urls:
        reason = None
        hard_mode = database.settings.select(
            ("setting_status",),
            peer_id=message.peer_id,
            setting_name='Hard_Mode'
        )
        hard_mode = hard_mode[0][0] if hard_mode else False
        hard_mode = True if hard_mode == "True" else False
        for domain, url in content:
            if hard_mode:
                if domain in ALLOWED_DOMAIN or url in ALLOWED_URL:
                    return

            if domain in CRITICAL_DOMAIN or url in CRITICAL_URL:
                reason = "Запрещенная ссылка"

        if reason is None and hard_mode:
            reason = "Нежелательная ссылка"
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

            await processor.warn_proc(context, collapse=True, log=True, respond=True)

        elif reason is not None:
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
                "command_name": "mute",
                "now_time": converter.now(),
                "target_time": converter.now() + converter.delta(time, coefficient),
                "cmids": [message.conversation_message_id]
            }

            await processor.unwarn_proc(context, log=False, respond=False)
            await processor.mute_proc(context, collapse=True, log=True, respond=True)
