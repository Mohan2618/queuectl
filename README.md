# QueueCTL

A production-inspired command-line background job queue built in Python.

QueueCTL allows users to enqueue shell commands, execute them asynchronously using one or more workers, automatically retry failed jobs with exponential backoff, recover from worker crashes, and manage failed jobs through a Dead Letter Queue.

---

## Features

- Enqueue background jobs
- Continuous worker execution
- Multi-worker support
- SQLite persistence
- Worker locking
- Retry mechanism
- Exponential backoff
- Dead Letter Queue (DLQ)
- Crash recovery
- Runtime configuration
- Execution logging
- Unit tests

---

## Architecture

```
CLI
 │
 ▼
SQLite Database
 │
 ▼
Worker(s)
 │
 ▼
Command Executor
 │
 ├── Success → Completed
 │
 └── Failure
      │
      ▼
 Retry Scheduler
      │
      ├── Retry
      │
      └── Dead Letter Queue
```

---

## Project Structure

```
queuectl/
│
├── cli/
│   ├── enqueue.py
│   ├── worker.py
│   ├── list_jobs.py
│   ├── status.py
│   └── config.py
│
├── core/
│   ├── database.py
│   ├── executor.py
│   ├── scheduler.py
│   ├── recovery.py
│   ├── logger.py
│   ├── models.py
│   └── ...
│
├── tests/
│
├── logs/
│
├── queue.db
├── main.py
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Mohan2618/queuectl.git
cd queuectl
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Usage

Enqueue a job

```bash
python main.py enqueue --id job1 --command "echo Hello"
```

Start a worker

```bash
python main.py worker --id workerA
```

List jobs

```bash
python main.py list
```

Check status

```bash
python main.py status --id job1
```

Configure retry delay

```bash
python main.py config set retry_delay 2
```

---

## Retry Strategy

QueueCTL uses exponential backoff.

| Attempt | Delay |
|---------:|------:|
| 1 | 2 sec |
| 2 | 4 sec |
| 3 | 8 sec |

The base delay is configurable.

---

## Dead Letter Queue

Jobs exceeding the maximum retry count are automatically moved to the Dead Letter Queue for later inspection.

---

## Logging

Logs are stored in

```
logs/queuectl.log
```

Each log contains

- Worker startup
- Job execution
- Retries
- Failures
- Dead Letter Queue events
- Worker shutdown

---

## Running Tests

Run all tests

```bash
python -m unittest discover tests
```

---

## Technologies Used

- Python 3
- SQLite
- argparse
- subprocess
- logging
- unittest

---

## Future Improvements

- Job priorities
- Scheduled jobs
- REST API
- Web dashboard
- Docker support
- Metrics endpoint

---

## License

MIT License
