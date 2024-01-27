import os
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll

class Bot(object):
    """
    Bot main class
    """
    _session = None
    _longpoll = None

    api = None

    def _create_session(self):
        self._session = VkApi(
            token=os.getenv("TOASTER_DEV_TOKEN"),
            api_version="5.199"
        )

    def _create_longpoll(self):
        self._longpoll = VkLongPoll(
            vk=self._session,
            wait=10,
            group_id=os.getenv("TOASTER_DEV_GROUPID")
        )

    def _create_api(self):
        self.api = self._session.get_api()

    def _fabricate_event(self, raw_event):
        # TODO: write me
        return raw_event

    def __init__(self):
        self._create_session()
        self._create_longpoll()
        self._create_api()

    def run(self):
        """
        Starts listening VK long polling server.
        """
        for raw_event in self._longpoll.listen():
            event = self._fabricate_event(raw_event)
            print(event)
