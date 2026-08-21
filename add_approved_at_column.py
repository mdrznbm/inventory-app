"""
One-time migration: adds the approved_at timestamp column to the
existing transactions table, preserving all current rows.

New column:
    approved_at DATETIME (nullable -- populated only once a
    transaction is approved by a supervisor; stays NULL for
    still-pending or rejected transactions)

Safe to run once. Running it a second time will simply report that
the column already exists and do nothing.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python add_approved_at_column.py
"""

import sqlite3

DB_PATH = 'instance/inventory.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

existing_columns = {row[1] for row in cur.execute("PRAGMA table_info(transactions)")}

if "approved_at" in existing_columns:
    print("Column 'approved_at' already exists, skipped.")
else:
    cur.execute("ALTER TABLE transactions ADD COLUMN approved_at DATETIME")
    conn.commit()
    print("Added column: approved_at")

conn.close()
