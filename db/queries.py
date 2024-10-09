create_tables = """
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    mentor_assigned VARCHAR(50),
    total_qs INT DEFAULT 0,
    easy_total_qs INT DEFAULT 0,
    medium_total_qs INT DEFAULT 0,
    hard_total_qs INT DEFAULT 0,
    profile_link VARCHAR(50),
    name VARCHAR(50) NOT NULL,
    hostler VARCHAR(50),
    cgpa VARCHAR(50),
    phone_number VARCHAR(50),
    email VARCHAR(50),
    pass_year int DEFAULT 0,
    university_rollno VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
