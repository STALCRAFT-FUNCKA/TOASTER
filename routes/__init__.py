from . import (
    commands,
    commands_mention,
    message_queue,
    forbidden,
    mutepunish,
    account_age
)


labelers = [message_queue.bl, forbidden.bl, account_age.bl, mutepunish.bl, commands.bl, commands_mention.bl]
