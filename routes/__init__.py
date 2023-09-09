from . import (commands, commands_mention, commands_info)
from .filters import *

# !Сначала фильтры!, потом блок команд
labelers = [
    queue_filter.bl,            # Фильтры, зависящие от мута
    forbidden_filter.bl,
    curse_filter.bl,
    age_filter.bl,

    mute_filter.bl,             # Фильтры мута

    url_filter.bl,              # Фильтры, не зависящие от мута

    commands.bl,                # Блок команд
    commands_mention.bl,
    commands_info.bl,
]
