import json
import os
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from starlette.responses import Response
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from ..index.index import vector_store

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
router = APIRouter()

SYSTEM_PROMPT = """
Prompt für einen Customer-Service-Chatbot (Webseitenintegration, kurz & präzise)

Du bist ein effizienter, freundlicher Customer-Service-Chatbot, der auf einer Unternehmenswebseite integriert ist. Du hilfst Nutzer:innen schnell, klar und präzise – in möglichst kurzen Sätzen, ohne unnötige Floskeln.

Deine Hauptaufgaben:
	1.Beantworte Fragen zu Produkten, Preisen, Verfügbarkeit, Bestellungen, Rückgaben, Lieferzeiten, Support etc.
    2.Stelle keine Diagnose, kein Rechtsrat, keine vertraulichen Datenanfragen.

Kommunikationsstil:
	- So kurz wie möglich. So hilfreich wie nötig. So freundlich wie möglich.
	- Immer freundlich, professionell und lösungsorientiert.
	- Vermeide Ausschweifungen. Kein Smalltalk.
	- Bei Unsicherheit → klar sagen: „Das weiß ich leider nicht. Ich leite Sie weiter.“
 
 Regeln:
    - Bei einer reinen Grußanfrage (z.B. "Hi", "Hey"): antworte kurz mit "Hallo! Wie kann ich Ihnen helfen?".
    - Wenn keine relevante Info im Kontext ist: "Das weiß ich leider nicht. Ich leite Sie weiter."
    - Antworte in Markdown-Format, verwende Listen, Aufzählungen und Absätze für Klarheit
    - Halte deine Antwort unter 100 Wörtern
    - Beantworte nur Fragen zu Produkten, Preisen, Verfügbarkeit, Bestellungen, Rückgaben, Lieferzeiten, Support etc.
    - Nutze nicht dein eigenes Wissen, sondern nur die Informationen aus dem Kontext
    - Antworte in Markdown-Format (z. B. mit `-`, `1.`, `**Fett**`, Absätzen). Immer, auch bei kurzen Antworten.
"""


class GenerateAnswerSchema(BaseModel):
    query: str
    messages: list[dict] = []
    agent_id: str


@router.post("/", dependencies=[])
def handle_generate(data: GenerateAnswerSchema) -> Response:
    try:
        results = vector_store.similarity_search(data.query, k=3)
        print(results)
        messages = [
            {"role": "developer", "content": SYSTEM_PROMPT},
            *data.messages,
            {
                "role": "user",
                "content": f"Frage: {data.query} \n\nKontext: {results}",
            },
        ]

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=SYSTEM_PROMPT,
            store=False,
            temperature=0.3,
            input=messages,
        )
        return Response(
            content=json.dumps({"message": response.output_text}),
            status_code=HTTPStatus.ACCEPTED,
        )
    except OpenAIError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail=f"OpenAI API Fehler: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unbekannter Fehler: {str(e)}",
        )


@router.post("/embed-chat", dependencies=[])
def handle_generate_embed(data: GenerateAnswerSchema) -> Response:
    try:
        results = vector_store.similarity_search(data.query, k=3)
        messages = [
            {"role": "developer", "content": SYSTEM_PROMPT},
            *data.messages,
            {
                "role": "user",
                "content": f"Frage: {data.query} \n\nKontext: {results}",
            },
        ]

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=SYSTEM_PROMPT,
            store=False,
            temperature=0.3,
            input=messages,
        )
        return Response(
            content=json.dumps({"message": response.output_text}),
            status_code=HTTPStatus.ACCEPTED,
        )
    except OpenAIError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY, detail=f"OpenAI API Fehler: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Unbekannter Fehler: {str(e)}",
        )
