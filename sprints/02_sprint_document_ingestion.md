# Sprint 2 — Document Ingestion

## Goal

Populate Pinecone with documentation.

## Tasks

### Build Ingestion Pipeline

Flow:

Document
→ Load
→ Chunk
→ Embed
→ Pinecone

### Implement

Create:

```text
app/ingestion/
```

Components:

* document loader
* chunker
* embedding service
* Pinecone upsert

### Supported Files

* txt
* md

Optional:

* pdf

## Definition of Done

* Documents successfully indexed
* Pinecone contains vectors
* Metadata stored correctly
