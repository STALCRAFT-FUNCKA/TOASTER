"""
This file describes the main queries that form the structure of the database.
"""
# TODO: add new Tables
CONVERSATIONS = """
CREATE TABLE IF NOT EXISTS conversations
    (
        conv_id BIGINT PRIMARY KEY,

        conv_name VARCHAR(255),
        conv_mark VARCHAR(10),

        CONSTRAINT conversation UNIQUE conv_id
    );
"""

tables = (CONVERSATIONS,)
