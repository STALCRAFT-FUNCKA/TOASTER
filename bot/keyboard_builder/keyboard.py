"""Description of the VK keyboard class file.
"""
import json
from .button import CallbackButton


class Keyboard(object):
    """VK keyboard builder class.
    Currently does not support creating buttons with built-in
    VK functionality. Supports callback buttons exclusively
    with payload.
    """
    # Empty keyboard pattern
    _body = {
        "one_time": False,
        "inline": False,
        "buttons": []
    }

    _button_count = 0

    def __init__(self, inline: bool = False, one_time: bool = False):
        if inline:
            one_time = False

        self._body["one_time"] = one_time
        self._body["inline"] = inline


    def add_row(self, *buttons: CallbackButton):
        """Adds a new line for placing buttons.
        The count of lines cannot exceed 6.
        The count of buttons in a line cannot exceed 5.
        The maximum possible count of buttons on the keyboard is 10
        
        Args:
            *buttons (Button): List of buttons separated by commas.
        """
        if any([
            len(buttons) > 5,
            len(self._body["buttons"]) > 6,
            (len(buttons) + self._button_count) > 10
        ]):
            return

        self._body["buttons"].append(
            [button.body for button in buttons]
        )

        self._button_count += len(buttons)


    @property
    def json(self):
        """Converts a cell body dictionary to a JSON string.
        In other words, it returns the keyboard as JSON
        to be sent as an argument in message (VK).
        
        Returns:
            str: JSON dumped string.
        """
        return json.dumps(self._body)
