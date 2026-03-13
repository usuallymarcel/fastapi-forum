import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse, FileResponse

from schemas.posts import Post
from services.posts import upload_post
import pathlib

router = APIRouter(prefix="/files")

UPLOAD_DIR = "app/static/uploads"

@router.post("/upload")
def upload(post: Post):

    upload_post(post)

    return RedirectResponse(f"/{post.slug}", status_code=303)

@router.post("/upload-image")
def upload_image(request: Request, file: UploadFile = File(...)):
    allowed = ["image/png", "image/jpeg", "image/webp"]

    if file.content_type not in allowed:
        raise HTTPException(400, "invalid file type")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = pathlib.Path(file.filename).suffix
    filename = f"{uuid4()}{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    base_url = request.base_url

    return {"url": f"{base_url}files/image/{filename}"}

@router.get('/image/{file}')
def get_image(file: str):

    filepath = os.path.join(f"{UPLOAD_DIR}", file)

    if not os.path.exists(filepath):
        raise HTTPException(404, "Image not found")
    
    return FileResponse(filepath)