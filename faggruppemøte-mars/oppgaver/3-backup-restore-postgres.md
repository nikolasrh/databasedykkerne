# Oppgave 3: Backup og restore — PostgreSQL

Ta en logisk backup av databasen med `pg_dump`, legg til nye data, og restore tilbake til backup-tilstanden.

## Start databasen

```bash
cd postgres && docker compose up -d --wait
```

## Koble til

```bash
docker compose exec postgres psql -U postgres -d demo_db
```

Eller bruk foretrukket verktøy mot `localhost:5432`.

## Ta backup

```bash
docker compose exec postgres pg_dump \
  -U postgres \
  -d demo_db \
  --format=custom \
  -f /backup/demo_backup.dump
```

## Legg til nye data

```bash
docker compose exec postgres psql -U postgres -d demo_db \
  -c "INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 2, 99)"

docker compose exec postgres psql -U postgres -d demo_db \
  -c "SELECT COUNT(*) AS antall_ordrer FROM orders"
```

## Restore fra backup

```bash
docker compose exec postgres pg_restore \
  -U postgres \
  -d demo_db \
  --clean \
  --if-exists \
  /backup/demo_backup.dump
```

## Verifiser

```bash
docker compose exec postgres psql -U postgres -d demo_db \
  -c "SELECT COUNT(*) AS antall_ordrer FROM orders"
```
