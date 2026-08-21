"""
One-time migration: adds account-lockout tracking columns to the
existing users table, preserving all current rows.

New columns:
    failed_login_attempts INTEGER NOT NULL DEFAULT 0
    is_locked             BOOLEAN NOT NULL DEFAULT 0
    lock_requested_at     DATETIME (nullable)

Safe to run once. Running it a second time will simply report that
the columns already exist and do nothing.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python add_lockout_columns.py
"""

import sqlite3

DB_PATH = 'instance/inventory.db'

NEW_COLUMNS = [
    ("failed_login_attempts", "INTEGER NOT NULL DEFAULT 0"),
    ("is_locked", "BOOLEAN NOT NULL DEFAULT 0"),
    ("lock_requested_at", "DATETIME"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

existing_columns = {row[1] for row in cur.execute("PRAGMA table_info(users)")}

added = []
skipped = []

for col_name, col_def in NEW_COLUMNS:
    if col_name in existing_columns:
        skipped.append(col_name)
        continue
    cur.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
    added.append(col_name)

conn.commit()
conn.close()

if added:
    print(f"Added column(s): {', '.join(added)}")
if skipped:
    print(f"Already present, skipped: {', '.join(skipped)}")
if not added and not skipped:
    print("No changes made.")
