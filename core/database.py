import sqlite3
from pathlib import Path

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

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        self.conn.commit()

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

    def get_next_pending_job(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE state = 'pending'
            ORDER BY created_at
            LIMIT 1
        """)

        return cursor.fetchone()

    def update_job_state(self, job_id, state):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET state = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (state, job_id))

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

    def close(self):
        self.conn.close()