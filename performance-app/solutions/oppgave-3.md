# Oppgave 3: Finn samlet inventory for en selger

Uten en indeks på `seller_id` må PostgreSQL skanne hele tabellen for å finne alle relevante rader.

Ved å legge til en indeks på `seller_id` kan databasen hoppe direkte til selgeren sine rader.

migrations/003_add_seller_inventory_index.up.sql
```sql
CREATE INDEX seller_inventory_seller_id_idx ON seller_inventory (seller_id);
```

migrations/003_add_seller_inventory_index.down.sql
```sql
DROP INDEX IF EXISTS seller_inventory_seller_id_idx;
```

En annen løsning er å endre unique constraint-en.
Fra før er rekkefølgen `UNIQUE (product_id, seller_id)`. Det hadde hjulpet for å finne alle selgere for et produkt.
Ved å snu rekkefølgen i unique constrainten, snur man også rekkefølgen i den underliggende index-en.

migrations/003_change_unique_constraint.up.sql
```sql
ALTER TABLE seller_inventory DROP CONSTRAINT seller_inventory_product_id_seller_id_key;
ALTER TABLE seller_inventory ADD CONSTRAINT seller_inventory_seller_id_product_id_key UNIQUE (seller_id, product_id);
```

migrations/003_change_unique_constraint.down.sql
```sql
ALTER TABLE seller_inventory DROP CONSTRAINT seller_inventory_seller_id_product_id_key;
ALTER TABLE seller_inventory ADD CONSTRAINT seller_inventory_product_id_seller_id_key UNIQUE (product_id, seller_id);
```

## Execution plan

```
Aggregate  (cost=52.11..52.12 rows=1 width=8)
  Output: sum(quantity)
  ->  Index Scan using seller_inventory_seller_id_idx on public.seller_inventory  (cost=0.43..48.40 rows=1484 width=4)
        Output: id, product_id, seller_id, quantity, price, last_updated
        Index Cond: (seller_inventory.seller_id = $1)
Planning:
  Buffers: shared hit=99 read=2
```

## Test results

- Rounds: 10000
- Time: 4.11s
- Mean query time: 404.65 μs
