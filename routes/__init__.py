from . import (
    commands,
    commands_mention,
    queue,
    forbidden,
    mutepunish,
    account_age
)


labelers = [queue.bl, forbidden.bl, account_age.bl, mutepunish.bl, commands.bl, commands_mention.bl]
