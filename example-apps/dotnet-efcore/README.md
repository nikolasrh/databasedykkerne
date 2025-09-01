# Entity Framework Core (EF Core)

Denne solution-en består av `EFCoreApp` og tilhørende testprosjekt `EFCoreApp.Tests`.
`EFCoreApp`. `EFCoreApp` er bare en konsoll-applikasjon, men inneholder `PersonEntity` og `PersonContext` som kan utvides for å lære mer om EF Core.

## Oppgaver

- Finn ut hvordan databasemigreringer lages og kjøres
- Legg til en test som lagrer en ny `PersonEntity` i en in-memory database
- Legg til en tilsvarende test som som bruker en database kjørende med Docker
- Legg til `YearOfBirth` på `PersonEntity`
- Lag en databaseindeks på det nye feltet
- Legg til en relasjon til noe annet, og sett opp en fremmednøkkel
- Legg til en list på `PersonEntity` og lagre verdien som JSON i databasen

For oppgave,  oppdater tester, lag nye migreringer, og se hvordan det ser ut i databasen.

## Kommandoer

Kjør applikasjon:

```
dotnet run --project EFCoreApp
```

Kjør med hot reload:

```
dotnet watch run --project EFCoreApp
```

Kjør alle tester i solution:

```
dotnet test
```

Kjør tester når filer endres:

```
cd EFCoreApp.Tests
dotnet watch test
```

## Kommandoer brukt for å lage applikasjonen

Lage solution og projects:

```
dotnet new gitignore
dotnet new editorconfig
dotnet new sln -n EFCoreApp
dotnet new console -n EFCoreApp
dotnet new xunit -n EFCoreApp.Tests
dotnet sln add EFCoreApp
dotnet sln add EFCoreApp.Tests
```

Legge til pakker og prosjektavhengigheter:

```
dotnet add EFCoreApp package Microsoft.EntityFrameworkCore.Design
dotnet add EFCoreApp package Microsoft.EntityFrameworkCore.SqlServer
dotnet add EFCoreApp package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add EFCoreApp package Oracle.EntityFrameworkCore
dotnet add EFCoreApp.Tests reference EFCoreApp
```

Installere kommandolinjeverktøy for å lage databasemigreringer:

```
dotnet tool install --global dotnet-ef
```

[Les mer om databasemigreringer her.](https://learn.microsoft.com/en-us/ef/core/get-started/overview/first-app?tabs=netcore-cli#create-the-database)
