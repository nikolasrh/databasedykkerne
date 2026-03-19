# Oppgave 3: Backup og restore — MSSQL

Ta en backup av databasen, legg til nye data, og restore tilbake til backup-tidspunktet.

## Start databasen

```bash
cd mssql && docker compose up -d --wait
```

## Koble til

```bash
docker compose exec mssql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P Password123! -C
```

Eller bruk foretrukket verktøy mot `localhost:1433`.

## Ta backup

```sql
USE demo_db
GO

SELECT COUNT(*) AS antall_ordrer FROM orders
GO

BACKUP DATABASE demo_db TO DISK = '/var/opt/mssql/backup/demo_db.bak'
GO
```

## Legg til nye data

```sql
INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 2, 99)
GO

SELECT COUNT(*) AS antall_ordrer FROM orders  -- én mer enn før
GO
```

## Restore fra backup

```sql
USE master
GO

ALTER DATABASE demo_db SET SINGLE_USER WITH ROLLBACK IMMEDIATE

RESTORE DATABASE demo_db
  FROM DISK = '/var/opt/mssql/backup/demo_db.bak'
  WITH REPLACE
GO

ALTER DATABASE demo_db SET MULTI_USER
GO
```

## Verifiser

```sql
USE demo_db
GO

SELECT COUNT(*) AS antall_ordrer FROM orders  -- tilbake til original antall
GO
```
