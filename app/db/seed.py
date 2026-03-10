import sqlite3

conn = sqlite3.connect("posts.db")

conn.execute("""
INSERT INTO posts (title, slug, content)
VALUES (?, ?, ?)
""", (
    "First Post",
    "first-post",
    """
# Hello World

This is my **first blog post**.

![Test Image](/static/images/test.jpg)
"""
))

conn.commit()


conn.execute("""
INSERT INTO posts (title, slug, content, tags)
VALUES (?, ?, ?, ?)
""", (
    "Learning FastAPI",
    "learning-fastapi",
    """
# FastAPI is great

You can write **very small backends**.

![Example](/static/images/test.png)
""",
    "python,fastapi,backend"
))

conn.commit()