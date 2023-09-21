import random
from routes.commands.core import *
from config import PERMISSION_ACCESS, ALIASES, PREFIXES, EMOJI_NUMBERS
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
async def roll(message: Message, args: Tuple):
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

    random.seed()
    if len(args) == 0:
        down_border = 0
        up_border = 100
        context["down_border"] = down_border
        context["up_border"] = up_border
        result = random.randint(down_border, up_border)
        context["result"] = result

    else:
        try:
            if len(args) == 1:
                down_border = int(args[0])
                up_border = 100
                if down_border > up_border:
                    down_border, up_border = up_border, down_border
                context["down_border"] = down_border
                context["up_border"] = up_border
                result = random.randint(down_border, up_border)
                context["result"] = result

            if len(args) == 2:
                down_border = int(args[0])
                up_border = int(args[1])
                if down_border > up_border:
                    down_border, up_border = up_border, down_border
                context["down_border"] = down_border
                context["up_border"] = up_border
                result = random.randint(down_border, up_border)
                context["result"] = result

        except Exception as error:
            print("Command aborted: ", error)
            return

    emoji_result = ''
    for num in str(context["result"]):
        emoji_result += EMOJI_NUMBERS[int(num)]
    context["result"] = emoji_result

    await fun_processor.fun_roll_proc(context, log=False, respond=False)
