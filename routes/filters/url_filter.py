from vkbottle.bot import Bot, BotLabeler, Message
from config import TOKEN, GROUP_ID, STUFF_ADMIN_ID, GROUP_URL, ALLOWED_URL, ALLOWED_DOMAIN, CRITICAL_URL, \
    CRITICAL_DOMAIN
from database.sql_interface import Connection
from routes.rules import IgnorePermission, HandleIn, OnlyEnrolled
from utils import *
from urlextract import URLExtract

bot = Bot(token=TOKEN)
bl = BotLabeler()
database = Connection('database/database.db')
logger = Logger()
about = About()
converter = Converter()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def url_filter(message: Message):
    async def send_mute_log(data, command):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name"),
            peer_name=data.get("peer_name"),
            command_name=command,
            reason=data.get('reason'),
            target_name=data.get("target_name_tagged"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_warn_log(data, command):
        # формируем лог
        logger.compose_log_data(
            initiator_name=data.get("initiator_name"),
            peer_name=data.get("peer_name"),
            command_name=command,
            reason=data.get('reason'),
            target_name=data.get("target_name_tagged"),
            target_warns=data.get("target_warns"),
            now_time=data.get("now_time"),
            target_time=data.get("target_time")
        )
        logger.compose_log_attachments(
            peer_id=data.get("peer_id"),
            cmids=data.get("cmids")
        )

        # отправляем лог
        await logger.log()

    async def send_warn_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) получил предупреждение.\n" \
                f"Причина: {data.get('reason')}.\n" \
                f"Текущее количество предупреждений: {data.get('target_warns')}/3.\n" \
                f"Время снятия предупреждений: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def send_mute_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) был заглушен.\n" \
                f"Причина: {data.get('reason')}.\n" \
                f"Время снятия блокировки: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    extractor = URLExtract()
    urls = extractor.find_urls(message.text)
    urls = [url.split("//")[-1] for url in urls]
    domains = [url.split("/")[0] for url in urls]
    content = ((domains[i], urls[i]) for i in range(len(urls)))

    print(content)

    if urls:
        reason = None
        hard_mode = database.get_setting(message.peer_id, 'Hard_Mode')
        for domain, url in content:
            print(domain, url)
            if hard_mode:
                if domain in ALLOWED_DOMAIN or url in ALLOWED_URL:
                    return

            if domain in CRITICAL_DOMAIN or url in CRITICAL_URL:
                reason = "Запрещенная ссылка"

        if reason is None and hard_mode:
            reason = "Нежелательная ссылка"
            delta = converter.delta(0, "d")
            all_data = await about.get_all_info(
                cpid=message.peer_id,
                ctid=message.from_id,
                rsn=reason,
                time_delta=delta
            )
            all_data["initiator_id"] = 0
            all_data["initiator_name"] = "Система"
            all_data["initiator_url"] = GROUP_URL
            all_data["chat_id"] = message.peer_id - 2000000000
            all_data["target_warns"] += 1
            all_data["cmids"] = [message.conversation_message_id]

            database.add_warn(all_data)

            await send_warn_respond(all_data)
            await send_warn_log(all_data, command="warn")

            await collapse(message)

        elif reason is not None:
            delta = converter.delta(0, "d")
            all_data = await about.get_all_info(
                cpid=message.peer_id,
                ctid=message.from_id,
                rsn=reason,
                time_delta=delta
            )
            all_data["initiator_id"] = 0
            all_data["initiator_name"] = "Система"
            all_data["initiator_url"] = GROUP_URL
            all_data["chat_id"] = message.peer_id - 2000000000
            all_data["cmids"] = [message.conversation_message_id]

            database.add_mute(all_data)

            await send_mute_respond(all_data)
            await send_mute_log(all_data, command="mute")

            await collapse(message)


