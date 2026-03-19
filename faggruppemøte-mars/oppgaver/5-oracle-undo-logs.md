# Oppgave 5: Rollback med Oracle undo logs

Oracle lagrer undo-data i en begrenset periode. Det gjør det mulig å lese data slik de
så ut tidligere — uten backup. I motsetning til restore points (oppgave 2) krever ikke
dette ARCHIVELOG-modus, men det fungerer bare så lenge undo-dataene ikke er blitt
overskrevet.

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

## Sjekk hvor lenge undo-data bevares

Oracle styrer dette med `UNDO_RETENTION` (i sekunder). Koble til som `sysdba` for å se
gjeldende verdi:

```bash
docker compose exec oracle sqlplus / as sysdba
```

```sql
SHOW PARAMETER undo_retention;
```

Standardverdien er 900 sekunder (15 minutter). Det betyr at Oracle forsøker å beholde
undo-data i minst 15 minutter etter en commit — men det er ingen garanti hvis
undo-tablespace er fullt.

Du kan øke verdien om du vil ha lengre vindu:

```sql
ALTER SYSTEM SET undo_retention = 3600;
```

## Gjør en feil-endring

Koble til som `demo_user` og noter tidspunktet før du gjør endringen:

```sql
SELECT SYSTIMESTAMP FROM dual;
```

Slett noen rader og commit:

```sql
DELETE FROM orders WHERE id IN (1, 2, 3);
COMMIT;

SELECT COUNT(*) AS antall_ordrer FROM orders;
```

## Flashback Query

Med `AS OF TIMESTAMP` kan du lese tabellen slik den så ut på et tidligere tidspunkt.
Erstatt tidspunktet under med verdien du noterte over:

```sql
SELECT COUNT(*) AS antall_ordrer
FROM orders AS OF TIMESTAMP
  TO_TIMESTAMP('2026-03-19 10:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

De slettede radene er synlige igjen — Oracle henter dem fra undo-segmentene.

Du kan også bruke et relativt tidspunkt:

```sql
SELECT *
FROM orders AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '5' MINUTE);
```

## Gjenopprett rad for rad

Bruk `INSERT INTO ... SELECT ... AS OF TIMESTAMP` for å hente tilbake bare de radene
som ble slettet:

```sql
INSERT INTO orders
SELECT * FROM orders AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '5' MINUTE)
WHERE id IN (1, 2, 3);

COMMIT;

SELECT COUNT(*) AS antall_ordrer FROM orders;
```

## Flashback Table

Et enklere alternativ er `FLASHBACK TABLE`, som ruller tilbake hele tabellen til et
gitt tidspunkt i ett enkelt statement. ROW MOVEMENT må være aktivert på tabellen
(det er det allerede i dette oppsettet):

```sql
FLASHBACK TABLE orders TO TIMESTAMP (SYSTIMESTAMP - INTERVAL '5' MINUTE);

SELECT COUNT(*) AS antall_ordrer FROM orders;
```

> Merk: Hvis du allerede gjenopprettet rad for rad i steget over, slett radene på nytt
> og commit før du prøver `FLASHBACK TABLE`.

## Bonus: Se endringshistorikken til en rad

`VERSIONS BETWEEN TIMESTAMP` viser alle versjoner av radene i et tidsintervall —
nyttig for å finne ut nøyaktig når noe gikk galt:

```sql
SELECT id, quantity, versions_starttime, versions_endtime, versions_operation
FROM orders
VERSIONS BETWEEN TIMESTAMP (SYSTIMESTAMP - INTERVAL '10' MINUTE) AND SYSTIMESTAMP
WHERE id IN (1, 2, 3)
ORDER BY id, versions_starttime;
```

- `versions_operation`: `I` = insert, `U` = update, `D` = delete
- `versions_starttime`: når denne versjonen av raden ble gjeldende
- `versions_endtime`: når den ble erstattet av neste versjon (NULL = gjeldende versjon)
