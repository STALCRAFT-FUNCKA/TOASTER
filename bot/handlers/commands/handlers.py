import re
from tools.event import MessageEvent
from tools.keyboard import (
    Keyboard,
    Callback,
    ButtonColor
)
import config
from .base import BaseCommand


class TestCommand(BaseCommand):
    """Test command.
    Sends test content to the chat where the command was called:
        Message
        Attachments
        Keyboard
        e.t.c
    """
    COMMAND_NAME = "test"
    __permission_lvl = config.COMMAND_PERMISSIONS[COMMAND_NAME]

    def _handle(self, event: MessageEvent, kwargs) -> bool:
        answer_text = f"Вызвана комманда <{self.COMMAND_NAME}> " \
                      f"с аргументами {kwargs.get('argument_list')}."

        keyboard = (
            Keyboard(inline=True, one_time=False)
            .add_row()
            .add_button(
                Callback(
                    label="Позитив",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "test"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Негатив",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "test"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class MarkCommand(BaseCommand):
    """Mark command.
    Initializes conversation marking process.
    Allows:
        - To mark conversation as "CHAT" or "LOG".
        - Update the data about conversation.
        - Delete conversation mark.
    """
    COMMAND_NAME = "mark"
    __permission_lvl = config.COMMAND_PERMISSIONS[COMMAND_NAME]

    def _handle(self, event: MessageEvent, kwargs) -> bool:
        answer_text = "⚠️ Вы хотите пометить новую беседу? \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        keyboard = (
            Keyboard(inline=True, one_time=False)
            .add_row()
            .add_button(
                Callback(
                    label="CHAT",
                    payload={
                        "keyboard_owner_id": event.peer_id,
                        "call_action": "mark_as_chat"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="LOG",
                    payload={
                        "keyboard_owner_id": event.peer_id,
                        "call_action": "mark_as_log"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_row()
            .add_button(
                Callback(
                    label="Обновить данные беседы",
                    payload={
                        "keyboard_owner_id": event.peer_id,
                        "call_action": "update_conv_data"
                    }
                ),
                ButtonColor.SECONDARY
            )
            .add_row()
            .add_button(
                Callback(
                    label="Сбросить метку",
                    payload={
                        "keyboard_owner_id": event.peer_id,
                        "call_action": "drop_mark"
                    }
                ),
                ButtonColor.NEGATIVE
            )
            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "keyboard_owner_id": event.peer_id,
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True



class PermissionCommand(BaseCommand):
    """_summary_
    """
    COMMAND_NAME = "permission"
    __permission_lvl = config.COMMAND_PERMISSIONS[COMMAND_NAME]

    def _handle(self, event: MessageEvent, kwargs) -> bool:
        user_tag = kwargs.get('argument_list')[0]

        if not self.is_tag(user_tag):
            return False

        answer_text = f"⚠️ Уровни доступа пользователя {user_tag} \n\n" \
        "Выберите необходимое дествие из меню ниже:"

        keyboard = (
            Keyboard(inline=True, one_time=False)
            .add_row()
            .add_button(
                Callback(
                    label="Модератор",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "set_moderator_permission"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Администратор",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "set_administrator_permission"
                    }
                ),
                ButtonColor.POSITIVE
            )
            .add_button(
                Callback(
                    label="Пользователь",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "set_user_permission"
                    }
                ),
                ButtonColor.NEGATIVE
            )
            .add_row()

            .add_button(
                Callback(
                    label="Отмена команды",
                    payload={
                        "keyboard_owner_id": event.from_id,
                        "call_action": "cancel_command"
                    }
                ),
                ButtonColor.NEGATIVE
            )
        )

        self.api.messages.send(
            peer_id=event.peer_id,
            random_id=0,
            message=answer_text,
            keyboard=keyboard.json
        )

        return True


    def is_tag(self, tag: str) -> bool:
        """Takes a string as input, determines
        is the line a VK user tag.

        Args:
            tag (str): The string that
            is assumed to be the user tag.

        Returns:
            bool: Is tag?
        """
        pattern = r"^\[id[-+]?\d+\|\@\w+\]"
        return bool(re.search(pattern, tag))



commandlist = {
    "test": TestCommand,
    "mark": MarkCommand,
    "permission": PermissionCommand
}
