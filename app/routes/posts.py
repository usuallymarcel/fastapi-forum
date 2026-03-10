from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from services.posts import get_posts, get_post_by_slug, get_posts_by_tag

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

POSTS_PER_PAGE = 5

@router.get("/")
def index(request: Request, page: int = 1):

    posts = get_posts(page, POSTS_PER_PAGE)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "page": page}
    )

@router.get("/post/{slug}")
def post(request: Request, slug: str):

    post, html , tags = get_post_by_slug(slug)

    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post, "content": html, "tags": tags}
    )

@router.get("/tag/{tag}")
def posts_by_tag(request: Request, tag: str):

    posts = get_posts_by_tag(tag)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "page": 1}
    )