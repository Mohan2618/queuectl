from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Job:
    id: str
    command: str
    state: str = "pending"
    attempts: int = 0
    max_retries: int = 3
    next_retry_at: str | None = None
    worker_id: str | None = None
    created_at: str = field(
    default_factory=lambda: datetime.now(UTC).isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )