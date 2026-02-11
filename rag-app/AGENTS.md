This is an app that showcases a simple Retrieval-Augmented Generation (RAG) app.

All code is written in Python and runs in a development container.

Folder structure:

```
rag-app/
├─ step-1-convert-pdfs-to-text/
│  ├─ input/
│  ├─ output/
│  ├─ main.py
│  └─ README.md
├─ step-2-create-text-embeddings/
│  ├─ input/
│  ├─ output/
│  ├─ main.py
│  └─ README.md
├─ step-3-load-text-embeddings/
│  ├─ input/
│  ├─ main.py
│  └─ README.md
├─ step-4-searching/
│  ├─ main.py
│  └─ README.md
```

For each step a README.md describes what happens.
All comments and documentation is written in Norwegian using English code expressions. For instance, don't translate "Retrieval-Augmented Generation".

A chunk has the following structure:

```json
{
  "chunk_id": "example-chunk-001",
  "text": "This is the chunk text...",
  "embedding": [],
  "char_start": 0,
  "char_end": 512,
  "source_file": "example"
}
```

Step 3 loads the embeddings into a PostgreSQL database with the pgvector extension.

Step 4 has example code that allows the user to search in the vector database. The search query is embedded the same way as in step 2, then pgvector functions are used to find relevant hits.
