from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graph.sources import extract_sources
from app.graph.workflow import run_rag
from app.ingestion.pipeline import ingest_path

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class ContextDocument(BaseModel):
    text: str
    source: str
    score: float
    origin: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    context: list[ContextDocument]


class IngestRequest(BaseModel):
    path: str = Field(default="", description="File or directory under data/docs")


class IngestResponse(BaseModel):
    files_processed: int
    chunks_indexed: int
    files: list[dict]


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    result = run_rag(request.question)
    context = [ContextDocument(**doc) for doc in result["context"]]

    return AskResponse(
        answer=result["answer"],
        sources=extract_sources(result["context"]),
        context=context,
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    try:
        result = ingest_path(request.path or None)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IngestResponse(**result)
