# Java Spring JPA

## Oppgaver

- Uten å ha en database kjørende – hvorfor feiler alle testene selv om de egentlig ikke skal kjøre?
- Velg database i `application.yml` og start den
- Implementer noen tester i `UserRepository`
- Utvid `UserEntity` med `YearOfBirth` og utvid `UserRepository` med en metode som finner alle over 30 år
- Sett `spring.jpa.hibernate.ddl-auto: off` – hva skjer?
- Legg til et Liquibase eller Flyway for å kjøre databasemigreringer
- Hva for arbeidsflyt eller verktøy kunne du tenkt deg å bruke for å enkelt lagre migreringer?

## Kommandoer

Kjør applikasjon:

```bash
./gradlew run
```

Kjør tester

```bash
./gradlew test --info
```

## Kommandoer brukt for å lage applikasjonen

```bash
gradle init --type java-application --dsl groovy --test-framework junit-jupiter --overwrite
```
