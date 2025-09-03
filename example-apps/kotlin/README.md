# Kotlin

Tooling for Kotlin i VS Code er ikke best.
Bruk IntelliJ hvis du har det og ønsker det lille ekstra.

Her står man fritt til å teste det man måtte ønske.

Forslag:
- Reactive streaming fra databasen med RD2BC og Postgres
- Bruk Exposed som ORM (object-relational mapping), og for å lage migreringer

## Kommandoer

Kjør applikasjon:

```bash
./gradlew run
```

Kjør tester:

```bash
./gradlew test --rerun
```

## Kommandoer brukt for å lage applikasjonen

```bash
gradle init --type kotlin-application --dsl kotlin --java-version 21 --test-framework junit-jupiter --package com.example
```
