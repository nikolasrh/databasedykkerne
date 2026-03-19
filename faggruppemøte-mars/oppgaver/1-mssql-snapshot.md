# Oppgave 1: MSSQL Database Snapshot

Et database snapshot er et fryst bilde av databasen på ett tidspunkt. Det lagrer hva som
har endret seg siden øyeblikksbildet ble tatt, og er avhengig av at kildedatabasen er intakt.

## Start databasen

```bash
cd mssql && docker compose up -d --wait
```

## Koble til

Via `sqlcmd` i containeren:

```bash
docker compose exec mssql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P Password123! -C
```

Eller bruk foretrukket verktøy (SSMS, DataGrip, DBeaver) mot `localhost:1433`.

## Opprett et snapshot

```sql
USE master
GO

CREATE DATABASE demo_snap ON (
  NAME = demo_db,
  FILENAME = '/var/opt/mssql/snapshot/demo_snap.ss'
) AS SNAPSHOT OF demo_db
GO
```

`.ss`-filen dukker nå opp i `mssql/snapshot/` på host-maskinen.

## Gjør en endring i kildedatabasen

```sql
USE demo_db
GO

DELETE FROM orders WHERE id IN (1, 2, 3)
GO

SELECT COUNT(*) AS antall_ordrer FROM orders
GO
```

Kildedatabasen har nå 5 ordrer. Snapshotet lagrer originale sider copy-on-write når de endres.

## Les fra snapshotet

Snapshotet er lesbart som en vanlig database:

```sql
USE demo_snap
GO

SELECT COUNT(*) AS antall_ordrer FROM orders
GO
```

De slettede radene er fortsatt her.

## Gå tilbake til snapshotet

```sql
USE master
GO

-- Kildedatabasen må ikke ha aktive tilkoblinger
ALTER DATABASE demo_db SET SINGLE_USER WITH ROLLBACK IMMEDIATE

RESTORE DATABASE demo_db FROM DATABASE_SNAPSHOT = 'demo_snap'
GO

ALTER DATABASE demo_db SET MULTI_USER
GO
```

Verifiser at de slettede radene er tilbake:

```sql
USE demo_db
GO

SELECT COUNT(*) AS antall_ordrer FROM orders
GO
```
