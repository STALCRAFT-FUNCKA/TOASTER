conversations = """
CREATE TABLE IF NOT EXISTS conversations
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER UNIQUE,
        peer_name VARCHAR(255),
        peer_type VARCHAR(255)
    );
"""

permissions = """
CREATE TABLE IF NOT EXISTS permissions
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        target_id INTEGER, 
        target_name VARCHAR(255),
        target_lvl INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT permission UNIQUE (peer_id, target_id)
    );
"""

settings = """
CREATE TABLE IF NOT EXISTS settings
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        setting_name VARCHAR(255),
        setting_status BOOLEAN,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT setting UNIQUE (peer_id, setting_name)
    );
"""

kicked = """
CREATE TABLE IF NOT EXISTS kicked
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        initiator_id INTEGER,
        initiator_name VARCHAR(255),
        target_id INTEGER,
        target_name VARCHAR(255),
        kick_time INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT kick UNIQUE (peer_id, target_id)
    );
"""

banned = """
CREATE TABLE IF NOT EXISTS banned
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        initiator_id INTEGER,
        initiator_name VARCHAR(255),
        target_id INTEGER,
        target_name VARCHAR(255),
        ban_time INTEGER,
        unban_time INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT ban UNIQUE (peer_id, target_id) 
    );
"""

muted = """
CREATE TABLE IF NOT EXISTS muted
   (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        initiator_id INTEGER,
        initiator_name VARCHAR(255),
        target_id INTEGER,
        target_name VARCHAR(255),
        mute_time INTEGER,
        unmute_time INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT mute UNIQUE (peer_id, target_id)
   );
"""

warned = """
CREATE TABLE IF NOT EXISTS warned
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        initiator_id INTEGER,
        initiator_name VARCHAR(255),
        target_id INTEGER,
        target_name VARCHAR(255),
        warn_count INTEGER,
        warn_time INTEGER,
        unwarn_time INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT warn UNIQUE (peer_id, target_id) 
    );
"""

queue = """
CREATE TABLE IF NOT EXISTS queue
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER,
        target_id INTEGER,
        target_name VARCHAR(255),
        send_time INTEGER,
        next_time INTEGER,

        FOREIGN KEY (peer_id) REFERENCES conversations(peer_id) ON DELETE CASCADE,
        CONSTRAINT message UNIQUE (peer_id, target_id)
    );
"""

tables = [conversations, permissions, settings, kicked, banned, muted, warned, queue]
