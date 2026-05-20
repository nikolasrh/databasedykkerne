---
marp: true
theme: default
paginate: true
---

# Databaser i 2026

## Faggruppemøte — April

---

# Agenda

1. OLTP vs. OLAP
2. Rad-basert vs. kolonne-basert lagring
3. Distribuerte databaser
4. Gruppearbeid: Utforsk en database
5. Diskusjon: Når bruker vi hva?

---

# OLTP — Online Transaction Processing

- Mange korte, samtidige transaksjoner
- INSERT, UPDATE, DELETE
- Lav svartid per operasjon

---

# OLAP — Online Analytical Processing

- Få, men tunge spørringer over store datamengder
- Aggregeringer, GROUP BY, JOIN over millioner av rader
- Lesing dominerer — sjelden skriving

---

# Rad-basert lagring

```
| id | navn    | alder | by      |
|----|---------|-------|---------|
| 1  | Ola     | 32    | Oslo    |
| 2  | Kari    | 28    | Bergen  |
```

- Lagres rad for rad på disk
- Rask å hente **hele rader**
- Passer OLTP: hent én kunde, oppdater én ordre

---

# Kolonne-basert lagring

```
id:    [1, 2, 3, 4, 5, ...]
alder: [32, 28, 45, 22, 37, ...]
by:    ["Oslo", "Bergen", "Oslo", ...]
```

- Lagres kolonne for kolonne
- Rask å lese **én kolonne** over mange rader
- Passer OLAP: `SELECT AVG(alder) FROM brukere`
- Komprimerer bedre (like verdier samlet)

---

# Oppsummering: OLTP vs. OLAP

|             | OLTP                 | OLAP                 |
| ----------- | -------------------- | -------------------- |
| Mønster     | Mange små spørringer | Få store spørringer  |
| Operasjoner | CRUD                 | Aggregering, analyse |
| Lagring     | Rad-basert           | Kolonne-basert       |
| Eksempler   | PostgreSQL, MSSQL    | ClickHouse, DuckDB   |

---

# Distribuerte databaser

Hvorfor distribuere?

- **Tilgjengelighet** — overlev at noder dør
- **Skalering** — mer data enn én maskin kan holde
- **Geografisk nærhet** — lavere svartid for brukere

---

# CAP-teoremet

Du kan bare velge **to av tre**:

- **C**onsistency — alle ser samme data
- **A**vailability — alle får svar
- **P**artition tolerance — tåler nettverksbrudd

**P** er gitt
Valget er mellom **C** og **A**

---

# Replikering

**Strong consistency (CP)**

- Alle noder ser samme data til enhver tid
- Krever koordinering → høyere svartid

**Eventual consistency (AP)**

- Noder kan midlertidig ha ulike svar
- Raskere skriving, høyere tilgjengelighet

---

# Databasekategorier

