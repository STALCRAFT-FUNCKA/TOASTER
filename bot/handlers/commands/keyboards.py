"""_summary_
"""
from tools.keyboard import (
    Keyboard,
    Callback,
    ButtonColor
)


# -------------------------------------------------------------------
EmptyKbd = (
    Keyboard(inline=True, one_time=False)
)



# -------------------------------------------------------------------
TestCommandKbd = (
    Keyboard(inline=True, one_time=False)
    .add_row()
    .add_button(
        Callback(
            label="Позитив",
            payload={
                "master_command": "test",
                "call_action": "test"
            }
        ),
        ButtonColor.POSITIVE
    )
    .add_button(
        Callback(
            label="Негатив",
            payload={
                "master_command": "test",
                "call_action": "test"
            }
        ),
        ButtonColor.NEGATIVE
    )
)



# -------------------------------------------------------------------
MarkCommandKbd =  (
    Keyboard(inline=True, one_time=False)
    .add_row()
    .add_button(
        Callback(
            label="CHAT",
            payload={
                "master_command": "mark",
                "call_action": "mark_as_chat"
            }
        ),
        ButtonColor.POSITIVE
    )
    .add_button(
        Callback(
            label="LOG",
            payload={
                "master_command": "mark",
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
                "master_command": "mark",
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
                "master_command": "mark",
                "call_action": "drop_mark"
            }
        ),
        ButtonColor.NEGATIVE
    )
    .add_button(
        Callback(
            label="Отмена команды",
            payload={
                "master_command": "mark",
                "call_action": "cancel_marking"
            }
        ),
        ButtonColor.NEGATIVE
    )
)
