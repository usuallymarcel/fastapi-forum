import sqlite3

DB = "posts.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        slug TEXT UNIQUE,
        content TEXT,
        tags TEXT,
        files TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()