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
    mark_command,
    permission_command,
    setting_command,
    kick_command,
    ban_command,
    mute_command,
    warn_command,
    queue_command,
    copy_command,
    delete_command,
    roll_command,
    say_command,
    hate_soloma_command,
]

handlers = [
    MuteHandler(),
    BanHandler(),
    WarnHandler(),
    WarnOverflowHandler(),
    QueueHandler()
]
