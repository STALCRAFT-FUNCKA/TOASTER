COMMAND_PREFIXES: tuple = (
    "!", 
    "/"
)

MAX_COMMAND_ARG_COUNT: int = 10

PERMISSIONS_DECODING = {
    0: "Пользователь",
    1: "Модератор",
    2: "Администратор"
}

COMMAND_PERMISSIONS = {
    "test": 2,
    "mark": 2,
    "permission": 2,
}
