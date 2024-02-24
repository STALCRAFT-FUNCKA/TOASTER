"""File describing the types of answers of VK keyboard buttons.
"""
import json


class BaseAnswer(object):
    """VK keyboard button action base class.
    """
    def __init__(self, action_type: str):
        self.type = action_type

    @property
    def data(self) -> dict:
        """Returns a dictionary representation of the button
        action feilds.
        
        Returns:
            dict: Action dictionary.
        """
        data = {
            key: value for key, value in vars(self).items()
        }

        return json.dumps(data)



class SnackbarAnswer(BaseAnswer):
    """VK keyboard button action base class.
    """
    def __init__(self, text: str):
        super().__init__("show_snackbar")

        self.text = text



class LinkAnswer(BaseAnswer):
    """VK keyboard button action base class.
    """
    def __init__(self, url: str):
        super().__init__("open_link")

        self.link = url



class AppAnswer(BaseAnswer):
    """VK keyboard button action base class.
    """
    def __init__(self, app_hash: str, app_id: int, owner_id: int):
        super().__init__("open_app")

        self.hash = app_hash
        self.app_id = app_id
        self.owner_id = owner_id
