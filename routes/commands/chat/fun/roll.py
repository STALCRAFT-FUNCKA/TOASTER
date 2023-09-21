import random
from routes.commands.core import *
from config import PERMISSION_ACCESS, ALIASES, PREFIXES
from vkbottle.bot import Message, BotLabeler
from typing import Tuple
from routes.rules import *


bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['roll'], PREFIXES),
    CollapseCommand(),
    CheckPermission(access_to=PERMISSION_ACCESS['roll']),
    HandleIn(handle_log=False, handle_chat=True),
    OnlyEnrolled()
)
async def ban(message: Message, args: Tuple):
    context = {
        "peer_id": message.peer_id,
        "peer_name": await informer.peer_name(message.peer_id),
        "chat_id": message.chat_id,
        "initiator_id": message.from_id,
        "initiator_name": await informer.user_name(message.from_id, tag=False),
        "initiator_nametag": await informer.user_name(message.from_id, tag=True),
        "command_name": "roll",
        "now_time": converter.now(),
        "down_border": None,
        "up_border": None,
        "result": None
    }
    try:
        down_border = int(args[0])
        up_border = int(args[1])
    except Exception as error:
        print("Command aborted: ", error)
        return

    random.seed()
    if len(args) == 0:
        context["down_border"] = 0
        context["up_border"] = 100
        result = random.randint(0, 100)
        context["result"] = result

    if len(args) == 1:
        context["down_border"] = down_border
        context["up_border"] = 100
        result = random.randint(down_border, 100)
        context["result"] = result

    if len(args) == 2:
        context["down_border"] = down_border
        context["up_border"] = up_border
        result = random.randint(down_border, up_border)
        context["result"] = result

    await fun_processor.fun_roll_proc(context, log=False, respond=False)
