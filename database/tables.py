conversations = """CREATE TABLE IF NOT EXISTS conversations
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   peer_id INTEGER UNIQUE ON CONFLICT REPLACE,
                   peer_name TEXT,
                   destination TEXT
               );"""

# TODO: Сделать унифицированные названия столбцов
permissions = """CREATE TABLE IF NOT EXISTS permissions
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER, 
                    user_name TEXT,
                    user_url TEXT,
                    permission_lvl INTEGER,
                    permission_name TEXT,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT REPLACE
                );"""

settings = """CREATE TABLE IF NOT EXISTS settings
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    setting_name TEXT UNIQUE ON CONFLICT IGNORE,
                    setting_status INTEGER
                );"""

kicked = """CREATE TABLE IF NOT EXISTS kicked
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER,
                    user_name TEXT,
                    user_url TEXT,
                    kicked_by_id INTEGER,
                    kicked_by_name TEXT,
                    kicked_by_url TEXT,
                    kick_time INTEGER,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT IGNORE
                );"""

banned = """CREATE TABLE IF NOT EXISTS banned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER,
                    user_name TEXT,
                    user_url TEXT,
                    banned_by_id INTEGER,
                    banned_by_name TEXT,
                    banned_by_url TEXT,
                    ban_time INTEGER,
                    unban_time INTEGER,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT IGNORE  
                );"""

muted = """CREATE TABLE IF NOT EXISTS muted
               (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER,
                    user_name TEXT,
                    user_url TEXT,
                    muted_by_id INTEGER,
                    muted_by_name TEXT,
                    muted_by_url TEXT,
                    mute_time INTEGER,
                    unmute_time INTEGER ,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT IGNORE 
               );"""

warned = """CREATE TABLE IF NOT EXISTS warned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER,
                    user_name TEXT,
                    user_url TEXT,
                    warned_by_id INTEGER,
                    warned_by_name TEXT,
                    warned_by_url TEXT,
                    warn_time INTEGER,
                    unwarn_time INTEGER,
                    warn_count INTEGER,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT REPLACE 
                );"""

blacklist = """CREATE TABLE IF NOT EXISTS blacklist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    url TEXT
                );"""

whitelist = """CREATE TABLE IF NOT EXISTS whitelist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    domain TEXT
                );"""

queue = """CREATE TABLE IF NOT EXISTS queue
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    peer_id INTEGER REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    user_id INTEGER,
                    user_name TEXT,
                    user_url TEXT,
                    send_time INTEGER,
                    next_send_time INTEGER,
                    CONSTRAINT someone UNIQUE (user_id, peer_id) ON CONFLICT IGNORE
                );"""

tables = [conversations, settings, permissions, kicked, banned, warned, muted, blacklist, whitelist, queue]
