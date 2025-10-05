# Task 1: Bli kjent med oppsettet

Oppslag på `product_id` er raskt fordi det er primærnøkkelen.
PostgreSQL lager automatisk en b-tree index for å sikre unike verdier og ytelse.

## Execution plan

```
Index Scan using products_pkey on public.products  (cost=0.43..8.45 rows=1 width=16)
  Output: id, category, released_date, discontinued_date
  Index Cond: (products.id = $1)
Planning:
  Buffers: shared hit=70
```

## Test results

- Rounds: 10000
- Time: 3.57s
- Mean query time: 350.13 μs
