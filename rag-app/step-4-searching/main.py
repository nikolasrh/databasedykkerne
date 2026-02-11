"""
Semantisk søk i embeddings

Bruk:
    python main.py "søketekst"           # Standard søk med 5 resultater
    python main.py "søketekst" --top 3   # Begrens til 3 resultater
    python main.py --demo                # Kjør demo med eksempler
"""
import sys
import argparse
from sentence_transformers import SentenceTransformer
from database import create_connection


MODEL_NAME = "intfloat/multilingual-e5-base"

# Global modell-cache for raskere gjentatte søk
_model = None


def load_model():
    """Last inn embedding-modell (cached, ingen nettverkskall)"""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    return _model


def search(query_text: str, top_k: int = 5, verbose: bool = False) -> list[dict]:
    """
    Semantisk søk - finner relevante tekstchunks basert på mening
    
    Args:
        query_text: Søketekst (norsk eller engelsk)
        top_k: Antall resultater (default: 5)
        verbose: Vis detaljert progresjon (default: False)
    
    Returns:
        Liste med matches og similarity scores
    """
    if verbose:
        print(f"Laster modell: {MODEL_NAME}", file=sys.stderr)
    
    model = load_model()
    
    # E5-modellen krever 'query:' prefix for søketekst
    query_embedding = model.encode(
        f"query: {query_text}",
        normalize_embeddings=True
    )
    
    if verbose:
        print("Kobler til database...", file=sys.stderr)
    
    conn = create_connection()
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                chunk_id,
                text,
                source_file,
                char_start,
                char_end,
                1 - (embedding <=> %s::vector) AS similarity
            FROM embeddings
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding.tolist(), query_embedding.tolist(), top_k))
        
        results = cur.fetchall()
    
    conn.close()
    
    formatted_results = []
    for i, (chunk_id, text, source_file, char_start, char_end, similarity) in enumerate(results):
        formatted_results.append({
            'rank': i + 1,
            'chunk_id': chunk_id,
            'text': text,
            'source_file': source_file,
            'char_start': char_start,
            'char_end': char_end,
            'similarity': float(similarity)
        })
    
    return formatted_results


def print_results(results: list[dict], query: str):
    """Skriv ut søkeresultater i et lesbart format"""
    print(f"\n## Søkeresultater for: \"{query}\"\n")
    print(f"Fant {len(results)} relevante tekstchunks:\n")
    
    for r in results:
        print(f"### Resultat {r['rank']} (likhet: {r['similarity']:.2%})")
        print(f"Kilde: {r['source_file']}")
        print(f"\n{r['text']}\n")
        print("---\n")


def run_demo():
    """Kjør demo med eksempelsøk"""
    print("=" * 60)
    print("DEMO: Semantisk søk med pgvector")
    print("=" * 60)
    
    print("\n### Eksempel 1: Norsk søk ###")
    results = search("Hva er reglene for bevegelse?", top_k=3, verbose=True)
    print_results(results, "Hva er reglene for bevegelse?")
    
    print("\n### Eksempel 2: Engelsk søk ###")
    results = search("What are the movement rules?", top_k=3, verbose=True)
    print_results(results, "What are the movement rules?")


def main():
    parser = argparse.ArgumentParser(
        description="Semantisk søk i vektordatabase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eksempler:
  python main.py "Hvordan fungerer bevegelse?"
  python main.py "combat rules" --top 3
  python main.py --demo
        """
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Søketekst (norsk eller engelsk)"
    )
    parser.add_argument(
        "--top", "-n",
        type=int,
        default=5,
        help="Antall resultater (default: 5)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Kjør demo med eksempelsøk"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Vis detaljert progresjon"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
    elif args.query:
        results = search(args.query, top_k=args.top, verbose=args.verbose)
        print_results(results, args.query)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
