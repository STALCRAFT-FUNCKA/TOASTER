from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle_types.objects import MessagesMessageAttachmentType as AttachmentType
from config import TOKEN, GROUP_ID, STUFF_ADMIN_ID, GROUP_URL
from database.sql_interface import Connection
from utils.chat_logger import Logger
from routes.rules.custom_rules import IgnorePermission, HandleIn
from utils.information_getter import About
from utils.time_converter import Converter

bot = Bot(token=TOKEN)
bl = BotLabeler()
database = Connection('database/database.db')
logger = Logger()
about = About()
converter = Converter()


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    blocking=False
)
async def forbidden(message: Message):
    async def send_log(data, command):
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

    async def send_respond(data):
        title = f"@id{data.get('target_id')} (Пользователь) получил предупреждение.\n" \
                f"Причина: {data.get('reason')}.\n" \
                f"Текущее количество предупреждений: {data.get('target_warns')}/3.\n" \
                f"Время снятия предупреждений: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await message.answer(title)

    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    if database.get_mute(peer_id=message.peer_id, user_id=message.from_id):
        return

    if message.deleted is None:
        reason = None

        attachment_checks = [
            ('Allow_Picture', AttachmentType.PHOTO, 'Вложенная фотография'),
            ('Allow_Video', AttachmentType.VIDEO, 'Вложенное видео'),
            ('Allow_Music', AttachmentType.AUDIO, 'Вложенная музыка'),
            ('Allow_Links', AttachmentType.LINK, 'Ссылающее вложение'),
            ('Allow_Voice', AttachmentType.AUDIO_MESSAGE, 'Голосовое сообщение'),
            ('Allow_Post', (AttachmentType.WALL_REPLY, AttachmentType.WALL), 'Репост'),
            ('Allow_Votes', AttachmentType.POLL, 'Вложенное голосование'),
            ('Allow_Files', AttachmentType.DOC, 'Вложенный файл'),
            ('Allow_Miniapp', AttachmentType.MINI_APP, 'Вложенное мини-приложение'),
            ('Allow_Graffiti', AttachmentType.GRAFFITI, 'Граффити'),
            ('Allow_Sticker', AttachmentType.STICKER, 'Стикер')
        ]

        if reason is None:
            if message.attachments:
                for setting, attachment_type, r in attachment_checks:
                    if not database.get_setting(message.peer_id, setting):
                        for attachment in message.attachments:
                            if attachment.type == attachment_type:
                                reason = r

        if reason is None and (message.reply_message or message.fwd_messages):
            if not database.get_setting(message.peer_id, 'Allow_Reply'):
                if message.reply_message:
                    if message.from_id != message.reply_message.from_id:
                        reason = 'Переслано чужое сообщение'
                elif message.fwd_messages:
                    for msg in message.fwd_messages:
                        if message.from_id != msg.from_id:
                            reason = 'Переслано чужое сообщение'

        if reason is not None:
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

            await send_respond(all_data)
            await send_log(all_data, command="warn")

            await collapse(message)
