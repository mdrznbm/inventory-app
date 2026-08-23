"""
One-time migration: adds permanent name-snapshot columns to the
existing transactions table, preserving all current rows.

New columns:
    requester_name_snapshot   VARCHAR(50) (nullable)
    actioned_by_name_snapshot VARCHAR(50) (nullable)

Why this is needed: staff IDs get recycled when an employee is
deactivated and a new hire is auto-assigned their old ID. Since
User rows were being reused (to satisfy the unique staff_id
constraint), the *name* on that row would silently change --
meaning old transaction history would start showing the new
hire's name instead of the original employee who actually made
the request or approval. These new columns permanently record
the name at the exact moment the transaction happened, so history
stays accurate even after a staff ID is later reassigned.

Safe to run once. Running it a second time will simply report that
the columns already exist and do nothing.

Note: this migration only adds the columns -- it does NOT backfill
existing rows with a snapshot (there's no way to know what name was
correct retroactively for a row that's already been overwritten).
Run this before doing a clean-slate reset so all future transactions
are captured correctly from this point forward.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python add_name_snapshot_columns.py
"""

import sqlite3

DB_PATH = 'instance/inventory.db'

NEW_COLUMNS = [
    ("requester_name_snapshot", "VARCHAR(50)"),
    ("actioned_by_name_snapshot", "VARCHAR(50)"),
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
