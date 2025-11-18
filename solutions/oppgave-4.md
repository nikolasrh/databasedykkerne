# Oppgave 4: Søk på dato

Uten indeks må PostgreSQL skanne hele `products`-tabellen for å finne radene som matcher datoområdet.

En indeks på `released_date` lar databasen hoppe direkte til riktig dato. Indeksen holder datoene sortert, så PostgreSQL kan fortsette helt til den finner sluttdatoen.

migrations/004_add_products_released_date_index.up.sql
```sql
CREATE INDEX products_released_date_idx ON products (released_date);
```

migrations/004_add_products_released_date_index.down.sql
```sql
DROP INDEX IF EXISTS products_released_date_idx;
```

## Execution plan

```
Bitmap Heap Scan on public.products  (cost=142.93..11330.12 rows=10000 width=16)
  Output: id, category, released_date, discontinued_date
  Recheck Cond: ((products.released_date >= $1) AND (products.released_date <= $2))
  ->  Bitmap Index Scan on products_released_date_idx  (cost=0.00..140.43 rows=10000 width=0)
        Index Cond: ((products.released_date >= $1) AND (products.released_date <= $2))
Planning:
  Buffers: shared hit=85 read=4
```

## Test results

- Rounds: 500
- Time: 3.97s
- Mean query time: 7.42 ms