Se fullstendig oversikt: [db-engines.com/en/ranking](https://db-engines.com/en/ranking)

| Kategori           | Optimalisert for | Eksempler                 |
| ------------------ | ---------------- | ------------------------- |
| Relasjonell (OLTP) | Transaksjoner    | PostgreSQL, CockroachDB   |
| Kolonne (OLAP)     | Analyse          | ClickHouse, DuckDB        |
| Key-value / Cache  | Rask tilgang     | Valkey, Dragonfly         |
| Tidsserie          | Tidsbasert data  | TimescaleDB, QuestDB      |
| Søkemotor          | Fulltekstsøk     | Elasticsearch, OpenSearch |
| Graf               | Relasjoner       | Neo4j                     |
| Vektor             | Likhetssøk       | Qdrant, pgvector          |

---

# Gruppearbeid

Velg en database. Bruk ~1 time på å:

1. Forstå hva den er laget for
2. Prøv den ut og test funksjonaliteten
3. Lag en kort presentasjon (5-10 min) for resten


- Hvilket spørrespråk?
- Hvordan indekseres data?
- Historikk, lisens osv.

---

# Diskusjon etterpå

- Hvilke bruksområder dekkes av hver database?
- Har du noen gode use-caser på **ditt** prosjekt?

<!-- ---

# Databasevalg for gruppearbeid

Se neste slides for detaljer om hvert valg →

---

# 1. Elasticsearch / OpenSearch — Søkemotor

**Spørsmål:** Hvorfor løser disse full text search bra?

Nøkkelkonsepter:

- **Invertert indeks** — som stikkordregister: ord → dokumenter
- **Tokenisering** — tekst brytes ned, normaliseres, stemmes
- **BM25-scoring** — rangerer treff etter relevans

Postgres har: `tsvector/tsquery`, `pg_trgm`, `pg_textsearch` (BM25)

---

# 2. Vektordatabase — Qdrant (eller Chroma)

**Spørsmål:** Hva kan en vektordatabase brukes til?
Hvilke operasjoner gjøres vanligvis på vektorer?

Bruksområder: RAG, semantisk søk, anbefalinger, bildesøk
Operasjoner: cosine similarity, euklidsk avstand, dot product
Indeksering: HNSW (graf-basert), IVF (klynge-basert)

Postgres har: `pgvector` (bra opp til ~1M vektorer)

---

# 3. TimescaleDB / QuestDB — Tidsserie

**Spørsmål:** Hvorfor er disse bedre på tidsseriedata?

- Automatisk tidsbasert partisjonering
- Hopper over irrelevante tidsperioder
- Spesialisert kompresjon (90–98%)
- Kontinuerlige aggregater (forhåndsberegning)

Postgres har: `timescaledb`-utvidelsen (det _er_ PostgreSQL)

---

# 4. Neo4j — Grafdatabase

**Spørsmål:** Hvilke type spørringer er bedre/enklere
mot en graf-database?

- Korteste vei, venn-av-venn, mønstergjenkjenning
- SQL krever rekursive CTE-er og mange JOINs
- Cypher: `(alice)-[:VENNER*1..3]-(venn)` — én linje!
- Index-free adjacency: O(1) per hopp

_For de som ikke var med da vi gikk igjennom Neo4j sist_

---

# 5. DuckDB — Embedded OLAP

**Spørsmål:** Når er det en fordel å bruke embedded?
Forklar hvorfor DuckDB ofte brukes med Parquet.
Gjelder CAP-teoremet for DuckDB?

- **Embedded** = ingen server, kjører i prosessen din (som SQLite)
- Fordel: null infrastruktur, notebooks, CI-pipelines
- **Parquet** = kolonne-format på disk, komprimert, med skjema
- DuckDB leser Parquet effektivt: predicate pushdown, column pruning

---

# 6. ClickHouse — Distribuert OLAP

**Spørsmål:** Når gir distribuert mening? CAP-valg?

- **AP** — tilgjengelighet prioritert, eventuell konsistens
- ReplicatedMergeTree + ClickHouse Keeper
- Sharding: data fordeles over noder etter shard-nøkkel
- Bruksområde: real-time analytics på enorme datamengder

---

# 7. CockroachDB — Distribuert OLTP

**Spørsmål:** Når gir distribuert mening? CAP-valg?

- **CP** — sterk konsistens via Raft-protokollen
- Automatisk sharding og rebalansering
- Geo-partisjonering: data kan bo nær brukeren
- PostgreSQL-kompatibel (wire protocol)

---

# 8. Valkey / Dragonfly — Key-value / Cache

**Spørsmål:** Forklar forskjellen fra Redis.
Hva finnes utover key/value storage?

- **Valkey**: Linux Foundation-fork, BSD-lisens, lik Redis
- **Dragonfly**: Bygget fra bunnen, multi-threaded, 25x throughput
- Funksjonalitet: pub/sub, streams, sorted sets, geospatial,
  HyperLogLog, Lua-skripting, bloom filters

---

# Diskusjon etterpå

- Hvilke bruksområder dekkes av hver database?
- Er det overlapp?
- Har du noen gode use-caser på **ditt** prosjekt?
- Hvilke av disse har Postgres-utvidelser som dekker behovet? -->
