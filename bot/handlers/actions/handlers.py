from tools.event import ButtonEvent
from .base import BaseAction
from .keyboards import EmptyKbd


class NotMessageOwnerAction(BaseAction):
    """Action that denies force
    unless it belongs to the author
    of the message with keyboard.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return True



class TestAction(BaseAction):
    """Test action.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        new_msg_text = "Тест был пройден!"

        self.api.messages.edit(
            peer_id=event.peer_id,
            conversation_message_id=event.cmid,
            message=new_msg_text,
            keyboard=EmptyKbd.json
        )

        snackbar_message = "⚠️ Тест пройден!"

        self.snackbar(event, snackbar_message)

        return True



class MarkAsChatAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        feilds = ("conv_name",)
        mark = self.db.conversations.select(
            feilds=feilds,
            conv_id=event.peer_id
        )
        already_marked = bool(mark)

        if not already_marked:
            self.db.conversations.insert(
                conv_id=event.peer_id,
                conv_name=event.peer_name,
                conv_mark="CHAT"
            )

            snackbar_message = "📝 Беседа помечена как \"чат\"."

        else:
            snackbar_message = f"❗Беседа уже имеет метку \"{mark[0][0]}\"."

        self.snackbar(event, snackbar_message)

        return True



class MarkAsLogAction(BaseAction):
    """Creates a "log" mark and stores
    data about it in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        feilds = ("conv_name",)
        mark = self.db.conversations.select(
            feilds=feilds,
            conv_id=event.peer_id
        )
        already_marked = bool(mark)

        if not already_marked:
            self.db.conversations.insert(
                conv_id=event.peer_id,
                conv_name=event.peer_name,
                conv_mark="LOG"
            )

            snackbar_message = "📝 Беседа помечена как \"лог\"."

        else:
            snackbar_message = f"❗Беседа уже имеет метку \"{mark[0][0]}\"."

        self.snackbar(event, snackbar_message)

        return True



class UpdateConvDataAction(BaseAction):
    """Updates the data of a conversation
    that already has a label. First of all,
    it is necessary for the correct display
    of logs when changing the name of the
    conversation.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        feilds = ("conv_name",)
        mark = self.db.conversations.select(
            feilds=feilds,
            conv_id=event.peer_id
        )
        already_marked = bool(mark)

        if already_marked:
            new_data = {
                "conv_name": event.peer_name,
            }
            self.db.conversations.update(
                new_data=new_data,
                conv_id=event.peer_id
            )

            snackbar_message = "📝 Данные беседы обновлены."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True



class DropMarkAction(BaseAction):
    """Removes the mark from the conversation,
    deleting records about it in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        feilds = ("conv_name",)
        mark = self.db.conversations.select(
            feilds=feilds,
            conv_id=event.peer_id
        )
        already_marked = bool(mark)

        if already_marked:
            self.db.conversations.delete(
                conv_id=event.peer_id
            )

            snackbar_message = f"📝 Метка \"{mark[0][0]}\" снята с беседы."

        else:
            snackbar_message = "❗Беседа еще не имеет метку."

        self.snackbar(event, snackbar_message)

        return True



class CancelMarkingAction(BaseAction):
    """Cancels the command, closes the menu,
    and deletes the message.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        self.api.messages.delete(
            peer_id=event.peer_id,
            cmids=event.cmid
        )

        snackbar_message = "❗Отмена команды."

        self.snackbar(event, snackbar_message)

        return True


actionlist = {
    # not msg owner
    "not_msg_owner": NotMessageOwnerAction,
    # test -----
    "test": TestAction,
    # mark -----
    "mark_as_chat": MarkAsChatAction,
    "mark_as_log": MarkAsLogAction,
    "update_conv_data": UpdateConvDataAction,
    "drop_mark": DropMarkAction,
    "cancel_marking": CancelMarkingAction
}
