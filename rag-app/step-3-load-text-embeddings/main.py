"""
Last embeddings inn i PostgreSQL
"""
from pathlib import Path
import json
from database import create_connection


def load_chunk(conn, chunk_data):
    """Last inn en chunk i databasen"""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO embeddings 
            (chunk_id, text, embedding, char_start, char_end, source_file)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id) DO UPDATE 
            SET text = EXCLUDED.text,
                embedding = EXCLUDED.embedding,
                char_start = EXCLUDED.char_start,
                char_end = EXCLUDED.char_end,
                source_file = EXCLUDED.source_file,
                created_at = NOW()
        """, (
            chunk_data['chunk_id'],
            chunk_data['text'],
            chunk_data['embedding'],
            chunk_data['char_start'],
            chunk_data['char_end'],
            chunk_data['source_file']
        ))


def load_all():
    """Last inn alle chunks fra JSON-filer"""
    input_dir = Path(__file__).parent / "input"
    
    json_files = list(input_dir.glob("*.json"))
    
    if not json_files:
        print(f"Ingen JSON-filer funnet i {input_dir}")
        print(f"Kopier filer fra step-2: cp ../step-2-create-text-embeddings/output/*.json input/")
        return
    
    print(f"Fant {len(json_files)} chunks å laste inn")
    print("Kobler til database...")
    
    conn = create_connection()
    
    for i, json_file in enumerate(json_files, 1):
        with open(json_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
        
        load_chunk(conn, chunk_data)
        
        if i % 10 == 0:
            print(f"  Lastet {i}/{len(json_files)} chunks...")
    
    conn.commit()
    conn.close()
    
    print(f"✓ Ferdig! Lastet inn {len(json_files)} chunks")
    print(f"\nVerifiser: docker exec -i postgres-pgvector psql -U postgres -c \"SELECT COUNT(*) FROM embeddings;\"")


if __name__ == "__main__":
    load_all()
