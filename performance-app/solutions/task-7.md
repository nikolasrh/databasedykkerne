# Task 7: Finn topp 10 selgere i Trondheim

Sammenlignet med forrige oppgave filtrerer vi nå på `location` og `HAVING COUNT(sr.id) >= 5`. Da vil en index betydelig redusere antall rader vi trenger å aggregere.

migrations/007_add_sellers_location_index.up.sql
```sql
CREATE INDEX sellers_location_id_idx ON sellers (location, id);
```

migrations/007_add_sellers_location_index.down.sql
```sql
DROP INDEX IF EXISTS sellers_location_id_idx;
```

`sellers_location_id_idx` gjør det raskt å finne alle selgere i en spesifikk lokasjon.
Legg merke til at index-en fra forrige oppgave, `seller_reviews_seller_id_idx`, ikke blir brukt.
Optimizeren kjører i stedet `Parallel Seq Scan on public.seller_reviews sr`.

## Execution plan

```
Limit  (cost=27934.83..27934.85 rows=8 width=48)
  Output: s.id, s.location, (avg(sr.rating)), (count(sr.id))
  ->  Sort  (cost=27934.83..27935.03 rows=78 width=48)
        Output: s.id, s.location, (avg(sr.rating)), (count(sr.id))
        Sort Key: (avg(sr.rating)) DESC
        ->  Finalize GroupAggregate  (cost=27871.02..27932.38 rows=78 width=48)
              Output: s.id, s.location, avg(sr.rating), count(sr.id)
              Group Key: s.id
              Filter: (count(sr.id) >= $2)
              ->  Gather Merge  (cost=27871.02..27925.39 rows=466 width=48)
                    Output: s.id, s.location, (PARTIAL avg(sr.rating)), (PARTIAL count(sr.id))
                    Workers Planned: 2
                    ->  Sort  (cost=26871.00..26871.58 rows=233 width=48)
                          Output: s.id, s.location, (PARTIAL avg(sr.rating)), (PARTIAL count(sr.id))
                          Sort Key: s.id
                          ->  Partial HashAggregate  (cost=26859.51..26861.84 rows=233 width=48)
                                Output: s.id, s.location, PARTIAL avg(sr.rating), PARTIAL count(sr.id)
                                Group Key: s.id
                                ->  Hash Join  (cost=11.28..26677.47 rows=24271 width=16)
                                      Output: s.id, s.location, sr.rating, sr.id
                                      Inner Unique: true
                                      Hash Cond: (sr.seller_id = s.id)
                                      ->  Parallel Seq Scan on public.seller_reviews sr  (cost=0.00..23930.67 rows=1041667 width=12)
                                            Output: sr.id, sr.seller_id, sr.rating, sr.review_date
                                      ->  Hash  (cost=8.36..8.36 rows=233 width=8)
                                            Output: s.id, s.location
                                            ->  Index Only Scan using sellers_location_id_idx on public.sellers s  (cost=0.29..8.36 rows=233 width=8)
                                                  Output: s.id, s.location
                                                  Index Cond: (s.location = $1)
Planning:
  Buffers: shared hit=178 read=11 dirtied=1
```

## Test results

- Rounds: 10
- Time: 5.93s
- Mean query time: 569.64 ms

## Endre random_page_cost fra 4 til 1.1

Innstillingen `random_page_cost` forteller optimizeren hvor dyrt random IO er. En verdi på 4 er mest brukt for HDD, mens 1.1 er bedre for SSD.

Etter denne endringen ser vi at optimizeren bruker Nested Loop i stedet for Hash Join.

migrations/007_add_sellers_location_index.up.sql (oppdatert)
```sql
CREATE INDEX sellers_location_id_idx ON sellers (location, id);

ALTER DATABASE postgres SET random_page_cost = 1.1;
```

migrations/007_add_sellers_location_index.down.sql (oppdatert)
```sql
ALTER DATABASE postgres SET random_page_cost = 4;

DROP INDEX IF EXISTS sellers_location_id_idx;
```

### Execution plan

```
Limit  (cost=17274.97..17274.99 rows=8 width=48)
  Output: s.id, s.location, (avg(sr.rating)), (count(sr.id))
  ->  Sort  (cost=17274.97..17275.16 rows=78 width=48)
        Output: s.id, s.location, (avg(sr.rating)), (count(sr.id))
        Sort Key: (avg(sr.rating)) DESC
        ->  GroupAggregate  (cost=0.72..17272.52 rows=78 width=48)
              Output: s.id, s.location, avg(sr.rating), count(sr.id)
              Group Key: s.id
              Filter: (count(sr.id) >= $2)
              ->  Nested Loop  (cost=0.72..16832.15 rows=58250 width=16)
                    Output: s.id, s.location, sr.rating, sr.id
                    ->  Index Only Scan using sellers_location_id_idx on public.sellers s  (cost=0.29..5.46 rows=233 width=8)
                          Output: s.location, s.id
                          Index Cond: (s.location = $1)
                    ->  Index Scan using seller_reviews_seller_id_idx on public.seller_reviews sr  (cost=0.43..69.71 rows=251 width=12)
                          Output: sr.id, sr.seller_id, sr.rating, sr.review_date
                          Index Cond: (sr.seller_id = s.id)
Planning:
  Buffers: shared hit=183
```

### Test results (med random_page_cost = 1.1)

- Rounds: 1000
- Time: 8.59s
- Mean query time: 8.53 ms

**Ytelsesforbedring:** ~67x raskere (569.64 ms → 8.53 ms)

Nå brukes begge index-ene effektivt:
1. `sellers_location_id_idx` finner raskt de 233 selgerne i Trondheim
2. For hver selger brukes `seller_reviews_seller_id_idx` til å finne deres reviews
3. Ingen scanning av alle 2.5M reviews lenger!
