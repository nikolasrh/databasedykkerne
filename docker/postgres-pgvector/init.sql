-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE embeddings (
    chunk_id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(768),
    char_start INT,
    char_end INT,
    source_file TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create vector similarity index (IVFFlat for cosine distance)
-- Note: Index is created after table is populated for better performance
-- For small datasets, this index helps with query speed
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
