# Warehouse Inventory Management System

A Flask-based warehouse inventory management system built as the final project for a 3-month Cloud Support / DevOps bootcamp. The app supports three roles — **Supervisor**, **Inbound Employee**, and **Outbound Employee** — with a full approval workflow, security controls, and a live audit trail.

## Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite
- **Frontend:** Bootstrap 5.3 (with light/dark mode support), Jinja2 templates
- **Deployment (in progress):** Docker, targeting Microsoft Azure with vertical/horizontal scaling

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mdrznbm/inventory-app.git
cd inventory-app
```

### 2. Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize the database
```bash
flask init-db
```
This creates `instance/inventory.db` and seeds an initial supervisor account plus a few sample products.

### 4. Run the app
```bash
python app.py
```
The app runs on `http://localhost:5001` by default.

### 5. Log in
Check the login page itself — it dynamically lists **Active Test Credentials** for every currently active account, so this stays accurate even as staff are added, removed, or reset. Staff IDs follow the pattern `s001`/`ib001`/`ob001`, and default passwords follow `firstname123`.

## Roles

| Role | Can do |
|---|---|
| **Supervisor** | Approve/reject inbound & outbound requests; register, edit, deactivate/reactivate, and reset passwords for employees and other supervisors; view full transaction history per product |
| **Inbound Employee** | Submit stock-receiving requests (existing SKUs or new items with auto-generated SKUs); view own request history |
| **Outbound Employee** | Submit stock-withdrawal requests; view own request history and full SKU movement audit |

## Features

### Staff Management
- Auto-generated Staff IDs and default passwords (`firstname123`) on registration
- First Name / Last Name fields with automatic capitalization
- Auto-balancing department assignment for new Inbound/Outbound hires (assigns to whichever department is understaffed); Supervisor registration is always available regardless of balance
- Multiple supervisors supported — any supervisor can deactivate any other, but never themselves, guaranteeing at least one active supervisor always remains
- In-app "Edit" feature on every staff row to correct name typos/capitalization without needing a database script

### Security
- Default-password reminder banner (dismissible per visit, reappears until changed)
- Self-service Change Password flow (old password, new password, confirmation)
- Account lockout after 3 failed login attempts
- Supervisor-facing "Password Reset Requests" panel to reset locked-out accounts back to their default password
- Works reciprocally between multiple supervisors (one can rescue another)

### Inventory & Approval Workflow
- Inbound: receive stock against an existing SKU, or register new items with auto-generated SKUs
- Outbound: request stock withdrawal (blocked if insufficient stock)
- Supervisor approval queue for all pending requests, with Approve / Reject (with required reason) actions
- Full accountability trail: every approved/rejected transaction records **who** actioned it and **when**, plus the stated reason for any rejection — visible on the Supervisor, Inbound, and Outbound dashboards
- Per-product transaction history modal on the Supervisor's Live Stock Overview
- "My Request History" panel for both Inbound and Outbound employees, showing their own submissions and outcomes

### UI
- Light/dark mode toggle (saved per-browser via localStorage), with dark-mode-specific contrast fixes
- Staff Directory grouped into Supervisor / Inbound / Outbound sections with aligned columns

## Project Structure

```
inventory_app/
├── app.py                  # Flask routes and application logic
├── models.py                # SQLAlchemy models (User, Product, Transaction)
├── templates/                # Jinja2 templates
│   ├── base.html             # Shared layout, navbar, dark mode toggle
│   ├── login.html
│   ├── supervisor.html
│   ├── inbound.html
│   ├── outbound.html
│   └── change_password.html
├── static/css/style.css      # Custom styling, dark mode overrides
├── instance/inventory.db     # SQLite database (not tracked in git)
├── Dockerfile, compose.yaml  # Containerization (in progress)
└── requirements.txt
```

## Utility Scripts

A few one-off scripts exist for managing test data during development. **Use with care** — several of these are destructive.

| Script | Purpose |
|---|---|
| `clean_slate_reset.py` | Clears all products and transactions (users untouched) — simulates a brand-new warehouse |
| `trim_staff.py` | Removes all staff except the primary supervisor (`s001`) — resets staff roster to baseline |
| `fix_supervisor_name.py` | One-off name capitalization fix (superseded by the in-app Edit feature, kept for reference) |
| `add_lockout_columns.py` | Database migration: adds account-lockout tracking columns |
| `add_approved_at_column.py` | Database migration: adds approval timestamp column |
| `add_actioned_by_columns.py` | Database migration: adds accountability tracking columns (who approved/rejected) |

Migration scripts only need to be run once against an existing database and are safe to re-run (they detect already-applied changes and skip them).

## Project Status

- ✅ Core application features (staff management, security, inventory workflow, audit trail, UI)
- 🔲 Docker packaging
- 🔲 Deployment to Microsoft Azure
- 🔲 Vertical & horizontal scaling demonstration

## Contributing

This is a team project, and `main` is kept protected — all changes go through a branch and a Pull Request, never a direct commit to `main`. This keeps the live app stable even while multiple people are working on it.

If you're picking this up for the first time — especially if you're new to Git or Python — see **[GETTING_STARTED.md](GETTING_STARTED.md)** for a detailed, step-by-step setup and workflow guide.

If you're already comfortable with these tools, the short version:
1. Follow the **Getting Started** steps above to get a local copy running
2. Check `git log --oneline` for the full history of what's been built and why
3. Create a branch for your work, commit and push there, then open a Pull Request for review before it's merged into `main`
