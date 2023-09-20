from commands import *
from filters import *
from handlers import *

labelers = [

]

handlers = [
    MuteHandler(),
    BanHandler(),
    WarnHandler(),
    WarnOverflowHandler(),
    QueueHandler()
]
