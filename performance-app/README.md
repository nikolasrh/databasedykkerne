# Ytelsesoptimaliserings-workshop

Python-applikasjon for å optimalisere database-spørringer.

## Kom i gang

Åpne mappen `performance-app` i eget VS Code-vindu:
```
code performance-app
```

Installer Dev Containers extensionen, og trykk dialogen for å åpne med Dev Containers.
Alternativt Cmd+Shift+P og søk etter "Reopen in Container".

Kjør setup script:
```bash
./setup.sh
```

Scriptet starter PostgreSQL, kjører migreringer og seeder databasen.
Ta en titt i [001_create_product_scehma.up.sql](migrations/001_create_product_schema.up.sql) for å se hvordan tabellene ser ut.

Åpne `test_task_1.py` og les oppgaven i toppen av filen.

Kjør første test:
```bash
pytest src/test_task_1.py
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
