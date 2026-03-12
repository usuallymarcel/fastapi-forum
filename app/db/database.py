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
        title TEXT NOT NULL CHECK(length(title) <= 200),
        slug TEXT NOT NULL UNIQUE CHECK(length(slug) <= 200),
        content TEXT NOT NULL CHECK(length(content) <= 50000),
        tags TEXT CHECK(length(tags) <= 50000),
        files TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()