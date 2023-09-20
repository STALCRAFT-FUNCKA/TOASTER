from .chat.information.info import bl as info_labeler
from .chat.information.reference import bl as reference_labeler
from .chat.moderation.ban import bl as ban_labeler
from .chat.moderation.copy import bl as copy_labeler
from .chat.moderation.delete import bl as delete_labeler
from .chat.moderation.kick import bl as kick_labeler
from .chat.moderation.mark import bl as mark_labeler
from .chat.moderation.mute import bl as mute_labeler
from .chat.moderation.permission import bl as permission_labeler
from .chat.moderation.queue import bl as queue_labeler
from .chat.moderation.setting import bl as setting_labeler
from .chat.moderation.warn import bl as warn_labeler

__all__ = (
    "info_labeler",
    "reference_labeler",
    "ban_labeler",
    "copy_labeler",
    "delete_labeler",
    "kick_labeler",
    "mark_labeler",
    "mute_labeler",
    "permission_labeler",
    "queue_labeler",
    "setting_labeler",
    "warn_labeler"
)
