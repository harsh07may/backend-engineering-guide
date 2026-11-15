# Backend Engineering Field Guide: design

Approved 2026-11-15.

## Goal
One self-contained HTML page that teaches the 14-category backend checklist through Node.js, Express 5 and TypeScript. Terse, taught not asserted, terms introduced before use.

## Stack used in examples (verified against docs, Nov 2026)
- Node.js 26 LTS, running `.ts` directly via type stripping (no enums, parameter properties or decorators; `.ts` import extensions; `import type`)
- Express 5 (async errors reach the error handler; `/*splat`; read-only `req.query`)
- TypeScript 5.8+ as checker only (`erasableSyntaxOnly`, `verbatimModuleSyntax`)
- PostgreSQL 18 via `pg` (PostgreSQL 19 GA planned 2026-11-19; re-check in session 2)
- Redis 8 via `redis` (node-redis), Zod 4

## Page
- `src/shell.html`: styles, sidebar, hash routing (one chapter visible at a time, plain `#id` hashes), topic search, "learned" toggles in localStorage, copy buttons, highlight.js from cdnjs.
- `src/sections/NN-name.html`: one file per chapter. Shorthands: fenced code blocks (```` ```lang title=… ````) and backtick inline code, both escaped by the build.
- `build.py` joins them into `index.html` and fails on duplicate ids or broken internal links.
- Sidebar parts: Foundations (1, 5, 6), Building APIs (2, 9), Data (3, 4), Scale (7, 8, 10, 11), Shipping (12, 13, 14). Unwritten chapters show a session chip; adding a section file with the matching id makes it live.

## Topic template
`<article class="topic" id data-k="search keywords">`: h3, `.lede` (the problem), how it works (table, `.seq` or `.flow` where it helps), Express/TS snippet, `.pit` common mistake, `.more` one or two links.

## Running example
Orders API for a shop. Tables: users, products, orders, order_items. Shared code so far: `app.ts`, `server.ts`, `db.ts` (`pool`, `withTransaction`, `replica`), `redis.ts`, `orders.ts` (`placeOrder`), `products.ts` (`getProduct`), `middleware/auth.ts` (`authenticate`, `requireRole`, `res.locals.user = { id, role }`), `routes/orders.ts`.

## Duplicates in the checklist: taught once
| Topic | Home | Later mention links back |
|---|---|---|
| Caching | 4 Data Storage (cache-aside) | 11 Caching Strategies adds stampede, write-through, layers |
| Replication | 4 (primary/replica) | 7 adds failover, multi-leader |
| Consistency | 4 (models) | 7 adds CAP, quorums |
| Locks | 6 Concurrency | 5 OS introduces, 6 applies |
| Database design / optimization | 3 Databases | 10 and 11 link back, add only what is new |

## Sessions
1. Shell, setup, 1 Internet, 2 APIs, 3 Databases, 4 Data Storage (done)
2. 5 Operating Systems, 6 Concurrency, 7 Distributed Systems, 8 Messaging (done; adds config.ts, retry.ts, mutex.ts, queues.ts, worker.ts, outbox and idempotency_keys tables; ids dist-replication, dist-consistency)
3. 9 Security, 10 System Design, 11 Performance (done; adds passwords.ts, tokens.ts, cache.ts, middleware csrf/limits/latency; ids oauth, system-database-design, bottlenecks). Still promised for session 4: Load Testing (from Throughput)
4. 12 Testing, 13 Deployment, 14 Observability (done; all 14 chapters written)

Forward references already promised: idempotency keys (8), race conditions (6), SQL injection and `verifyToken`/JWT/sessions (9), cache stampede (11), failover and cross-service consistency (7).

## Continuing in a new session
Add `src/sections/05-os.html` etc. with `<section class="cat" id="os" data-title="Operating Systems">` (ids: os, concurrency, distributed, messaging, security, design, performance, testing, deployment, observability), remove the matching `<span class="later">` chips, run `python3 build.py`, republish `index.html` to the same artifact.
