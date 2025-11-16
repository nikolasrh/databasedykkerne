# Task C: Keyset pagination for seller reviews med minimum rating

## Hvordan fungerer det?

I stedet for å si "hopp over de første N radene", sender vi med verdiene fra siste rad på forrige page:

**Offset pagination (Task B):**
```sql
WHERE rating >= 5
ORDER BY review_date, id
LIMIT 1000
OFFSET 10000
```

**Keyset pagination (Task C):**
```sql
WHERE rating >= 5
  AND (review_date, id) > (last_review_date, last_id)
ORDER BY review_date, id
LIMIT 1000
```

## Hvorfor er dette raskere?

### Med offset (Task B):
- Page 1: Scann ~5000 rader
- Page 10: Scann ~50000 rader
- Page 100: Scann ~500000 rader

PostgreSQL må telle gjennom alle matchende rader fra starten hver gang.

### Med keyset (Task C):
- Page 1: Scann ~5000 rader
- Page 10: Scann ~5000 rader
- Page 100: Scann ~5000 rader

PostgreSQL starter der forrige page sluttet, og kan hoppe dit direkte ved å bruke indeksen.

Derfor fungerer samme indeks som fra Task A og B:
```sql
CREATE INDEX seller_reviews_review_date_id_idx ON seller_reviews (review_date, id);
```

### Execution plan

```
Limit  (cost=0.43..287.95 rows=1000 width=16)
  Output: id, seller_id, rating, review_date
  ->  Index Scan using seller_reviews_review_date_id_idx on public.seller_reviews sr  (cost=0.43..79866.46 rows=277778 width=16)
        Output: id, seller_id, rating, review_date
        Index Cond: (ROW(sr.review_date, sr.id) > ROW($2, $3))
        Filter: (sr.rating >= $1)
```

PostgreSQL hopper direkte til riktig sted i indeksen ved å bruke `(review_date, id) > (...)`.

## Test results

Med filtrering på 5 rating:
- Rounds: 1000
- Mean query time: 4,67 ms

Uten filtrering på rating:
- Rounds: 1000
- Mean query time: 1,37 ms

Som forventet er det raskere å hente ut uten filter.

## Fordeler og ulemper

### Fordeler:
- Konstant ytelse uavhengig av page-nummer

### Ulemper:
- Kan ikke hoppe direkte til en vilkårlig page (f.eks. "gå til page 47")
- Av samme grunn er det vanskelig å gå en side tilbake
