"""
One-time migration: adds accountability tracking columns to the
existing transactions table, preserving all current rows.

New columns:
    actioned_by_user_id INTEGER (nullable -- the supervisor who
    approved OR rejected this transaction)
    rejected_at DATETIME (nullable -- symmetric with the existing
    approved_at column, populated only for rejected transactions)

Safe to run once. Running it a second time will simply report that
the columns already exist and do nothing.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python add_actioned_by_columns.py
"""

import sqlite3

DB_PATH = 'instance/inventory.db'

NEW_COLUMNS = [
    ("actioned_by_user_id", "INTEGER"),
    ("rejected_at", "DATETIME"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

existing_columns = {row[1] for row in cur.execute("PRAGMA table_info(transactions)")}

added = []
skipped = []

for col_name, col_def in NEW_COLUMNS:
    if col_name in existing_columns:
        skipped.append(col_name)
        continue
    cur.execute(f"ALTER TABLE transactions ADD COLUMN {col_name} {col_def}")
    added.append(col_name)

conn.commit()
conn.close()

if added:
    print(f"Added column(s): {', '.join(added)}")
if skipped:
    print(f"Already present, skipped: {', '.join(skipped)}")
if not added and not skipped:
    print("No changes made.")
