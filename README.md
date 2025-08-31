# Databasedykkerne

Dette trenger du:
- VS Code
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Colima eller Docker Desktop

Dette repoet inneholder eksempel-applikasjoner med lokalt databaseoppsett for populære teknologier som brukes på Trondheimskontoret. Det er lagt opp til at man enkelt skal kunne komme i gang med lokal utvikling for hver applikasjon ved å bruke [Dev Containers](https://github.com/devcontainers). Databaser settes opp på utsiden med [Docker Compose](https://docs.docker.com/compose/). Man står fritt til å bruke den databasen man ønsker for hver applikasjon.

## Oppsett av Docker

MSSQL server har ingen container images for arm64 (x86_64).
For å kjøre dette trenger man å emulere amd64 (aarch64).
To vanlige løsninger for dette er Docker Desktop og Colima.

### Docker Desktop

TODO: Legg til beskrivelse

### Colima

Installer Colima:

```sh
brew install colima
```

Man har to valg for å kjøre amd64-prosesser:
- Lage en aarch64 (arm64) virtuell maskin som er emulert av Apple Virtualization Framework (vz) med Rosetta skrudd på, slik at den kan kjøre amd64-prosesser ved at Rosetta oversetter prosessor-instruksjoner.
- Lage en x86_64 (amd64) virtuell maskin som er emulert av QEMU som kun kan kjøre amd64-prosesser.

Vi fokuserer på den første fordi det er raskere, og man trenger kun én VM hvis man også vil kjøre arm64-prosesser.

For å lage en Colima-instans:

```sh
colima start --vm-type=vz --vz-rosetta
```

## Starte databaser og appikasjoner

Starte ønsket database:
```sh
docker compose up postgres
docker compose up mssql
docker compose up oracle
```

For å utvikle mot en applikasjon med Dev Containers må root av applikasjonen åpnes i et nytt VS Code-vindu.

```sh
code example-apps/python-django
```

Hvis man har Dev Containers extensionen blir man spurt om å åpne mappen på nytt med Dev Containers. Alternativt kan man kjøre kommandoen manuelt. Trykk `Cmd + Shift + P` og søk etter `Dev Containers: Reopen in Container`.

