conversation = """CREATE TABLE IF NOT EXISTS conversation
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   PeerID INTEGER UNIQUE ON CONFLICT REPLACE,
                   PeerName TEXT,
                   Destination TEXT
               );"""

permission = """CREATE TABLE IF NOT EXISTS permission
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserID INTEGER, 
                    UserName TEXT,
                    UserURL TEXT,
                    PermissionLvl INTEGER,
                    PermissionName TEXT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    CONSTRAINT someone UNIQUE (UserID, PeerID) ON CONFLICT REPLACE
                );"""

setting = """CREATE TABLE IF NOT EXISTS setting
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    SettingName TEXT UNIQUE ON CONFLICT IGNORE,
                    SettingStatus INTEGER,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE
                );"""

kicked = """CREATE TABLE IF NOT EXISTS kicked
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    KickedByID INTEGER,
                    KickedByName TEXT,
                    KickedByURL TEXT,
                    KickTime INTEGER,
                    CONSTRAINT someone UNIQUE (UserID, PeerID) ON CONFLICT IGNORE
                );"""

banned = """CREATE TABLE IF NOT EXISTS banned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    BannedByID INTEGER,
                    BannedByName TEXT,
                    BannedByURL TEXT,
                    BanTime INTEGER,
                    UnbanTime INTEGER,
                    CONSTRAINT someone UNIQUE (UserID, PeerID) ON CONFLICT IGNORE  
                );"""

muted = """CREATE TABLE IF NOT EXISTS muted
               (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    MutedByID INTEGER,
                    MutedByName TEXT,
                    MutedByURL TEXT,
                    MuteTime INTEGER,
                    UnmuteTime INTEGER ,
                    CONSTRAINT someone UNIQUE (UserID, PeerID) ON CONFLICT IGNORE 
               );"""

warned = """CREATE TABLE IF NOT EXISTS warned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    WarnedByID INTEGER,
                    WarnedByName TEXT,
                    WarnedByURL TEXT,
                    WarnTime INTEGER,
                    UnwarnTime INTEGER,
                    WarnCount INTEGER,
                    CONSTRAINT someone UNIQUE (UserID, PeerID) ON CONFLICT REPLACE 
                );"""

blacklist = """CREATE TABLE IF NOT EXISTS blacklist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    URL TEXT
                );"""

whitelist = """CREATE TABLE IF NOT EXISTS whitelist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    Domain TEXT
                );"""

queue = """CREATE TABLE IF NOT EXISTS queue
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER REFERENCES conversation (PeerID) ON DELETE CASCADE,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    SendTime INTEGER,
                    NextSendTime INTEGER
                );"""

tables = [conversation, setting, permission, kicked, banned, warned, muted, blacklist, whitelist, queue]
