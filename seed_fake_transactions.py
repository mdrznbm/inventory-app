"""
Seeds fake transaction history for load-testing the stock reconciliation
report (vertical scaling demo). Does NOT touch app.py, models.py, or any
existing route.

This is additive only:
  - Does not delete or modify existing products, users, or transactions
  - Does not recalculate Product.current_stock (fake transactions are for
    report volume only, not a realistic live inventory state)

Safe to undo: run clean_slate_reset.py afterwards to wipe all transactions
and products back to a clean slate.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python seed_fake_transactions.py [count]

    count defaults to 2000 if not provided.
"""
import random
import sys
from datetime import datetime, timedelta
from app import app
from models import db, User, Product, Transaction

SEED_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

with app.app_context():
    products = Product.query.all()
    inbound_staff = User.query.filter_by(role='inbound_emp', is_account_active=True).all()
    outbound_staff = User.query.filter_by(role='outbound_emp', is_account_active=True).all()
    supervisors = User.query.filter_by(role='supervisor', is_account_active=True).all()

    if not products:
        print("No products found. Add at least one product before seeding.")
        sys.exit(1)
    if not inbound_staff or not outbound_staff or not supervisors:
        print("Need at least one active inbound, outbound, and supervisor account before seeding.")
        sys.exit(1)

    statuses = ['APPROVED'] * 8 + ['REJECTED'] * 1 + ['PENDING'] * 1  # weighted mix
    now = datetime.utcnow()

    new_transactions = []
    for i in range(SEED_COUNT):
        is_inbound = random.choice([True, False])
        product = random.choice(products)
        status = random.choice(statuses)
        quantity = random.randint(1, 50)
        created_at = now - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))

        if is_inbound:
            requester = random.choice(inbound_staff)
        else:
            requester = random.choice(outbound_staff)

        txn = Transaction(
            txn_type='INBOUND' if is_inbound else 'OUTBOUND',
            quantity=quantity,
            status=status,
            user_id=requester.id,
            product_id=product.id,
            requester_name_snapshot=requester.name,
            created_at=created_at,
        )

        if status == 'APPROVED':
            approver = random.choice(supervisors)
            txn.approved_at = created_at + timedelta(minutes=random.randint(1, 120))
            txn.actioned_by_user_id = approver.id
            txn.actioned_by_name_snapshot = approver.name
        elif status == 'REJECTED':
            approver = random.choice(supervisors)
            txn.rejected_at = created_at + timedelta(minutes=random.randint(1, 120))
            txn.actioned_by_user_id = approver.id
            txn.actioned_by_name_snapshot = approver.name
            txn.rejection_reason = 'Seeded test rejection'

        new_transactions.append(txn)

        if (i + 1) % 500 == 0:
            print(f"  ...{i + 1}/{SEED_COUNT} prepared")

    db.session.bulk_save_objects(new_transactions)
    db.session.commit()

    print(f"\nSeeded {SEED_COUNT} fake transactions across {len(products)} product(s).")
    print("Note: Product.current_stock was NOT recalculated (see script docstring).")
    print("Run clean_slate_reset.py afterwards to remove this test data.")
