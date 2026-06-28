from sqlite3 import Cursor


import hashlib
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DATABASE_PATH


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_identifier(value: str) -> str:
    """One-way hash for correlating events without storing raw emails."""
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()[:16]


@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                email_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (recipient_id) REFERENCES recipients(id)
            );
            """
        )


def create_campaign(name: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO campaigns (name, created_at) VALUES (?, ?)",
            (name, utc_now()),
        )
        return cursor.lastrowid or 0


def create_recipient(campaign_id: int, email: str, token: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO recipients (campaign_id, token, email_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (campaign_id, token, hash_identifier(email), utc_now()),
        )
        return cursor.lastrowid or 0



def get_recipient_by_token(token: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM recipients WHERE token = ?",
            (token,),
        ).fetchone()
        return dict(row) if row else None


def log_event(
    recipient_id: int,
    event_type: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
    metadata: str | None = None,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO events (recipient_id, event_type, ip_address, user_agent, metadata, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (recipient_id, event_type, ip_address, user_agent, metadata, utc_now()),
        )


def get_campaign_summary():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                c.id,
                c.name,
                c.created_at,
                COUNT(DISTINCT r.id) AS recipients,
                SUM(CASE WHEN e.event_type = 'link_clicked' THEN 1 ELSE 0 END) AS clicks,
                SUM(CASE WHEN e.event_type = 'landing_viewed' THEN 1 ELSE 0 END) AS landing_views,
                SUM(CASE WHEN e.event_type = 'form_submitted' THEN 1 ELSE 0 END) AS submissions
            FROM campaigns c
            LEFT JOIN recipients r ON r.campaign_id = c.id
            LEFT JOIN events e ON e.recipient_id = r.id
            GROUP BY c.id
            ORDER BY c.created_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_recent_events(limit: int = 50):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                e.event_type,
                e.ip_address,
                e.user_agent,
                e.metadata,
                e.created_at,
                c.name AS campaign_name,
                r.email_hash
            FROM events e
            JOIN recipients r ON r.id = e.recipient_id
            JOIN campaigns c ON c.id = r.campaign_id
            ORDER BY e.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
