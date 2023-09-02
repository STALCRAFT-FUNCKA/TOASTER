conversations = """CREATE TABLE IF NOT EXISTS conversations
               (
                   peer_id INTEGER PRIMARY KEY UNIQUE ON CONFLICT REPLACE,
                   peer_name TEXT,
                   peer_type TEXT
               );"""

permissions = """CREATE TABLE IF NOT EXISTS permissions
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    target_id INTEGER, 
                    target_name TEXT,
                    target_lvl INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT REPLACE
                );"""

settings = """CREATE TABLE IF NOT EXISTS settings
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    setting_name TEXT,
                    setting_status INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, setting_name) ON CONFLICT REPLACE
                );"""

kicked = """CREATE TABLE IF NOT EXISTS kicked
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    initiator_id INTEGER,
                    initiator_name TEXT,
                    target_id INTEGER,
                    target_name TEXT,
                    kick_time INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT IGNORE
                );"""

banned = """CREATE TABLE IF NOT EXISTS banned
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    initiator_id INTEGER,
                    initiator_name TEXT,
                    target_id INTEGER,
                    target_name TEXT,
                    ban_time INTEGER,
                    unban_time INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT IGNORE  
                );"""

muted = """CREATE TABLE IF NOT EXISTS muted
               (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    initiator_id INTEGER,
                    initiator_name TEXT,
                    target_id INTEGER,
                    target_name TEXT,
                    mute_time INTEGER,
                    unmute_time INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT IGNORE 
               );"""

warned = """CREATE TABLE IF NOT EXISTS warned
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    initiator_id INTEGER,
                    initiator_name TEXT,
                    target_id INTEGER,
                    target_name TEXT,
                    warn_count INTEGER,
                    warn_time INTEGER,
                    unwarn_time INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT REPLACE 
                );"""

queue = """CREATE TABLE IF NOT EXISTS queue
                (
                    peer_id INTEGER PRIMARY KEY REFERENCES conversations (peer_id) ON DELETE CASCADE,
                    target_id INTEGER,
                    target_name TEXT,
                    send_time INTEGER,
                    next_time INTEGER,
                    CONSTRAINT someone UNIQUE (peer_id, target_id) ON CONFLICT IGNORE
                );"""

tables = [conversations, settings, permissions, queue, kicked, banned, muted, warned]
