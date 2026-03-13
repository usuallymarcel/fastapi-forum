from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes import files
from services.posts import get_posts
from routes import posts
from db.database import init_db

app = FastAPI()

init_db()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts.router)
app.include_router(files.router)

POSTS_PER_PAGE = 5

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def index(request: Request, page: int = 1):

    posts = get_posts(page, POSTS_PER_PAGE)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "page": page}
    )