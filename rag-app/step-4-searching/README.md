# Steg 4: Semantisk søk

Søkescriptet bruker samme embedding-modell som i steg 2 for å konvertere søketeksten til en vektor, og bruker deretter pgvector for å finne lignende tekstchunks.

## Forutsetninger

1. Database kjører (`docker compose up -d postgres-pgvector`)
2. Data er lastet inn (steg 3)

## Bruk

```bash
# Søk med norsk tekst
python main.py "Hvordan fungerer bevegelse?"

# Søk med engelsk tekst
python main.py "What are the combat rules?"

# Begrens antall resultater
python main.py "bevegelse" --top 3

# Vis detaljert progresjon
python main.py "bevegelse" --verbose

# Kjør demo med eksempelsøk
python main.py --demo
```

## Output

Scriptet skriver resultater til stdout i et lesbart markdown-format:

```
## Søkeresultater for: "bevegelse"

Fant 5 relevante tekstchunks:

### Resultat 1 (likhet: 87.23%)
Kilde: example-document

Tekstinnhold fra chunken...

---
```

## Frivillige oppgaver

- Hvilke muligheter finnes for å indeksere dataen? Hva er i så fall fordeler og ulemper?
- Velg deg ut en chunk. Finn andre chunks som ligner på den du valgte. Sammenlign den opprinnelige teksten og se om det gir mening.
- Finnes det andre måter å sammenligne vektorene på enn det scriptet bruker?
