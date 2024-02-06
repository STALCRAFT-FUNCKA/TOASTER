class CallbackButton(object):
    """VK button callback description class.
    """
    _body = {
        "color": None,
        "action": {
            "type": "callback",
            "label": None,
            "payload": {}
        }
    }

    def __init__(
        self,
        payload: dict,
        color: str = "primary",
        label: str = "Button",
    ):
        self._body["color"] = color
        self._body["action"]["label"] = label

        if payload:
            self._body["action"]["label"] = payload


    @property
    def body(self):
        """Returns the callback body 
        of the button as a dictionary.

        Returns:
            dict: Button body.
        """
        return self._body
