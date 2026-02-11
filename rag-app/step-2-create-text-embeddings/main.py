"""
Lag embeddings av tekst-chunks
"""
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json


MODEL_NAME = "intfloat/multilingual-e5-base"
CHUNK_SIZE = 512
OVERLAP = 50


def load_embedding_model():
    """Last inn embedding-modell (laster ned ~1.1GB første gang)"""
    print(f"Laster modell: {MODEL_NAME}")
    print("Første kjøring laster ned ~1.1GB...")
    return SentenceTransformer(MODEL_NAME)


def chunk_text(text, source_file, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Del tekst opp i overlappende chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        
        chunks.append({
            "text": chunk_text,
            "char_start": start,
            "char_end": min(end, len(text)),
            "source_file": source_file
        })
        
        start += (chunk_size - overlap)
    
    return chunks


def create_embeddings(chunks, model):
    """Lag embeddings for chunks"""
    texts = [f"passage: {chunk['text']}" for chunk in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings


def save_chunk(chunk, embedding, output_dir, chunk_id):
    """Lagre chunk som JSON"""
    data = {
        "chunk_id": chunk_id,
        "text": chunk['text'],
        "embedding": embedding.tolist(),
        "char_start": chunk['char_start'],
        "char_end": chunk['char_end'],
        "source_file": chunk['source_file']
    }
    
    output_path = output_dir / f"{chunk_id}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_all():
    """Prosesser alle markdown-filer"""
    input_dir = Path(__file__).parent / "input"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    md_files = list(input_dir.glob("*.md"))
    
    if not md_files:
        print(f"Ingen markdown-filer funnet i {input_dir}")
        print(f"Kopier filer fra step-1: cp ../step-1-convert-pdfs-to-text/output/*.md input/")
        return
    
    print(f"Fant {len(md_files)} markdown-filer")
    
    model = load_embedding_model()
    
    for md_file in md_files:
        print(f"\nProsesserer: {md_file.name}")
        
        text = md_file.read_text(encoding='utf-8')
        chunks = chunk_text(text, md_file.stem)
        
        print(f"  Laget {len(chunks)} chunks")
        print(f"  Lager embeddings...")
        
        embeddings = create_embeddings(chunks, model)
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{md_file.stem}-chunk-{i+1:03d}"
            save_chunk(chunk, embedding, output_dir, chunk_id)
        
        print(f"  ✓ Lagret {len(chunks)} chunks")
    
    print(f"\nFerdig! Alle chunks lagret i {output_dir.absolute()}")


if __name__ == "__main__":
    process_all()
