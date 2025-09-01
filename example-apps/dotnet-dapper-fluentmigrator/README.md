# FluentMigrator og Dapper

Denne solution-en består av `DapperApp` og tilhørende testprosjekt `DapperApp.Tests`.
`DapperApp` er bare en konsoll-applikasjon, men kjører FluentMigrator ved oppstart, og bruker Dapper for å gjøre SQL-spørringer.

## Oppgaver

- Velg en database, og slå på testen for å koble til
- Sett opp FluentMigrator og lag en tabell med `fluentmigrator_user`
- Ta en titt i `init.sql` – hva er fordelen med en dedikert bruker for FluentMigrator?
- Reset databasen og kjør migreringen via `dotnet fm`
- Skriv eksempel-data via MCP-serveren
- Lag en test som resetter databasen og kjører migreringene
- Lag en test som skriver og leser data med Dapper

For hver oppgave, oppdater tester, lag nye migreringer, eller se hvordan det ser ut i databasen.

## Kommandoer

Kjør applikasjon:

```
dotnet run --project DapperApp
```

Kjør med hot reload:

```
dotnet watch run --project DapperApp
```

Kjør alle tester i solution:

```
dotnet test
```

Kjør tester når filer endres:

```
cd DapperApp.Tests
dotnet watch test
```

## Kommandoer brukt for å lage applikasjonen

Lage solution og projects:

```
dotnet new gitignore
dotnet new editorconfig
dotnet new sln -n DapperApp
dotnet new console -n DapperApp
dotnet new xunit -n DapperApp.Tests
dotnet sln add DapperApp
dotnet sln add DapperApp.Tests
```

Legge til pakker og prosjektavhengigheter:

```
dotnet add DapperApp package Dapper
dotnet add DapperApp package Npgsql
dotnet add DapperApp package Oracle.ManagedDataAccess.Core
dotnet add DapperApp package FluentMigrator
dotnet add DapperApp package FluentMigrator.Runner.SqlServer
dotnet add DapperApp package FluentMigrator.Runner.Oracle
dotnet add DapperApp package FluentMigrator.Runner.Postgres
dotnet add DapperApp package FluentMigrator.Extensions.SqlServer
dotnet add DapperApp package FluentMigrator.Extensions.Oracle
dotnet add DapperApp package FluentMigrator.Extensions.Postgres
dotnet add DapperApp.Tests reference DapperApp
```

Installere kommandolinjeverktøy for databasemigrering:

```
dotnet tool install --global FluentMigrator.DotNet.Cli
```
