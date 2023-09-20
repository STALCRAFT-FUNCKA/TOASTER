from .commands import *
from .filters import *
from .handlers import *

labelers = [
    queue_filter,
    forbidden_filter,
    curse_filter,
    age_filter,
    mute_filter,
    url_filter,

    info_command,
    reference_command,
    ban_command,
    copy_command,
    delete_command,
    kick_command,
    mark_command,
    mute_command,
    permission_command,
    queue_command,
    setting_command,
    warn_command
]

handlers = [
    MuteHandler(),
    BanHandler(),
    WarnHandler(),
    WarnOverflowHandler(),
    QueueHandler()
]
