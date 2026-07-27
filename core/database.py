import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("queue.db")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

        self.create_tables()
        self.migrate_database()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            command TEXT NOT NULL,
            state TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3,
            next_retry_at TEXT,
            worker_id TEXT,
            stdout TEXT,
            stderr TEXT,
            exit_code INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dead_jobs (
            id TEXT PRIMARY KEY,
            command TEXT,
            attempts INTEGER,
            stdout TEXT,
            stderr TEXT,
            exit_code INTEGER,
            failed_at TEXT
        )
        """)

        self.conn.commit()


    def move_to_dead_letter(self, job):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO dead_jobs (
                id,
                command,
                attempts,
                stdout,
                stderr,
                exit_code,
                failed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job["id"],
            job["command"],
            job["attempts"],
            job["stdout"],
            job["stderr"],
            job["exit_code"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        cursor.execute(
            "DELETE FROM jobs WHERE id = ?",
            (job["id"],)
        )

        self.conn.commit()

    def migrate_database(self):
        cursor = self.conn.cursor()

        migrations = [
            ("stdout", "TEXT"),
            ("stderr", "TEXT"),
            ("exit_code", "INTEGER"),
        ]

        for column, datatype in migrations:
            try:
                cursor.execute(
                    f"ALTER TABLE jobs ADD COLUMN {column} {datatype}"
                )
                print(f"Added column: {column}")
            except sqlite3.OperationalError:
                # Column already exists
                pass

        self.conn.commit()

    # --------------------------------------------------
    # Job Operations
    # --------------------------------------------------

    def insert_job(self, job):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO jobs (
            id,
            command,
            state,
            attempts,
            max_retries,
            next_retry_at,
            worker_id,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job.id,
            job.command,
            job.state,
            job.attempts,
            job.max_retries,
            job.next_retry_at,
            job.worker_id,
            job.created_at,
            job.updated_at
        ))

        self.conn.commit()

    def get_job(self, job_id):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,)
        )

        return cursor.fetchone()

    def get_all_jobs(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM jobs")

        return cursor.fetchall()

    def get_jobs_by_state(self, state=None):
        cursor = self.conn.cursor()

        if state:
            cursor.execute(
                "SELECT * FROM jobs WHERE state = ?",
                (state,)
            )
        else:
            cursor.execute("SELECT * FROM jobs")

        return cursor.fetchall()

    def get_next_pending_job(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE state = 'pending'
            ORDER BY created_at
        """)

        jobs = cursor.fetchall()

        for job in jobs:
            retry_time = job["next_retry_at"]

            if retry_time is None:
                return job

            retry_time = datetime.strptime(
                retry_time,
                "%Y-%m-%d %H:%M:%S"
            )

            if datetime.now() >= retry_time:
                return job

        return None

    # --------------------------------------------------
    # Update Operations
    # --------------------------------------------------

    def update_job_state(self, job_id, state):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET state = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            state,
            job_id
        ))

        self.conn.commit()

    def update_job_result(self, job_id, stdout, stderr, exit_code):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET stdout = ?,
                stderr = ?,
                exit_code = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            stdout,
            stderr,
            exit_code,
            job_id
        ))

        self.conn.commit()

    def increment_attempt(self, job_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET attempts = attempts + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            job_id,
        ))

        self.conn.commit()

    def schedule_retry(self, job_id, retry_time):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET next_retry_at = ?,
                state = 'pending',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            retry_time.strftime("%Y-%m-%d %H:%M:%S"),
            job_id
        ))

        self.conn.commit()

    def claim_job(self, job_id, worker_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET
                state = 'running',
                worker_id = ?
            WHERE
                id = ?
                AND state = 'pending'
        """, (
            worker_id,
            job_id
        ))

        self.conn.commit()

        return cursor.rowcount == 1

    def recover_running_jobs(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET
                state = 'pending',
                worker_id = NULL
            WHERE
                state = 'running'
        """)

        self.conn.commit()

        return cursor.rowcount

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def close(self):
        self.conn.close()