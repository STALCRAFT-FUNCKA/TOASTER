from . import (commands, commands_mention)
from .filters import *

# Сначала фильтры, потом блок команд
labelers = [
    queue_filter.bl,
    forbidden_filter.bl,
    curse_filter.bl,
    url_filter.bl,
    age_filter.bl,
    mute_filter.bl,

    commands.bl,
    commands_mention.bl
]
