from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from schemas.posts import Post
from services.posts import get_posts, get_post_by_slug, get_posts_by_tag, upload_post

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

@router.post("/upload")
def upload(post: Post):

    upload_post(post)

    return RedirectResponse(f"/{post.slug}", status_code=303)



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