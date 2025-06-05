from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.generate.router import router as generate_router
from app.index.router import router as index_router
from app.embed.router import router as embed_router
from fastapi.middleware.cors import CORSMiddleware
from app.index.models import init_db


init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(generate_router)
app.include_router(index_router)
app.include_router(embed_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # oder ["*"] für alle, aber nur zu Testzwecken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
