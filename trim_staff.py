"""
Trim the staff roster down to a lean startup team:
    s001 (john, supervisor)

Removes: ib001 (Razin), ib002 (Jack), ob001 (Jeff), ob002 (Hazrul), ob003 (Alice Jackson)

Safety: Transaction.user_id is a required (nullable=False) foreign
key to users.id. This script first checks whether any of the
to-be-removed users have transaction history. If they do, it stops
and reports which ones -- deleting a user with existing transactions
would break that FK relationship.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python trim_staff.py
"""

from app import app
from models import db, User, Transaction

STAFF_IDS_TO_REMOVE = ['s002', 'ib002', 'ob002', 'ob003', 'ib001', 'ob001']
STAFF_IDS_TO_KEEP = ['s001']

with app.app_context():
    users_to_remove = User.query.filter(User.staff_id.in_(STAFF_IDS_TO_REMOVE)).all()

    if not users_to_remove:
        print("None of the target staff IDs were found -- nothing to do.")
    else:
        blocked = []
        for u in users_to_remove:
            txn_count = Transaction.query.filter_by(user_id=u.id).count()
            if txn_count > 0:
                blocked.append((u.staff_id, u.name, txn_count))

        if blocked:
            print("Cannot proceed -- the following users have existing transaction history:")
            for staff_id, name, count in blocked:
                print(f"  {staff_id} ({name}): {count} transaction(s)")
            print("Resolve or reassign those transactions first, then rerun this script.")
        else:
            removed = [(u.staff_id, u.name) for u in users_to_remove]
            for u in users_to_remove:
                db.session.delete(u)
            db.session.commit()

            print("Removed the following staff accounts:")
            for staff_id, name in removed:
                print(f"  {staff_id} ({name})")

            remaining = User.query.order_by(User.staff_id).all()
            print("\nRemaining staff:")
            for u in remaining:
                print(f"  {u.staff_id} ({u.name}) - {u.role}")
