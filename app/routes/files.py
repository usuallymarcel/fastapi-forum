import io
import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse, FileResponse

from schemas.posts import Post
from services.posts import upload_post
from PIL import Image

router = APIRouter(prefix="/files")

UPLOAD_DIR = "app/static/uploads"

MAX_FILE_SIZE = 5 * 1024 * 1024      # 5MB
MAX_DIMENSION = 4000                 # 4000px

ALLOWED_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp"
}

@router.post("/upload")
def upload(post: Post):

    upload_post(post)

    return RedirectResponse(f"/{post.slug}", status_code=303)

@router.post("/upload-image")
async def upload_image(request: Request, file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "invalid file type")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "file too large")

    try:
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(400, "invalid image")

    if image.width > MAX_DIMENSION or image.height > MAX_DIMENSION:
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = ALLOWED_TYPES[file.content_type]
    filename = f"{uuid4()}{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    image.save(filepath, optimize=True, quality=85)

    base_url = str(request.base_url)

    return {"url": f"{base_url}files/image/{filename}"}

@router.get('/image/{file}')
def get_image(file: str):

    filepath = os.path.join(f"{UPLOAD_DIR}", file)

    if not os.path.exists(filepath):
        raise HTTPException(404, "Image not found")
    
    return FileResponse(filepath)