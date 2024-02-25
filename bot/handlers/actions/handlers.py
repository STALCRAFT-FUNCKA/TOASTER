from tools.event import ButtonEvent
from tools.keyboard import Keyboard
import config
from .base import BaseAction



# ------------------------------------------------------------------------
class NotMessageOwnerAction(BaseAction):
    """Action that denies force
    unless it belongs to the author
    of the message with keyboard.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        snackbar_message = "⚠️ Отказано в доступе."

        self.snackbar(event, snackbar_message)

        return False



# ------------------------------------------------------------------------
class CancelAction(BaseAction):
    """Cancels the command, closes the menu,
    and deletes the message.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        self.api.messages.delete(
            peer_id=event.peer_id,
            cmids=event.cmid,
            delete_for_all=1
        )

        snackbar_message = "❗Отмена команды."

        self.snackbar(event, snackbar_message)

        return True



# ------------------------------------------------------------------------
class TestAction(BaseAction):
    """Test action.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        new_msg_text = "Тест был пройден!"

        keyboard = (
            Keyboard(inline=True, one_time=False)
        )

        self.api.messages.edit(
            peer_id=event.peer_id,
            conversation_message_id=event.cmid,
            message=new_msg_text,
            keyboard=keyboard.json
        )

        snackbar_message = "⚠️ Тест пройден!"

        self.snackbar(event, snackbar_message)

        return True



# ------------------------------------------------------------------------
class MarkAsChatAction(BaseAction):
    """Creates a "chat" mark and stores
    data about it in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        fields = ("conv_mark",)
        mark = self.db.conversations.select(
            fields=fields,
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
        fields = ("conv_mark",)
        mark = self.db.conversations.select(
            fields=fields,
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
        fields = ("conv_mark",)
        mark = self.db.conversations.select(
            fields=fields,
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
        fields = ("conv_mark",)
        mark = self.db.conversations.select(
            fields=fields,
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



# ------------------------------------------------------------------------
class SetAdministratorPermissionAction(BaseAction):
    """Sets the user to the "administrator" role,
    records this in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        fields = ("user_permission",)
        target_id=event.payload.get("target")
        lvl = self.db.permissions.select(
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[2]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if already_promoted:
            lvl = int(lvl[0][0])

            if lvl == 2:
                role = config.PERMISSIONS_DECODING[lvl]
                snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

                self.snackbar(event, snackbar_message)

                return False

        user_name = self.get_name(target_id)

        self.db.permissions.insert(
            on_duplicate="update",
            conv_id=event.peer_id,
            user_id=target_id,
            user_name=user_name,
            user_permission=2
        )

        self.snackbar(event, snackbar_message)

        return True


    def get_name(self, user_id: int) -> str:
        """Returns the full name of the user,
        using its unique ID.

        Args:
            user_id (int): User ID.

        Returns:
            str: User full name.
        """
        name = self.api.users.get(
            user_ids=user_id
        )

        if not bool(name):
            name = "Unknown"

        else:
            name = name[0].get("first_name") + \
                " " + name[0].get("last_name")

        return name



class SetModeratorPermissionAction(BaseAction):
    """Sets the user to the "moderator" role,
    records this in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        fields = ("user_permission",)
        target_id=event.payload.get("target")
        lvl = self.db.permissions.select(
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[1]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if already_promoted:
            lvl = int(lvl[0][0])

            if lvl == 1:
                role = config.PERMISSIONS_DECODING[lvl]
                snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

                self.snackbar(event, snackbar_message)

                return False

        user_name = self.get_name(target_id)

        self.db.permissions.insert(
            on_duplicate="update",
            conv_id=event.peer_id,
            user_id=target_id,
            user_name=user_name,
            user_permission=1
        )

        self.snackbar(event, snackbar_message)

        return True


    def get_name(self, user_id: int) -> str:
        """Returns the full name of the user,
        using its unique ID.

        Args:
            user_id (int): User ID.

        Returns:
            str: User full name.
        """
        name = self.api.users.get(
            user_ids=user_id
        )

        if not bool(name):
            name = "Unknown"

        else:
            name = name[0].get("first_name") + \
                " " + name[0].get("last_name")

        return name



class SetUserPermissionAction(BaseAction):
    """Sets the user to the "user" role,
    records this in the database.
    """
    def _handle(self, event: ButtonEvent, kwargs) -> bool:
        fields = ("user_permission",)
        target_id = event.payload.get("target")
        lvl = self.db.permissions.select(
            fields=fields,
            user_id=target_id
        )
        already_promoted = bool(lvl)

        role = config.PERMISSIONS_DECODING[0]
        snackbar_message = f"⚒️ Пользователю назначена роль \"{role}\"."

        if not already_promoted:
            role = config.PERMISSIONS_DECODING[lvl]
            snackbar_message = f"❗Пользователь уже имеет роль \"{role}\"."

            self.snackbar(event, snackbar_message)

            return False

        self.db.permissions.delete(
            user_id=target_id
        )

        self.snackbar(event, snackbar_message)

        return True



actionlist = {
    # not msg owner -----------------------------
    "not_msg_owner": NotMessageOwnerAction,
    # test --------------------------------------
    "test": TestAction,
    # cancel command ----------------------------
    "cancel_command": CancelAction,
    # mark --------------------------------------
    "mark_as_chat": MarkAsChatAction,
    "mark_as_log": MarkAsLogAction,
    "update_conv_data": UpdateConvDataAction,
    "drop_mark": DropMarkAction,
    # permission --------------------------------
    "set_administrator_permission": SetAdministratorPermissionAction,
    "set_moderator_permission": SetModeratorPermissionAction,
    "set_user_permission": SetUserPermissionAction
}
