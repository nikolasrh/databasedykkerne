# Ytelsesoptimaliserings-workshop

Python-applikasjon for å optimalisere database-spørringer.

## Kom i gang

### Lag miljø med Dev Containers

Åpne mappen `performance-app` i eget VS Code-vindu:
```
code performance-app
```

Installer Dev Containers extensionen, og trykk dialogen for å åpne med Dev Containers.
Alternativt Cmd+Shift+P og søk etter "Reopen in Container".

### Lag miljø uten Dev Containers

Opprett et virtuelt miljø:
```bash
python3 -m venv .venv
```

Aktiver det virtuelle miljøet:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

Installer avhengigheter:
```bash
pip install -e .
```

### Kjør setup og første oppgave

Kjør setup script:
```bash
./setup.sh
```

Scriptet starter PostgreSQL, kjører migreringer og seeder databasen.
Ta en titt i [001_create_product_scehma.up.sql](migrations/001_create_product_schema.up.sql) for å se hvordan tabellene ser ut.

Åpne `test_oppgave_1.py` og les oppgaven i toppen av filen.

Kjør første test (oppgave):
```bash
pytest src/test_oppgave_1.py
```

## Golang migrate

Scriptet `./migrate.sh` er en wrapper rundt [golang-migrate](https://github.com/golang-migrate/migrate) som kjøres via Docker.

Når man legger til nye migreringer må de slutte på `.up.sql`.
Det er valgfritt å lage en "down" migrering som slutter på `.down.sql`.
Tallet først i filnavnet bestemmer rekkefølgen.

Legg til nye SQL-filer med index-er i `./performance-app/migrations`.

### Nyttige kommandoer

Kjør alle databasemigreringer:
```bash
./migrate.sh up
```

Gå til en spesifikk versjon:
```bash
./migrate.sh goto 2
```

Hvis man endrer på migreringer som allerede er kjørt, kan database-versjonen bli "dirty".
Da kan man tvinge den til den versjonen man mener er riktig med `force`:

```bash
./migrate.sh force 1
```
