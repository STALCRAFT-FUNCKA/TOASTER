"""This file describes the main queries
that form the structure of the database.
"""

CONVERSATIONS = """
CREATE TABLE IF NOT EXISTS conversations
    (
        conv_id BIGINT PRIMARY KEY,

        conv_name VARCHAR(255),
        conv_mark VARCHAR(10),

        CONSTRAINT conversation UNIQUE (conv_id)
    );
"""

CONVERSATIONS = """
CREATE TABLE IF NOT EXISTS permissions
    (
        record_id INT PRIMARY KEY AUTO_INCREMENT,
        
        conv_id BIGINT,
        user_id BIGINT,
        user_name VARCHAR(100),
        user_permission TINYINT(10),

        FOREIGN KEY (conv_id) REFERENCES conversations(conv_id) ON DELETE CASCADE,
        CONSTRAINT permission UNIQUE (conv_id, user_id)
        
    );
"""

tables = (CONVERSATIONS,)
