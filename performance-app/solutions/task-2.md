# Task 2: Bli kjent med oppsettet del 2

Denne spørringen er rask fordi `seller_inventory`-tabellen har en `UNIQUE (product_id, seller_id)` constraint, og PostgreSQL lager automatisk en b-tree index.

## Execution plan

```
Index Scan using seller_inventory_product_id_seller_id_key on public.seller_inventory  (cost=0.43..8.45 rows=1 width=4)
  Output: quantity
  Index Cond: ((seller_inventory.product_id = $2) AND (seller_inventory.seller_id = $1))
Planning:
  Buffers: shared hit=82 read=1 dirtied=1
```

## Test results

- Rounds: 10000
- Time: 3.55s
- Mean query time: 349.36 μs
