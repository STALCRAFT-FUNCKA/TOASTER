from .chat.information.info import bl as info_command
from .chat.information.reference import bl as reference_command
from .chat.moderation.ban import bl as ban_command
from .chat.moderation.copy import bl as copy_command
from .chat.moderation.delete import bl as delete_command
from .chat.moderation.kick import bl as kick_command
from .chat.moderation.mark import bl as mark_command
from .chat.moderation.mute import bl as mute_command
from .chat.moderation.permission import bl as permission_command
from .chat.moderation.queue import bl as queue_command
from .chat.moderation.setting import bl as setting_command
from .chat.moderation.warn import bl as warn_command
from .chat.fun.roll import bl as roll_command

__all__ = (
    "info_command",
    "reference_command",
    "ban_command",
    "copy_command",
    "delete_command",
    "kick_command",
    "mark_command",
    "mute_command",
    "permission_command",
    "queue_command",
    "setting_command",
    "warn_command",
    "roll_command"
)
