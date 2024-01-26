import os
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll


class Bot(object):
    __session = None
    __longpoll = None

    api = None

    def __create_session(self):
        self.__session = VkApi(
            token=os.getenv("TOASTER_DEV_TOKEN"),
            api_version="5.199"
        )

    def __create_longpoll(self):
        self.__longpoll = VkLongPoll(
            vk=self.__session,
            wait=10,
            group_id=os.getenv("TOASTER_DEV_GROUPID")
        )

    def __create_api(self):
        self.api = self.__session.get_api()

    def __init__(self):
        self.__create_session()
        self.__create_longpoll()
        self.__create_api()

    def run(self):
        for event in self.__longpoll.listen():
            print(event)
