from . import (
    commands,
    commands_mention,
    queue,
    forbidden,
    mutepunish
)


labelers = [queue.bl, forbidden.bl, mutepunish.bl, commands.bl, commands_mention.bl]
