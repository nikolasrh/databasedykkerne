# Steg 3: Last embeddings inn i database

1. Start database (fra `databasedykkerne/`): `docker compose up postgres-pgvector -d`
2. Kopier JSON fra step-2: `cp ../step-2-create-text-embeddings/output/*.json input/`
3. Kjør script: `python main.py`
