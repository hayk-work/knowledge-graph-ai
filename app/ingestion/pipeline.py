from pathlib import Path

from app.config import DATA_DIR
from app.ingestion.chunker import chunk_text
from app.ingestion.loader import collect_files, load_document
from app.mcp import pinecone


def _data_root() -> Path:
    return Path(DATA_DIR).resolve()


def _resolve_path(path: str | Path | None = None) -> Path:
    if path is None or str(path).strip() == "":
        resolved = _data_root()
    else:
        candidate = Path(path)
        if candidate.is_absolute():
            resolved = candidate
        else:
            cwd_path = (Path.cwd() / candidate).resolve()
            data_path = (_data_root() / candidate).resolve()
            if cwd_path.exists():
                resolved = cwd_path
            else:
                resolved = data_path

    if not resolved.exists():
        raise FileNotFoundError(f"Path not found: {resolved}")

    return resolved


def _source_name(file_path: Path) -> str:
    data_root = _data_root()
    try:
        return str(file_path.relative_to(data_root))
    except ValueError:
        return str(file_path)


def ingest_file(path: str | Path) -> dict:
    file_path = _resolve_path(path)
    if not file_path.is_file():
        raise ValueError(f"Expected a file path: {file_path}")

    text = load_document(file_path)
    chunks = chunk_text(text)
    source = _source_name(file_path)
    indexed = pinecone.upsert_chunks(source=source, chunks=chunks)

    return {
        "file": source,
        "chunks_indexed": indexed,
    }


def ingest_path(path: str | Path | None = None) -> dict:
    target = _resolve_path(path)
    files = collect_files(target)

    results = [ingest_file(file_path) for file_path in files]
    total_chunks = sum(result["chunks_indexed"] for result in results)

    return {
        "files_processed": len(results),
        "chunks_indexed": total_chunks,
        "files": results,
    }


if __name__ == "__main__":
    import json
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps(ingest_path(target), indent=2))
