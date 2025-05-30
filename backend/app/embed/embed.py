from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pathlib import Path

router = APIRouter()


@router.get("/get/{bot_id}", response_class=HTMLResponse)
def embed(bot_id: str):
    html_path = Path(__file__).parent / "embed.html"
    html = html_path.read_text(encoding="utf-8")
    # Bot-ID ersetzen
    html = html.replace("{{bot_id}}", bot_id)
    return html
