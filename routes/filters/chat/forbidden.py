"""
File with bot forbidden filter bot.
"""

from vkbottle_types.objects import MessagesMessageAttachmentType as AttachmentType
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
async def forbidden_filter(message: Message):
    """
    This function describes the logic behind the forbidden filter.
    
    Args:
        message (Message): vkbottle message object.
    """
    
    is_muted = database.muted.select(
        ("target_name",),
        peer_id=message.peer_id,
        target_id=message.from_id
    )
    if is_muted:
        return

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
                check = database.settings.select(
                    ("setting_status",),
                    peer_id=message.peer_id,
                    setting_name=setting
                )
                check = check[0][0]
                if not check:
                    for attachment in message.attachments:
                        if attachment.type == attachment_type:
                            reason = r

    if reason is None and (message.reply_message or message.fwd_messages):
        check = database.settings.select(
            ("setting_status",),
            peer_id=message.peer_id,
            setting_name='Allow_Reply'
        )
        check = check[0][0]
        if not check:
            if message.reply_message:
                if message.from_id != message.reply_message.from_id:
                    reason = 'Переслано чужое сообщение'
            elif message.fwd_messages:
                for msg in message.fwd_messages:
                    if message.from_id != msg.from_id:
                        reason = 'Переслано чужое сообщение'

    if reason is not None:
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

        await com_processor.warn_proc(context, collapse=True, log=True, respond=True)
