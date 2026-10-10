from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "gramshala.db"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                joined_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                synced INTEGER NOT NULL DEFAULT 0,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id)
            );
            """
        )
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(attempts)")}
        if "answers" not in cols:
            conn.execute("ALTER TABLE attempts ADD COLUMN answers TEXT")


def upsert_student(student_id: str, name: str) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO students (id, name, joined_at) VALUES (?, ?, ?)",
            (student_id, name.strip() or "Student", utcnow()),
        )
        conn.commit()


def save_attempt(
    attempt_id: str,
    student_id: str,
    lesson_id: str,
    score: int,
    total: int,
    answers: list[int] | None = None,
) -> None:
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO attempts (id, student_id, lesson_id, score, total, synced, completed_at, answers)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (attempt_id, student_id, lesson_id, score, total, utcnow(), json.dumps(answers or [])),
        )
        conn.commit()


def all_attempts() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT a.id, a.student_id, s.name, a.lesson_id, a.score, a.total,
                   a.answers, a.synced, a.completed_at
            FROM attempts a
            JOIN students s ON s.id = a.student_id
            ORDER BY a.completed_at ASC, a.rowid ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def roster() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT s.id, s.name, s.joined_at,
                   COUNT(a.id) AS lessons_done,
                   COALESCE(SUM(a.score), 0) AS points,
                   COALESCE(SUM(a.total), 0) AS points_possible
            FROM students s
            LEFT JOIN attempts a ON a.student_id = s.id
            GROUP BY s.id
            ORDER BY s.joined_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def unsynced_count() -> int:
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM attempts WHERE synced = 0").fetchone()
        return int(row["n"]) if row else 0


def mark_synced() -> int:
    with get_db() as conn:
        cur = conn.execute("UPDATE attempts SET synced = 1 WHERE synced = 0")
        conn.commit()
        return cur.rowcount
