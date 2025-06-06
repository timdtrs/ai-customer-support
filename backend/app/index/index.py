import json
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
from http import HTTPStatus
from docling.document_converter import DocumentConverter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from pydantic import BaseModel
from starlette.responses import Response
from dotenv import load_dotenv
import os
from qdrant_client.http.models import PointIdsList

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large", openai_api_key=os.getenv("OPENAI_API_KEY")
)
# Ersetze Chroma durch Qdrant
qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant_api_key = os.getenv("QDRANT_API_KEY", None)
qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# Collection anlegen, falls sie nicht existiert
if "data" not in [c.name for c in qdrant_client.get_collections().collections]:
    qdrant_client.create_collection(
        collection_name="data",
        vectors_config={
            "size": 3072,
            "distance": "Cosine",
        },  # 3072 für text-embedding-3-large
    )

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="data",
    embedding=embeddings,
)


def read_file_with_docling(file_path):
    """
    Liest den Inhalt einer Datei mit docling ein und gibt den Text zurück.
    :param file_path: Pfad zur Datei
    :return: Inhalt der Datei als String
    """
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()


def index_text_in_vectorstore(text, filename, size=None, doc_type="file"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    points = []
    for idx, chunk in enumerate(chunks):
        points.append(
            {
                "id": str(uuid4()),
                "vector": embeddings.embed_query(chunk),
                "payload": {
                    "title": filename,
                    "size": size,
                    "type": doc_type,
                    "chunk": idx,
                    "page_content": chunk,
                },
            }
        )
    qdrant_client.upsert(collection_name="data", points=points)
    return len(chunks)


class TextEntry(BaseModel):
    title: str
    text: str


class QAPair(BaseModel):
    title: str
    question: str
    answer: str


router = APIRouter()


@router.post("/files")
async def index_files(files: list[UploadFile] = File(...)) -> Response:
    contents = []
    for upload in files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file_bytes = await upload.read()
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            text = read_file_with_docling(tmp_path)
            size_kb = round(len(file_bytes) / 1024)
            num_chunks = index_text_in_vectorstore(text, upload.filename, size=size_kb)
            contents.append(
                {
                    "filename": upload.filename,
                    "size": size_kb,
                    "content": f"{num_chunks} Chunks indiziert",
                }
            )
        except Exception as e:
            contents.append({"filename": upload.filename, "error": str(e)})
    return Response(
        content=json.dumps({"files": contents}),
        status_code=HTTPStatus.ACCEPTED,
    )


@router.post("/texts")
def index_texts(entries: list[TextEntry]) -> Response:
    contents = []
    for entry in entries:
        size_kb = round(len(entry.text.encode("utf-8")) / 1024)
        num_chunks = index_text_in_vectorstore(
            entry.text, entry.title, size=size_kb, doc_type="text"
        )
        contents.append({"title": entry.title, "size": size_kb, "chunks": num_chunks})
    return Response(
        content=json.dumps({"texts": contents}),
        status_code=HTTPStatus.ACCEPTED,
    )


@router.post("/qa")
def index_qa_pairs(pairs: list[QAPair]) -> Response:
    contents = []
    for pair in pairs:
        combined = f"Frage: {pair.question}\nAntwort: {pair.answer}"
        size_kb = round(len(combined.encode("utf-8")) / 1024)
        num_chunks = index_text_in_vectorstore(
            combined, pair.title, size=size_kb, doc_type="qa"
        )
        contents.append({"title": pair.title, "size": size_kb, "chunks": num_chunks})
    return Response(
        content=json.dumps({"qa": contents}),
        status_code=HTTPStatus.ACCEPTED,
    )


@router.get("/indexed-files")
def get_indexed_files() -> Response:
    try:
        # Hole alle Punkte aus der Qdrant-Collection
        scroll_result = qdrant_client.scroll(
            collection_name="data", with_payload=True, with_vectors=False
        )
        unique = {}
        for point in scroll_result[0]:
            meta = point.payload
            title = meta.get("title", "Unbekannt")
            size = meta.get("size", "Unbekannt")
            if title not in unique:
                unique[title] = {
                    "title": title,
                    "size": size,
                    "type": meta.get("type", "Unbekannt"),
                }
        docs = list(unique.values())
        return Response(
            content=json.dumps({"data": docs}),
            status_code=HTTPStatus.ACCEPTED,
        )
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@router.delete("/files/{filename}")
def delete_indexed_file(filename: str) -> Response:
    try:
        # Finde alle IDs mit passendem Dateinamen
        scroll_result = qdrant_client.scroll(
            collection_name="data", with_payload=True, with_vectors=False
        )
        ids_to_delete = [
            point.id
            for point in scroll_result[0]
            if point.payload.get("title") == filename
        ]
        if ids_to_delete:
            qdrant_client.delete(
                collection_name="data",
                points_selector=PointIdsList(points=ids_to_delete),
            )
            return Response(
                content=json.dumps(
                    {
                        "success": True,
                        "deleted": filename,
                        "count": len(ids_to_delete),
                    }
                ),
                status_code=HTTPStatus.OK,
            )
        else:
            return Response(
                content=json.dumps({"success": False, "error": "Datei nicht gefunden"}),
                status_code=HTTPStatus.NOT_FOUND,
            )
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


class DeleteFileSchema(BaseModel):
    filename: str


@router.post("/delete-file")
def delete_indexed_file_post(data: DeleteFileSchema) -> Response:
    try:
        scroll_result = qdrant_client.scroll(
            collection_name="data", with_payload=True, with_vectors=False
        )
        ids_to_delete = [
            point.id
            for point in scroll_result[0]
            if point.payload.get("title") == data.filename
        ]
        if ids_to_delete:
            qdrant_client.delete(
                collection_name="data",
                points_selector=PointIdsList(points=ids_to_delete),
            )
            return Response(
                content=json.dumps(
                    {
                        "success": True,
                        "deleted": data.filename,
                        "count": len(ids_to_delete),
                    }
                ),
                status_code=HTTPStatus.OK,
            )
        else:
            return Response(
                content=json.dumps({"success": False, "error": "Datei nicht gefunden"}),
                status_code=HTTPStatus.NOT_FOUND,
            )
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
