from tools.handler import ABCHandlingHub
from tools.event import ButtonEvent
from db import DataBase
from .handlers import actionlist


class ActionHandler(ABCHandlingHub):
    """Event handler class that recognizes payload
    in the message and executing attached to each button
    actions.
    """
    db = DataBase()

    def _check(self, event: ButtonEvent) -> bool:
        return bool(event.payload)


    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        call_action = event.payload.get("call_action")

        if call_action is None:
            super().logger.info(
                "Wrong payload <%s>",
                event.payload
            )
            return False

        selected = actionlist.get(call_action)

        if selected is None:
            super().logger.info(
                "Could not recognize called action <%s>",
                call_action
            )
            return False

        selected = selected(self.db, super().api)
        return selected(event)
