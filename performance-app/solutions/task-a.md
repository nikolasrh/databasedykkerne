# Task A: Paginer gjennom seller reviews sortert på review_date

Uten indeks må PostgreSQL skanne hele `seller_reviews`-tabellen og sortere den hver gang.

Med riktig indeks slipper man å sortere, men må regne seg fram til ritkig offset. Dette går fortsatt raskt siden man bare "hopper" i indeksen.

## Før index

### Execution plan:
```
Limit  (cost=171159.43..171276.11 rows=1000 width=16)
  Output: id, seller_id, rating, review_date
  ->  Gather Merge  (cost=146852.22..389924.82 rows=2083334 width=16)
        Output: id, seller_id, rating, review_date
        Workers Planned: 2
        ->  Sort  (cost=145852.19..148456.36 rows=1041667 width=16)
              Output: id, seller_id, rating, review_date
              Sort Key: sr.review_date, sr.id
              ->  Parallel Seq Scan on public.seller_reviews sr  (cost=0.00..23930.67 rows=1041667 width=16)
                    Output: id, seller_id, rating, review_date
```


### Test results

- Rounds: 16 (før timeout)
- Mean query time: 607.23 ms

PostgreSQL henter alt parallell og må sortere 2.5M rader hver spørring.
Spørringen er så treg at den når 10s timeout etter bare 16 runder.

## Etter index

En indeks på `(review_date, id)` gjør spørringen rask fordi:
1. Radene er allerede sortert i riktig rekkefølge
2. PostgreSQL kan bruke Index Scan i stedet for Seq Scan + Sort
3. Offset er fortsatt relativt effektivt siden vi bare hopper over rader i indeksen

migrations/008_add_seller_reviews_date_index.up.sql
```sql
CREATE INDEX seller_reviews_review_date_id_idx ON seller_reviews (review_date, id);
```

migrations/008_add_seller_reviews_date_index.down.sql
```sql
DROP INDEX IF EXISTS seller_reviews_review_date_id_idx;
```

### Execution plan

```
Limit  (cost=11899.18..11946.77 rows=1000 width=16)
  Output: id, seller_id, rating, review_date
  ->  Index Scan using seller_reviews_review_date_id_idx on public.seller_reviews sr  (cost=0.43..118987.91 rows=2500000 width=16)
        Output: id, seller_id, rating, review_date
```

### Test results

- Rounds: 100
- Time: 2.33s
- Mean query time: 23.04 ms

**Ytelsesforbedring:** ~26x raskere (607.23 ms → 23.04 ms)

Med indeksen kan vi fullføre 100 pages på ~2.3 sekunder.
PostgreSQL bruker nå Index Scan og trenger ikke å sortere noe.

## Hvorfor sortere på ID etter dato?

review_date er ikke unik, så mange reviews kan ha samme dato.
Uten ID i sorteringen er rekkefølgen av reviews med samme dato udeterministisk.
Dette kan føre til at samme review vises på flere pages eller hoppes over.
