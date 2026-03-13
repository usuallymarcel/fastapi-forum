from schemas.posts import Post
from db.database import get_db
from utils.markdown_utils import render_markdown

def get_posts(page, per_page):
    db = get_db()

    offset = (page - 1) * per_page

    posts = db.execute(
        "SELECT * FROM posts ORDER BY created DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    ).fetchall()

    return posts

def get_post_by_slug(slug: str):

    db = get_db()

    post = db.execute(
        "SELECT * FROM posts WHERE slug = ?",
        (slug,)
    ).fetchone()

    if post is None:
        return None, None, None

    html = render_markdown(post["content"])

    tags = post["tags"].split(",") if post["tags"] else []

    return post, html, tags

def get_posts_by_tag(tag: str):

    db = get_db()

    posts = db.execute(
    "SELECT * FROM posts WHERE tags LIKE ? ORDER BY created DESC",
    (f"%{tag}%",)
    ).fetchall()

    return posts

def upload_post(post: Post):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO posts(title, slug, content, tags)
        VALUES(?, ?, ?, ?)
        """,
        (
            post.title,
            post.slug,
            post.content,
            post.tags
        )
    )

    db.commit()

    return cursor.lastrowid
    