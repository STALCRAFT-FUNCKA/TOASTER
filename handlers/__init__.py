from . import (
    ban_handler,
    mute_handler,
    warn_handler
)

handlers = [ban_handler.Handler(), mute_handler.Handler(), warn_handler.Handler()]