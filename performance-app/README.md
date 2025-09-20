# Ytelsesoptimaliserings-workshop

Python-applikasjon for å optimalisere database-spørringer.

## Kom i gang

Start PostgreSQL fra root i repoet:
```bash
docker compose up postgres -d
```

Åpne applikasjonen i nytt VS Code-vindu:
```
code performance-app
```

Installer Dev Containers extensionen, og trykk dialogen for å åpne med Dev Containers.
Alternativt Cmd+Shift+P og søk etter "Reopen in Container".

Kjør migrasjoner:
```bash
./migrate.sh up
```

Seed databasen:
```bash
python src/seed_database.py
```

Start PostgreSQL med begrensede ressurser fra root i repoet:
```bash
docker compose stop postgres
docker compose -f docker-compose.yml -f docker-compose.resources.yml up postgres -d
```

Kjør tester:
```bash
pytest
```

Til å begynne med kjører testene ganske treigt.
Lag index-er og tilpass spørringene for å få bedre resultater.

## Golang migrate

Scriptet `./migrate.sh` er en wrapper rundt [golang-migrate](https://github.com/golang-migrate/migrate) som kjøres via Docker.

Når man legger til nye migreringer må de slutte på `.up.sql`.
Det er valgfritt å lage en "down" migrering som slutter på `.down.sql`.
Tallet først i filnavnet bestemmer rekkefølgen.

Rulle én tilbake:
```sh
./migrate.sh down 1
```

Legg til nye SQL-filer med index-er i `./performance-app/migrations`.
