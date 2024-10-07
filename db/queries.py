create_tables = """
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    profile_link VARCHAR(50),
    mentor_assigned VARCHAR(50),
    hostler VARCHAR(50),
    total_qs INT DEFAULT 0,
    easy_total_qs INT DEFAULT 0,
    medium_total_qs INT DEFAULT 0,
    hard_total_qs INT DEFAULT 0
"""
