from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle_types.objects import MessagesMessageAttachmentType as AttachmentType
from config import TOKEN, GROUP_ID
from database.interface import Connection
from logger.logger import Logger
from rules.custom_rules import IgnorePermission, HandleIn
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
    HandleIn(handle_log=False, handle_chat=True),
    blocking=False
)
async def forbidden(message: Message):
    async def collapse(m: Message):
        await bot.api.messages.delete(
            group_id=GROUP_ID,
            peer_id=message.peer_id,
            cmids=m.conversation_message_id,
            delete_for_all=True
        )

    if message.deleted is None:
        reason = None

        attachment_checks = [
            ('Allow_Picture', AttachmentType.PHOTO, 'Вложенная фотография'),
            ('Allow_Video', AttachmentType.VIDEO, 'Вложенное видео'),
            ('Allow_Music', AttachmentType.AUDIO, 'Вложенная музыка'),
            ('Allow_Voice', AttachmentType.AUDIO_MESSAGE, 'Голосовое сообщение'),
            ('Allow_Post', (AttachmentType.WALL_REPLY, AttachmentType.WALL), 'Репост'),
            ('Allow_Votes', AttachmentType.POLL, 'Вложенное голосование'),
            ('Allow_Files', AttachmentType.DOC, 'Вложенный файл'),
            ('Allow_Miniapp', AttachmentType.MINI_APP, 'Вложенное мини-приложение'),
            ('Allow_Graffiti', AttachmentType.GRAFFITI, 'Граффити'),
            ('Allow_Sticker', AttachmentType.STICKER, 'Стикер')
        ]

        if reason is None:
            for setting, attachment_type, r in attachment_checks:
                if not database.get_setting(message.peer_id, setting):
                    if message.attachments:
                        for attachment in message.attachments:
                            if attachment.type == attachment_type:
                                reason = r

        if reason is None and (message.reply_message or message.fwd_messages):
            if message.reply_message:
                if message.from_id != message.reply_message.from_id:
                    reason = 'Переслано чужое сообщение'
            elif message.fwd_messages:
                for msg in message.fwd_messages:
                    if message.from_id != msg.from_id:
                        reason = 'Переслано чужое сообщение'

        if reason is not None:
            print(reason)
            # Код

            await collapse(message)
