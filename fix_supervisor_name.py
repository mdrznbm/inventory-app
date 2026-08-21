"""
One-off fix: capitalizes the supervisor account's (s001) name.

s001 was seeded directly by the `flask init-db` CLI command with a
hardcoded lowercase name ('john'), which predates the auto-capitalization
logic added to the Register New Employee form. That logic only runs on
new registrations through the form, so the original seed data was never
touched.

Usage:
    cd ~/projects/inventory_app
    source venv/bin/activate
    python fix_supervisor_name.py
"""

from app import app
from models import db, User

with app.app_context():
    user = User.query.filter_by(staff_id='s001').first()

    if not user:
        print("s001 not found -- nothing to do.")
    else:
        old_name = user.name
        capitalized = ' '.join(part.capitalize() for part in old_name.split())

        if old_name == capitalized:
            print(f"s001's name ('{old_name}') is already properly capitalized.")
        else:
            user.name = capitalized
            db.session.commit()
            print(f"Updated s001's name: '{old_name}' -> '{capitalized}'")
