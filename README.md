This is a database practice readme file which focuses on postgres. 

This repository is a 7 day plan created to actually learn the fundamentals from first principles instead of tutorials.

Note to remeber:
The goal is not to learn individual technologies. Instead encounter problems while building something moving towards solution using first principles.

## 7-Day Plan

| Day | Build | Stack | Focus |
| --- | --- | --- | --- |
| 1 | Concurrent Job Queue | PostgreSQL, Python, FastAPI, Psycopg | SQL, transactions, constraints, row locking, concurrency |
| 2 | Cached API | PostgreSQL, Redis, Python, FastAPI | caching, TTLs, invalidation, consistency, cache stampedes |
| 3 | Event Streaming Pipeline | Kafka/Redpanda, Python | topics, partitions, offsets, consumer groups, delivery semantics |
| 4 | Batch Processing Engine | Python, PostgreSQL | chunking, checkpoints, bulk operations, idempotency |
| 5 | Zero-Downtime Migration | PostgreSQL, Python | migrations, backfills, compatibility, schema evolution |
| 6 | Reliable Event System | PostgreSQL, Kafka/Redpanda | outbox pattern, retries, DLQs, reliable event delivery |
| 7 | Mini Feature Store | PostgreSQL, Redis, Kafka/Redpanda, Python | online/offline data, streaming + batch, point-in-time correctness |

## Day 1 — Concurrent Job Queue

Build a PostgreSQL-backed job queue and run multiple workers concurrently.

Start with a naive worker implementation and observe duplicate processing when
multiple workers attempt to claim the same pending job.

Use psycopg instead of SQLAlchemy Core or ORM

Explore:

- schema design and database constraints
- raw SQL with Psycopg
- transactions and transaction boundaries
- `COMMIT` and `ROLLBACK`
- row-level locking with `SELECT ... FOR UPDATE`
- blocking vs `SKIP LOCKED`
- concurrent workers without duplicate processing
- PostgreSQL identity/sequence behavior

Conceptually explore reliability problems such as retries, backoff, worker crashes, leases, heartbeats, dead-letter queues, and idempotency. You can also try to implement small snippets for these.

**Implementation:** [`jobqueue/`](jobqueue/)
