"""
This file describes the main queries that form the structure of the database.
"""

# Table
CONVERSATIONS = """
CREATE TABLE IF NOT EXISTS conversations
    (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,

        peer_id INTEGER UNIQUE,
        peer_name VARCHAR(255),
        peer_type VARCHAR(255)
    );
"""

# Table
PERMISSIONS = """
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

# Table
SETTINGS = """
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

# Table
KICKED = """
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

# Table
BANNED = """
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

# Table
MUTED = """
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

# Table
WARNED = """
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

# Table
QUEUE = """
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

# Table
tables = [CONVERSATIONS, PERMISSIONS, SETTINGS, KICKED, BANNED, MUTED, WARNED, QUEUE]
