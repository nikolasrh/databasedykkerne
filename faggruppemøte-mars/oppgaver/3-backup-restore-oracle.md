# Oppgave 3: Backup og restore — Oracle

Ta en logisk backup av skjemaet med Data Pump, legg til nye data, og importer tilbake til backup-tilstanden.

## Start databasen

```bash
cd oracle && docker compose up -d --wait
```

## Koble til

```bash
docker compose exec oracle sqlplus demo_user/password@FREEPDB1
```

Eller bruk foretrukket verktøy mot `localhost:1521/FREEPDB1`.

## Ta backup

```bash
docker compose exec oracle expdp demo_user/password@FREEPDB1 \
  schemas=demo_user \
  directory=backup_dir \
  dumpfile=demo_backup.dmp \
  logfile=demo_backup_exp.log
```

Backup-filen dukker nå opp i `oracle/backup/` på host-maskinen.

## Legg til nye data

```bash
docker compose exec oracle sqlplus demo_user/password@FREEPDB1
```

```sql
INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 2, 99);
COMMIT;

SELECT COUNT(*) AS antall_ordrer FROM orders;  -- én mer enn før
```

## Restore fra backup

```bash
docker compose exec oracle impdp demo_user/password@FREEPDB1 \
  schemas=demo_user \
  directory=backup_dir \
  dumpfile=demo_backup.dmp \
  logfile=demo_backup_imp.log \
  table_exists_action=replace
```

> `ORA-31684: Object type USER already exists` er en ufarlig advarsel og kan ignoreres.

## Verifiser

```bash
docker compose exec oracle sqlplus demo_user/password@FREEPDB1
```

```sql
SELECT COUNT(*) AS antall_ordrer FROM orders;  -- tilbake til original antall
```
