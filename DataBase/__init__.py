conversation = """CREATE TABLE IF NOT EXISTS conversation
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   PeerID INTEGER UNIQUE ON CONFLICT REPLACE,
                   PeerName TEXT
               );"""

log = """CREATE TABLE IF NOT EXISTS log
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER UNIQUE ON CONFLICT IGNORE,
                    PeerName TEXT,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE
                );"""

permission = """CREATE TABLE IF NOT EXISTS permission
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    UserID INTEGER, 
                    UserName TEXT,
                    UserURL TEXT,
                    PermissionLvl INTEGER,
                    PermissionName TEXT,
                    PeerID INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE
                );"""

setting = """CREATE TABLE IF NOT EXISTS setting
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    SettingName TEXT UNIQUE,
                    SettingStatus INTEGER,
                    PeerID INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE
                );"""

kicked = """CREATE TABLE IF NOT EXISTS kicked
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    KickedByID INTEGER,
                    KickedByName TEXT,
                    KickedByURL TEXT,
                    KickTime INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
                );"""

banned = """CREATE TABLE IF NOT EXISTS banned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    BannedByID INTEGER,
                    BannedByName TEXT,
                    BannedByURL TEXT,
                    BanTime INTEGER,
                    UnbanTime INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE  
                );"""

warned = """CREATE TABLE IF NOT EXISTS warned
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    WarnedByID INTEGER,
                    WarnedByName TEXT,
                    WarnedByURL TEXT,
                    WarnTime INTEGER,
                    UnwarnTime INTEGER,
                    WarnCount INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
                );"""

muted = """CREATE TABLE IF NOT EXISTS muted
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   PeerID INTEGER,
                   UserID INTEGER,
                   UserName TEXT,
                   UserURL TEXT,
                   MutedByID INTEGER,
                   MutedByName TEXT,
                   MutedByURL TEXT,
                   MuteTime INTEGER,
                   UnmuteTime INTEGER ,
                   FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
               );"""

blacklist = """CREATE TABLE IF NOT EXISTS blacklist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    URL TEXT,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
                );"""

whitelist = """CREATE TABLE IF NOT EXISTS whitelist
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    Domain TEXT,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
                );"""

cooldown = """CREATE TABLE IF NOT EXISTS cooldown
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PeerID INTEGER,
                    UserID INTEGER,
                    UserName TEXT,
                    UserURL TEXT,
                    SendTime INTEGER,
                    NextSendTime INTEGER,
                    FOREIGN KEY (PeerID)  REFERENCES conversation (PeerID) ON DELETE CASCADE 
                );"""

tables = [conversation, log, setting, permission, kicked, banned, warned, muted, blacklist, whitelist, cooldown]
