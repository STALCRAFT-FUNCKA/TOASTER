"""
This file contains all the necessary root information, utilities, classes
to ensure the operation of each command.
"""

from routes.processors import (
    CommandProcessor,
    InformationProcessor,
    ReferenceProcessor,
    FunProcessor
)
from utils import (
    Informer,
    Converter
)


informer = Informer()
converter = Converter()

com_processor = CommandProcessor()
info_processor = InformationProcessor()
ref_processor = ReferenceProcessor()
fun_processor = FunProcessor()


async def get_cuid(mention):
    """
    The function takes in an object mentioned on the VK platform,
    extracting the user screen name from it and converting it 
    into a user id.

    Args:
        mention (str): VK user mention object.

    Returns:
        int: user id.
    """
    screen_name = mention.replace("@", "")
    screen_name = screen_name[1:screen_name.find("|")].replace("id", "")
    uid = await informer.user_id(screen_name=screen_name)
    return uid
