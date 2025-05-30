# Backend für Customer Support Dashboard

Dieses Verzeichnis enthält das Backend auf Basis von FastAPI.

## Setup

1. Python-Umgebung erstellen (optional):
   python3 -m venv venv
   source venv/bin/activate

2. FastAPI und Uvicorn installieren:
   pip install fastapi uvicorn

3. Beispiel-Start:
   uvicorn main:app --reload

## Docker & Compose

### Start mit Docker Compose

1. Erstelle eine `.env`-Datei im Projektverzeichnis (siehe `.env.example`).
2. Starte alle Services:

   ```sh
   docker compose up --build
   ```

- Das Backend ist unter http://localhost:8000 erreichbar.
- Das Frontend ist unter http://localhost:5173 erreichbar.
- Qdrant läuft intern auf Port 6333.

### Hinweise
- Die Umgebungsvariablen für OpenAI und Qdrant werden aus der `.env` geladen.
- Änderungen am Code werden im Container automatisch erkannt (Hot Reload).

## Struktur
- main.py: Einstiegspunkt für FastAPI
- requirements.txt: Abhängigkeiten

Weitere Module und Routen können im Verlauf ergänzt werden.
