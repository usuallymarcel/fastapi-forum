from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from schemas.posts import Post
from services.posts import get_post_by_slug, get_posts_by_tag, upload_post

router = APIRouter(prefix="/posts")

templates = Jinja2Templates(directory="app/templates")

@router.get("/{slug}")
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

@router.post("/upload")
def upload(post: Post):

    upload_post(post)

    return RedirectResponse(f"/{post.slug}", status_code=303)