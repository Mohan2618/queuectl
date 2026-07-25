import sqlite3
from pathlib import Path

DB_PATH = Path("queue.db")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

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


    def get_all_jobs(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM jobs")

        return cursor.fetchall()

    def close(self):
        self.conn.close()