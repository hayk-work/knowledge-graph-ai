#!/usr/bin/env python3
"""
One-time script to index sample documentation into Pinecone.

Usage (from project root):
    uv run python scripts/seed_pinecone.py

Indexes all .md / .txt files under DATA_DIR (default: data/docs).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import DATA_DIR, PINECONE_INDEX
from app.ingestion.pipeline import ingest_path


def main() -> int:
    print(f"Indexing documents from: {Path(DATA_DIR).resolve()}")
    print(f"Pinecone index: {PINECONE_INDEX}")
    print("-" * 50)

    result = ingest_path()

    print(json.dumps(result, indent=2))
    print("-" * 50)
    print(
        f"Done: {result['files_processed']} file(s), "
        f"{result['chunks_indexed']} chunk(s) upserted."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
