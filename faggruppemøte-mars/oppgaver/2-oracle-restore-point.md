# Oppgave 2: Oracle Restore Point

Et restore point er et navngitt tidspunkt i Oracle som databasen kan spoles tilbake til.
Det lagrer hva som har endret seg siden restore point ble opprettet, og er avhengig av at
den underliggende databasen er intakt.

## Start databasen

```bash
cd oracle && docker compose up -d --wait
```

## Koble til

Via `sqlplus` i containeren:

```bash
docker compose exec oracle sqlplus demo_user/password@FREEPDB1
```

Eller bruk foretrukket verktøy (DataGrip, DBeaver, SQL Developer) mot `localhost:1521/FREEPDB1`.

## Aktiver ARCHIVELOG-modus

Guaranteed restore points krever at databasen kjører i ARCHIVELOG-modus.
Koble til som `sysdba` fra containeren:

```bash
docker compose exec oracle sqlplus / as sysdba
```

Sett opp Fast Recovery Area og aktiver ARCHIVELOG-modus:

```sql
-- Konfigurer Fast Recovery Area (montert til oracle/fast_recovery_area/ på host)
ALTER SYSTEM SET db_recovery_file_dest_size = 10G SCOPE=BOTH;
ALTER SYSTEM SET db_recovery_file_dest = '/opt/oracle/fast_recovery_area' SCOPE=BOTH;

-- Aktiver ARCHIVELOG-modus (krever restart av databasen)
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;
```

> Databasen starter i NOARCHIVELOG-modus. Etter `SHUTDOWN IMMEDIATE` og `STARTUP MOUNT`
> er du tilbake i CDB-kontekst som `sysdba` — dette er nødvendig for å opprette restore point.

Sjekk at ARCHIVELOG er aktivert:

```sql
SELECT log_mode FROM v$database;
```

## Opprett restore point

Guaranteed restore points opprettes på CDB-nivå. Kjør dette som `sysdba` (samme sesjon som over):

```sql
CREATE RESTORE POINT before_demo GUARANTEE FLASHBACK DATABASE;
```

`GUARANTEE FLASHBACK DATABASE` betyr at Oracle garanterer at restore point aldri slettes
automatisk — Oracle vil heller stoppe arkiveringen enn å slette det.

Verifiser at restore point ble opprettet:

```sql
SELECT name, guarantee_flashback_database, time
FROM v$restore_point;
```

## Gjør en endring i databasen

Koble til som `demo_user` og slett noen rader:

```bash
docker compose exec oracle sqlplus demo_user/password@FREEPDB1
```

```sql
DELETE FROM orders WHERE id IN (1, 2, 3);
COMMIT;

SELECT COUNT(*) AS antall_ordrer FROM orders;
```

Sjekk at filer har dukket opp i `oracle/fast_recovery_area/` på host-maskinen — Oracle
skriver hva som har endret seg siden restore point ble opprettet.

## Gå tilbake til restore point

Flashback Database krever at PDB-en er i mount-modus.
Koble til som `sysdba` fra containeren:

```bash
docker compose exec oracle sqlplus / as sysdba
```

```sql
ALTER SESSION SET CONTAINER = FREEPDB1;
ALTER PLUGGABLE DATABASE FREEPDB1 CLOSE;

FLASHBACK PLUGGABLE DATABASE FREEPDB1
  TO RESTORE POINT before_demo;

ALTER PLUGGABLE DATABASE FREEPDB1 OPEN RESETLOGS;
```

## Verifiser

Koble til igjen som `demo_user` og sjekk at radene er tilbake:

```sql
SELECT COUNT(*) AS antall_ordrer FROM orders;
```
