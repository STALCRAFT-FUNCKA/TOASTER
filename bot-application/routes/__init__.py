from commands import commands_labeler
from filters import filters_labeler
from handlers import *

labelers = [
    filters_labeler,
    commands_labeler
]

handlers = [
    MuteHandler(),
    BanHandler(),
    WarnHandler(),
    WarnOverflowHandler(),
    QueueHandler()
]
