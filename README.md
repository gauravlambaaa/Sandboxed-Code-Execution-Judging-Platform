# Sandboxed Code Execution & Judging Platform

> A distributed backend for safely executing untrusted code and judging it against test cases — the engineering core behind systems like Codeforces, LeetCode, and HackerRank.

## What it does
Submit code in one of several languages against a problem's test cases, and get back a verdict — Accepted, Wrong Answer, Time Limit Exceeded, Memory Limit Exceeded, Runtime Error, or Compile Error — while the actual execution happens safely inside an isolated, resource-limited container, and the underlying job queue survives worker crashes without losing or duplicating work.

## Why this exists
Running arbitrary user-submitted code is a real security and reliability problem, not a solved one by default — a bare `subprocess.run()` call has no protection against infinite loops, memory bombs, or a submission trying to touch the network or filesystem. This project builds the actual safeguards a production judging system needs, from the ground up, rather than treating "run the code" as a one-liner.

## Architecture

```
┌────────────┐      ┌───────────────┐      ┌──────────────────┐
│  REST API  │─────▶│  PostgreSQL    │◀────▶│  Worker Pool      │
│ (submit,   │      │  job queue     │      │  (N processes)    │
│  poll      │      │  (row-level    │      │                   │
│  status)   │      │  locking)      │      │  Docker-sandboxed │
└────────────┘      └───────────────┘      │  execution per job │
                                             └──────────────────┘
```

- **API layer** — accepts submissions, returns a submission ID, exposes status/verdict polling
- **Queue** — PostgreSQL-backed; workers claim jobs using `SELECT ... FOR UPDATE SKIP LOCKED`, so multiple workers pull from the same table concurrently without ever grabbing the same job
- **Workers** — pull a job, spin up a Docker container with CPU/memory/process/network limits, execute the submission, compare output against expected test-case output, report a verdict back to the queue
- **Failure recovery** — a heartbeat/lease mechanism detects a worker that died mid-job and requeues it instead of losing it; judging is idempotent so a retried job can't double-report a result

## Tech stack
| Layer | Choice |
|---|---|
| API & workers | Go |
| Sandboxing | Docker (`--memory`, `--cpus`, `--pids-limit`, `--network none`) |
| Queue / persistence | PostgreSQL |
| Supported submission languages | C++, Python, Java |

## Key design decisions
- **Why Go**: goroutines make a correct concurrent worker pool straightforward to write and reason about.
- **Why Docker over raw subprocess execution**: resource limits and network isolation are non-negotiable when running code you don't control.
- **Why Postgres row-level locking (`SELECT FOR UPDATE SKIP LOCKED`) over a separate broker**: gets safe concurrent job distribution without introducing another moving piece (e.g. Redis/RabbitMQ) for a project this scoped.
- **Why heartbeat-based retry over "just hope workers don't crash"**: a worker dying mid-execution is a real failure mode in any distributed system, not an edge case worth ignoring.

## Getting started
```bash
git clone <repo-url>
cd judge-platform
docker-compose up
```
_(Setup instructions will be filled in as the build reaches a runnable state.)_

## Roadmap
- [ ] Bare pipeline — REST API + single in-process worker, one language, hardcoded test cases
- [ ] Docker-sandboxed execution with resource limits + cgroup-based TLE/MLE detection
- [ ] PostgreSQL-backed queue with `SELECT FOR UPDATE SKIP LOCKED` across concurrent workers
- [ ] Heartbeat-based failure recovery + idempotent verdict reporting
- [ ] Full problem/test-case schema + multi-testcase judging
- [ ] Minimal frontend (Monaco editor + live status polling)
- [ ] Multi-worker scaling via docker-compose + structured logging + load-test benchmark

## License
MIT
