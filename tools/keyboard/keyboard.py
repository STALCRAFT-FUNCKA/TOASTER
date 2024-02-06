"""Description of the VK keyboard class file.
"""
import json
from .button import Button
from .action import BaseAction
from .color import ButtonColor


class Keyboard(object):
    """VK keyboard builder class.
    """

    def __init__(self, inline: bool, one_time: bool):
        self.inline: bool = inline
        self.one_time: bool = one_time
        self.buttons: list = []


    def add_row(self):
        """Adds a new line for placing buttons.
        The count of lines cannot exceed 6.

        Raises:
            ValueError: The maximum count of rows has been exceeded.
            RuntimeError: Cannot create a new row while the previous row is empty.

        Returns:
            object: self
        """
        if len(self.buttons) > 6:
            raise ValueError("The maximum count of rows has been exceeded.")

        if self.buttons and not self.buttons[-1]:
            raise RuntimeError("Cannot create a new row while the previous row is empty.")

        self.buttons.append([])

        return self


    def add_button(self, action: BaseAction, color: ButtonColor):
        """_summary_

        Args:
            action (BaseAction): VK keyboard button action.
            color (ButtonColor): VK keyboard button color.

        Raises:
            RuntimeError: Missing rows.

        Returns:
            object: self.
        """
        if not self.buttons:
            raise RuntimeError("Missing rows.")

        new_button = Button(action, color).data
        self.buttons[-1].append(new_button)

        return self


    @property
    def json(self):
        """Converts keyboard object fields to
        JSON string.
        
        Returns:
            str: JSON dumped string.
        """
        body = {
            "one_time": self.one_time,
            "inline": self.inline,
            "buttons": self.buttons
        }

        return json.dumps(body)
