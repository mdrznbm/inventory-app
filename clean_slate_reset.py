"""
Clean-slate reset for the inventory_app database.

Clears all Product and Transaction rows. Since models.py defines
primary keys as plain `db.Column(db.Integer, primary_key=True)`
(no AUTOINCREMENT keyword), SQLite naturally assigns the next ID
as 1 once a table is empty -- no manual counter reset needed.

Users are NOT touched by this script.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python clean_slate_reset.py
"""

from app import app
from models import db, Product, Transaction

with app.app_context():
    txn_count = Transaction.query.count()
    prod_count = Product.query.count()

    # Delete transactions first -- they hold FK references to products/users
    Transaction.query.delete()
    Product.query.delete()

    db.session.commit()

    print(f"Cleared {txn_count} transaction(s) and {prod_count} product(s).")
    print("IDs will restart at 1 on next insert. Users table untouched.")
