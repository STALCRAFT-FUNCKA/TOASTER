from config import TIME_COEFFICENT, GROUP_URL, STUFF_ADMIN_ID
from additionals.ABCHandler import ABCHandler


class Handler(ABCHandler):
    async def __send_respond(self, data):
        title = f"@id{data.get('target_id')} (Пользователь) был заглушен.\n" \
                f"Причина: {data.get('reason')}\n" \
                f"Время снятия заглушения: {data.get('target_time')}\n" \
                f"По вопросам обращаться к @id{STUFF_ADMIN_ID} (Администратору)."
        await self.bot.api.messages.send(chat_id=data.get('chat_id'), message=title, random_id=0)

    async def check(self):
        overflow = self.database.get_overflow_warn()
        if overflow:
            for warn in overflow:
                self.database.remove_warn(peer_id=warn[0], user_id=warn[1], force=True)
                delta = TIME_COEFFICENT["d"]
                all_data = await self.about.get_all_info(
                    cpid=warn[0],
                    ctid=warn[1],
                    time_delta=delta,
                    rsn="Получено три предупреждения"
                )
                all_data["initiator_id"] = 0
                all_data["initiator_name"] = "Система"
                all_data["initiator_url"] = GROUP_URL
                all_data["chat_id"] = warn[0] - 2000000000

                self.database.add_mute(all_data)

                await self.__send_respond(all_data)
                await self._send_log(peer_id=warn[0], user_id=warn[1], command="mute")