from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown

from database import get_db, init_db

# from feedgen.feed import FeedGenerator

app = FastAPI()

init_db()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

POSTS_PER_PAGE = 5


@app.get("/")
def index(request: Request, page: int = 1):

    db = get_db()

    offset = (page - 1) * POSTS_PER_PAGE

    posts = db.execute(
        "SELECT * FROM posts ORDER BY created DESC LIMIT ? OFFSET ?",
        (POSTS_PER_PAGE, offset)
    ).fetchall()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "page": page}
    )


@app.get("/post/{slug}")
def post(request: Request, slug: str):

    db = get_db()

    post = db.execute(
        "SELECT * FROM posts WHERE slug = ?",
        (slug,)
    ).fetchone()

    html = markdown.markdown(post["content"])

    tags = post["tags"].split(",") if post["tags"] else []

    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post, "content": html, "tags": tags}
    )


@app.get("/tag/{tag}")
def posts_by_tag(request: Request, tag: str):

    db = get_db()

    posts = db.execute(
        "SELECT * FROM posts WHERE tags LIKE ? ORDER BY created DESC",
        (f"%{tag}%",)
    ).fetchall()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "page": 1}
    )


# @app.get("/rss")
# def rss():

#     db = get_db()

#     posts = db.execute(
#         "SELECT * FROM posts ORDER BY created DESC LIMIT 10"
#     ).fetchall()

#     fg = FeedGenerator()
#     fg.title("My FastAPI Blog")
#     fg.link(href="http://localhost:8000", rel="alternate")
#     fg.description("Blog feed")

#     for p in posts:
#         fe = fg.add_entry()
#         fe.title(p["title"])
#         fe.link(href=f"http://localhost:8000/post/{p['slug']}")
#         fe.description(p["content"])

#     return Response(fg.rss_str(), media_type="application/xml")