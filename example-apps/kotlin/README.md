# Kotlin

Her står man fritt til å teste det man måtte ønske.

Forslag:
- Reactive streaming fra databasen med RD2BC
- Bruk Exposed som ORM (object-relational mapping) og for å lage og kjøre migreringer

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
