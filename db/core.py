"""
This file describes the main queries that form the structure of the database.
"""
# TODO: add new Tables

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

# Tables
tables = []
