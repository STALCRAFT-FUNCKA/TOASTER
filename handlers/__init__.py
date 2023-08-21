from . import (
    ban_handler,
    mute_handler,
    warn_handler,
    queue_handler,
    warnoverflow_handler
)

handlers = [
    ban_handler.Handler(),
    mute_handler.Handler(),
    warn_handler.Handler(),
    queue_handler.Handler(),
    warnoverflow_handler.Handler()
]