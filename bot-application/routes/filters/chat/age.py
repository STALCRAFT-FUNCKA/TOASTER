import datetime
import requests
from bs4 import BeautifulSoup
from vkbottle.bot import Message
from bot.routes.rules import IgnorePermission, HandleIn, OnlyEnrolled


@bl.chat_message(
    IgnorePermission(ignore_from=1, mode="SELF"),
    HandleIn(handle_log=False, handle_chat=True, send_respond=False),
    OnlyEnrolled(send_respond=False),
    blocking=False
)
async def age_filter(message: Message):
    is_muted = database.muted.select(
        ("target_name",),
        peer_id=message.peer_id,
        target_id=message.from_id
    )
    if is_muted:
        return

    check = database.settings.select(
        ("setting_status",),
        peer_id=message.peer_id,
        setting_name="Account_Age"
    )
    check = check[0][0] if check else False
    check = True if check == "True" else False
    if not check:
        return

    response = requests.get(f'https://vk.com/foaf.php?id={message.from_id}')
    user_xml = response.text

    soup = BeautifulSoup(user_xml, "xml")
    try:
        if 'banned' not in soup.Person.profileState:
            created_at = str(soup.Person.created)
            created_at = created_at[created_at.find('\"') + 1:]
            created_at = created_at[:created_at.find('\"')].replace('T', ' ')
            created_at = created_at[:created_at.find('+')]

            aca = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            n = datetime.datetime.now()

            delta = n - aca
            delta_seconds = int(delta.total_seconds())

            week = 60 * 60 * 24 * 7

            if delta_seconds < week*2:
                reason = 'Подозрительный аккаунт'
                context = {
                    "peer_id": message.peer_id,
                    "peer_name": await info.peer_name(message.peer_id),
                    "chat_id": message.chat_id,
                    "initiator_id": 0,
                    "initiator_name": "Система",
                    "initiator_nametag": "Система",
                    "target_id": message.from_id,
                    "target_name": await info.user_name(message.from_id, tag=False),
                    "target_nametag": await info.user_name(message.from_id, tag=True),
                    "command_name": "kick",
                    "reason": reason,
                    "now_time": converter.now(),
                    "cmids": [message.conversation_message_id]
                }

                await processor.kick_proc(context, collapse=True, log=True, respond=True)

    except Exception as error:
        print('!!!!!!!!!!!Some troubles in XML file!!!!!!!!!!!!: ', error)
