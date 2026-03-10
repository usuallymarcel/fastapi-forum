from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import posts
from db.database import init_db

app = FastAPI()

init_db()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(posts.router)