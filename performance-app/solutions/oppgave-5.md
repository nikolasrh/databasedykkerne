# Oppgave 5: Søk på kategori og dato

Med bare en indeks på `released_date` må databasen først finne alle produkter i datoområdet, og deretter filtrere på kategori.

En sammensatt indeks på `(category, released_date)` gjør spørringen raskere fordi PostgreSQL kan bruke begge filterkritene i index-en.

migrations/005_add_products_category_date_index.up.sql
```sql
CREATE INDEX products_category_released_date_idx ON products (category, released_date);
```

migrations/005_add_products_category_date_index.down.sql
```sql
DROP INDEX IF EXISTS products_category_released_date_idx;
```

Indeksen filtrerer først på `category`, som reduserer antall rader betydelig. Innenfor hver kategori er datoene sortert, så PostgreSQL kan hoppe til riktig dato slik som i forrige oppgave.

Dette er veldig effektivt når du filtrerer på kategori, men mindre nyttig hvis du bare søker på dato uten kategori.

## Execution plan

```
Bitmap Heap Scan on public.products  (cost=33.93..5132.34 rows=2000 width=16)
  Output: id, category, released_date, discontinued_date
  Recheck Cond: ((products.category = $1) AND (products.released_date >= $2) AND (products.released_date <= $3))
  ->  Bitmap Index Scan on products_category_released_date_idx  (cost=0.00..33.43 rows=2000 width=0)
        Index Cond: ((products.category = $1) AND (products.released_date >= $2) AND (products.released_date <= $3))
Planning:
  Buffers: shared hit=112 read=3
```

## Test results

- Rounds: 500
- Time: 1.04s
- Mean query time: 1.92 ms
