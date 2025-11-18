# Oppgave 6: Finn topp 100 selgere

Spørringen må gruppere alle rader per `seller_id`, beregne gjennomsnitt, sortere alle grupper, og hente topp 100.

En indeks på `seller_id` kan hjelpe litt med aggregeringen.
Hvis man inkluderer `rating` slipper man også table lookups på alle selgere som ikke havner i topp 100.

migrations/006_add_seller_reviews_index.up.sql
```sql
CREATE INDEX seller_reviews_seller_id_idx ON seller_reviews (seller_id) INCLUDE (rating);
```

migrations/006_add_seller_reviews_index.down.sql
```sql
DROP INDEX IF EXISTS seller_reviews_seller_id_idx;
```

Men databasen må fortsatt gå igjennom alle selgere hver gang spørringen kjøres. I planen under blir ikke index-en brukt.

Hvis denne spørringen kjøres ofte og krever lav responstid, gir det mer mening å lagre en pre-kalkulert gjennomsnittlig rating for hver selger.
Dette kan enten være en tidsbasert jobb som oppdaterer en kolonne på `sellers`-tabellen, eller et materialized view.

For å raskt finne topp 100 kan man enten sortere på rating i spørringen, eller legge til en index på materialized viewet.

migrations/006_add_seller_avg_rating_view.up.sql
```sql
CREATE MATERIALIZED VIEW seller_avg_ratings AS
SELECT seller_id, AVG(rating) as avg_rating
FROM seller_reviews
GROUP BY seller_id
ORDER BY seller_id; -- ORDER BY avg_rating instead of index

CREATE INDEX seller_avg_ratings_avg_rating_idx ON seller_avg_ratings (avg_rating DESC);
```

migrations/006_add_seller_avg_rating_view.down.sql
```sql
DROP MATERIALIZED VIEW IF EXISTS seller_avg_ratings;
```

Materialized views må oppdateres med `REFRESH MATERIALIZED VIEW`.
Alternativt kan man se på extensionen `pg_ivm` for inklementelle oppdateringer.
Andre databaser, som f.eks. Oracle, har bedre støtte for dette.

## Execution plan

```
Limit  (cost=33126.55..33129.05 rows=999 width=36)
  Output: seller_id, (avg(rating))
  ->  Sort  (cost=33126.55..33151.54 rows=9994 width=36)
        Output: seller_id, (avg(rating))
        Sort Key: (avg(seller_reviews.rating)) DESC
        ->  Finalize HashAggregate  (cost=32337.68..32462.61 rows=9994 width=36)
              Output: seller_id, avg(rating)
              Group Key: seller_reviews.seller_id
              ->  Gather  (cost=30139.00..32237.74 rows=19988 width=36)
                    Output: seller_id, (PARTIAL avg(rating))
                    Workers Planned: 2
                    ->  Partial HashAggregate  (cost=29139.00..29238.94 rows=9994 width=36)
                          Output: seller_id, PARTIAL avg(rating)
                          Group Key: seller_reviews.seller_id
                          ->  Parallel Seq Scan on public.seller_reviews  (cost=0.00..23930.67 rows=1041667 width=8)
                                Output: id, seller_id, rating, review_date
Planning:
  Buffers: shared hit=98 read=4
```

## Test results

- Rounds: 1
- Time: 2.56s
- Mean query time: 1.81 s
