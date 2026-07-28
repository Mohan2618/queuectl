# QueueCTL Design Decisions

## Database

SQLite was chosen because it is lightweight, requires no installation, and is suitable for a single-node job queue.

---

## Job States

Each job moves through the following lifecycle:

Pending
→ Running
→ Completed

or

Pending
→ Running
→ Retry
→ Dead Letter Queue

This makes the workflow easy to understand and debug.

---

## Retry Strategy

QueueCTL uses exponential backoff for retries.

Delay =
base_delay × (2^(attempt-1))

Example:

Attempt 1 → 5 seconds

Attempt 2 → 10 seconds

Attempt 3 → 20 seconds

This prevents continuously retrying failing jobs.

---

## Worker Coordination

Multiple workers safely process jobs using an atomic claim operation in SQLite.

This prevents two workers from executing the same job simultaneously.

---

## Dead Letter Queue

Jobs that exceed the maximum retry count are moved into a separate
dead_jobs table for later inspection.

This keeps the active queue clean while preserving failed jobs.

---

## Crash Recovery

If a worker crashes while executing a job, QueueCTL automatically resets
stale running jobs back to pending so another worker can resume processing.

---

## Configuration

Runtime configuration values such as retry_delay and poll_interval are stored
inside the config table instead of hardcoding them.

---

## Logging

The worker writes logs using Python's logging module to make debugging and
monitoring easier.

---

## Testing

Unit tests cover:

- Database operations
- Scheduler
- Executor

ensuring the core components work correctly.
