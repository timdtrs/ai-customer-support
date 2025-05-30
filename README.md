# Customer Support Dashboard

Dieses Projekt besteht aus drei Services:
- Qdrant (Vektor-Datenbank)
- Backend (FastAPI)
- Frontend (Vue.js)

## Schnellstart

1. Kopiere die Datei `.env.example` zu `.env` und trage deine Schlüssel ein.
2. Starte alle Services:

   ```sh
   docker compose up --build
   ```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Qdrant: http://localhost:6333

## Verzeichnisstruktur
- `backend/` – FastAPI Backend
- `frontend/` – Vue.js Frontend

## Hinweise
- Die Umgebungsvariablen werden aus `.env` geladen.
- Für OpenAI wird ein API-Key benötigt.
- Qdrant persistiert Daten im Volume `qdrant_data`.
# solvee
