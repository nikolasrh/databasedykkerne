# RAG-applikasjon

En RAG (Retrieval-Augmented Generation) applikasjon som demonstrerer semantisk søk i PDF-dokumenter.

## Steg

1. **step-1-convert-pdfs-to-text**: Konverter PDF til tekst
2. **step-2-create-text-embeddings**: Lag embeddings
3. **step-3-load-text-embeddings**: Last inn i PostgreSQL
4. **step-4-searching**: Semantisk søk
5. **step-5-first-price-mcp**: AI-agent integrasjon via MCP

Hvert steg har sin egen README.

## Kom i gang

### 1. Start database

Fra `databasedykkerne/`:

```bash
docker compose up postgres-pgvector -d
```

### 2. Åpne i Dev Container

```bash
code rag-app
```

Velg "Reopen in Container" (Cmd+Shift+P).

### 3. Kjør hvert steg

Se README og kjør Python-script:

```bash
python main.py
```

## Lenker

- [Vectors - 3Blue1Brown](https://youtu.be/fNk_zzaMoSs)
- [What is a Vector Database? - IBM Technology](https://youtu.be/gl1r1XV0SLw)
- [What are Word Embeddings? - IBM Technology](https://youtu.be/wgfSDrqYMJ4)
- [What is a Knowledge Graph? - IBM Technology](https://youtu.be/y7sXDpffzQQ)
- [GraphRAG: The Marriage of Knowledge Graphs and RAG – Emil Eifrem](https://youtu.be/knDDGYHnnSI)
