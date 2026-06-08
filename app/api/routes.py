from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

from app.graph.sources import extract_sources
from app.graph.workflow import run_rag
from app.ingestion.pipeline import ingest_path
from app.memory.checkpoint import delete_thread_checkpoint

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    thread_id: str | None = None


class ContextDocument(BaseModel):
    text: str
    source: str
    score: float
    origin: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    context: list[ContextDocument]
    thread_id: str


class IngestRequest(BaseModel):
    path: str = Field(default="", description="File or directory under data/docs")


class IngestResponse(BaseModel):
    files_processed: int
    chunks_indexed: int
    files: list[dict]


class DeleteThreadResponse(BaseModel):
    deleted: bool
    thread_id: str


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    thread_id = request.thread_id or str(uuid4())
    result = run_rag(request.question, thread_id)
    context = [ContextDocument(**doc) for doc in result["context"]]

    return AskResponse(
        answer=result["answer"],
        sources=extract_sources(result["context"]),
        context=context,
        thread_id=thread_id,
    )


@router.delete("/threads/{thread_id}", response_model=DeleteThreadResponse)
def delete_thread(thread_id: str):
    delete_thread_checkpoint(thread_id)
    return DeleteThreadResponse(deleted=True, thread_id=thread_id)


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    try:
        result = ingest_path(request.path or None)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IngestResponse(**result)
