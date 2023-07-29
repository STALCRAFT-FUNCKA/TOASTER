from typing import List, Optional, Union
from vkbottle import ABCRule, Bot
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from Config import GROUP, TOKEN

bot = Bot(token=TOKEN)

DEFAULT_PREFIXES = ["!", "/"]
DEFAULT_ALIASES = ["Command", "command"]


class HandleCommand(ABCRule[BaseMessageMin]):

    def __init__(
            self,
            command_aliases: Optional[List[str]] = None,
            prefixes: Optional[List[str]] = None,
            args_count: int = 0
    ):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_aliases = command_aliases or DEFAULT_ALIASES
        self.args_count = args_count
        self.sep = " "

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        text = message.text

        # Тут игнорируются аргументы, если команда имеет 0 аргументов в настройке
        if not self.args_count and self.sep in text:
            cut = message.text.find(self.sep)
            text = text[0:cut]

        for prefix in self.prefixes:
            for command_text in self.command_aliases:
                command_length = len(prefix + command_text)
                command_length_with_sep = command_length + len(self.sep)
                if text.startswith(prefix + command_text):
                    # Если команда имеет 0 аргументов в настройке
                    if not self.args_count and len(text) == command_length:
                        try:
                            await bot.api.messages.delete(
                                group_id=GROUP,
                                peer_id=message.peer_id,
                                cmids=message.conversation_message_id,
                                delete_for_all=True
                            )
                            message.deleted = True
                        except Exception:
                            pass

                        return True

                    elif self.args_count:
                        args = message.text[command_length_with_sep:].split(self.sep)
                        if len(args) == self.args_count and all(args):
                            try:
                                await bot.api.messages.delete(
                                    group_id=GROUP,
                                    peer_id=message.peer_id,
                                    cmids=message.conversation_message_id,
                                    delete_for_all=True
                                )
                                message.deleted = True
                            except Exception:
                                pass

                            return {"args": args}

                        else:
                            print('deleted')
                            try:
                                await bot.api.messages.delete(
                                    group_id=GROUP,
                                    peer_id=message.peer_id,
                                    cmids=message.conversation_message_id,
                                    delete_for_all=True
                                )
                                message.deleted = True
                            except Exception:
                                pass

                            return False

        return False
