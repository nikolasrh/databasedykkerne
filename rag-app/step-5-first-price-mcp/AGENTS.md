# RAG-søk for AI-agenter

Du har tilgang til en vektordatabase med dokumenter. **Før du svarer på spørsmål, skal du alltid utføre et semantisk søk** for å hente relevant informasjon fra databasen.

## Hvordan utføre søk

Kjør følgende kommando fra utsiden av devcontaineren:

```bash
docker exec -it rag-app-devcontainer python /workspaces/databasedykkerne/rag-app/step-4-searching/main.py "din søketekst her"
```

### Eksempler

```bash
# Søk på norsk
docker exec -it rag-app-devcontainer python /workspaces/databasedykkerne/rag-app/step-4-searching/main.py "Hvordan fungerer bevegelse?"

# Søk på engelsk
docker exec -it rag-app-devcontainer python /workspaces/databasedykkerne/rag-app/step-4-searching/main.py "What are the combat rules?"

# Begrens til 3 resultater
docker exec -it rag-app-devcontainer python /workspaces/databasedykkerne/rag-app/step-4-searching/main.py "bevegelse" --top 3
```

## Forutsetninger

For at søket skal fungere må følgende være startet:

1. **Devcontainer**: `rag-app-devcontainer` må kjøre
2. **Database**: `postgres-pgvector` må kjøre med data lastet inn

## Arbeidsflyt

1. **Motta spørsmål** fra bruker
2. **Utfør semantisk søk** med relevant søketekst
3. **Les resultatene** - de inneholder relevant kontekst fra dokumentene
4. **Formuler svar** basert på søkeresultatene

## Output-format

Søket returnerer resultater i markdown-format:

```
## Søkeresultater for: "søketekst"

Fant N relevante tekstchunks:

### Resultat 1 (likhet: 87.23%)
Kilde: dokument-navn

Tekstinnhold fra dokumentet...

---
```

## Tips

- Bruk norske søkeord for norske dokumenter
- Modellen forstår semantisk likhet, så eksakte ord er ikke nødvendig
- Ved usikkerhet, prøv flere søk med ulike formuleringer
- Sjekk similarity-score - høyere score (nærmere 100%) betyr mer relevant treff
