# Getting Started — A Guide for the Team

This guide is written for teammates who are new to Git, GitHub, and running a Python project locally. Follow it step by step — nothing here assumes you already know these tools.

If you get stuck at any point, that's completely normal. Reach out to the team rather than guessing, especially before running any command you're unsure about.

---

## Part 1: Accept the GitHub Invitation

1. Check your email (and spam folder) for an invitation from GitHub to collaborate on `mdrznbm/inventory-app`.
2. Click the link in the email and accept the invitation.
3. If you don't already have a GitHub account, you'll need to create one first (it's free) — go to [github.com](https://github.com) and sign up, then ask to be re-invited.

---

## Part 2: Install the Tools You'll Need

You'll need three things installed on your computer:

1. **Git** — lets you download and update the project code.
   Check if you already have it by opening a terminal (Command Prompt / PowerShell on Windows, Terminal on Mac) and typing:
   ```bash
   git --version
   ```
   If you see a version number, you're set. If not, download it from [git-scm.com](https://git-scm.com/downloads) and install it with default options.

2. **Python 3** — the language the app is written in.
   Check with:
   ```bash
   python3 --version
   ```
   (On Windows, try `python --version` instead.) If it's not installed, download it from [python.org](https://python.org) — during installation on Windows, make sure to tick **"Add Python to PATH"**.

3. **A code editor** — [VS Code](https://code.visualstudio.com/) is a good free option if you don't already have one.

---

## Part 3: Download the Project

1. Open a terminal.
2. Navigate to wherever you'd like to keep the project (e.g., your Desktop or a dedicated "projects" folder):
   ```bash
   cd Desktop
   ```
3. Clone the repository (this downloads a copy of the project to your computer):
   ```bash
   git clone https://github.com/mdrznbm/inventory-app.git
   ```
4. Move into the new folder it created:
   ```bash
   cd inventory-app
   ```

---

## Part 4: Set Up the Project to Run

These steps create an isolated Python environment for the project, so it doesn't interfere with anything else on your computer.

1. **Create the virtual environment:**
   ```bash
   python3 -m venv venv
   ```
   (On Windows, this may need to be `python -m venv venv` instead.)

2. **Activate it:**
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows (Command Prompt):
     ```bash
     venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```bash
     venv\Scripts\Activate.ps1
     ```
   You'll know it worked if you see `(venv)` appear at the start of your terminal line.

   **Important:** you'll need to activate the venv every time you open a new terminal to work on this project. If commands stop working with errors about missing packages, check whether `(venv)` is showing — if not, run the activation command again.

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   flask init-db
   ```
   This creates the database file and adds an initial supervisor account plus some sample products. You should only need to do this once.

5. **Run the app:**
   ```bash
   python app.py
   ```
   You should see output saying the server is running. Leave this terminal window open — closing it stops the app.

6. **Open the app in your browser:**
   Go to `http://localhost:5001`

7. **Log in:**
   The login page itself lists the current active test credentials at the bottom of the login box — use one of those to sign in and explore the app.

To stop the app, go back to the terminal and press `Ctrl+C`.

---

## Part 5: Basic Git Commands You'll Need

**Important:** `main` is protected — nobody, including the project owner, can push directly to it. The commands below are the building blocks of everyday Git use, but they only work as shown when you're working on your own branch, not on `main` directly. Part 6 (right after this) shows the full picture — read both parts together before making your first change.

Once you start making changes, here's the everyday workflow:

1. **Before you start working, get the latest version of the project:**
   ```bash
   git pull
   ```

2. **After making changes**, check what's changed:
   ```bash
   git status
   ```

3. **Stage the files you want to save** (replace `filename.py` with the actual file, or use `.` to stage everything):
   ```bash
   git add filename.py
   ```

4. **Commit your changes** with a short description of what you did:
   ```bash
   git commit -m "Describe what you changed here"
   ```

5. **Push your changes to GitHub** so the rest of the team can see them:
   ```bash
   git push
   ```
   On `main`, this step will be rejected — see Part 6 for how pushing actually works in this project.

If `git push` ever fails and asks for a username/password, note that GitHub no longer accepts your account password directly — you'll need a **Personal Access Token** instead. Ask the team for help setting this up if you hit this.

---

## Part 6: Working on a Branch (Important!)

This applies to **everyone on the team, including the project owner** — nobody pushes directly to `main`, no exceptions. `main` is protected on GitHub, so a direct push will simply be rejected regardless of who attempts it.

To keep the main version of the project safe and working at all times, **please don't commit changes directly to `main`**. Instead, do your work on a separate "branch" — think of it as your own private copy of the project where you can experiment freely without affecting anyone else's work or breaking the live app.

Here's the flow:

1. **Before starting new work, make sure you have the latest version:**
   ```bash
   git checkout main
   git pull
   ```

2. **Create your own branch** (replace `your-name-feature` with something short and descriptive, like `alisha-docker-setup`):
   ```bash
   git checkout -b your-name-feature
   ```
   This both creates the branch and switches you onto it.

3. **Work normally** — edit files, then:
   ```bash
   git add .
   git commit -m "Describe what you changed"
   ```

4. **Push your branch** (note: slightly different from before, since this branch doesn't exist on GitHub yet):
   ```bash
   git push -u origin your-name-feature
   ```

5. **Open a Pull Request on GitHub:**
   - Go to the repository on GitHub — you should see a banner suggesting you open a Pull Request for your recently pushed branch. Click it.
   - Add a short description of what you changed.
   - Submit the Pull Request.

6. **Wait for review.** Someone (usually whoever knows the codebase best) will review your Pull Request and either merge it into `main`, or ask you to make some changes first. This step is what keeps `main` safe — nothing gets merged in until it's been checked.

If you want to keep working on something else after this, switch back to `main` first and repeat from step 1 with a new branch name.

---



- **"command not found" errors** — usually means the tool (git/python) isn't installed correctly, or isn't added to your system PATH. Reinstall and make sure any "add to PATH" option is checked.
- **`(venv)` isn't showing in your terminal** — you forgot to activate the virtual environment (see Part 4, step 2). Run the activation command again.
- **"No module named flask" or similar** — the virtual environment isn't activated, or `pip install -r requirements.txt` wasn't run. Check both.
- **The app won't start / port already in use** — you may already have the app running in another terminal window. Close it first.

---

## A Note on the Utility Scripts

You'll see some `.py` files in the project root like `clean_slate_reset.py` and `trim_staff.py`. **Do not run these unless you know exactly what they do** — several of them delete data. Check the main `README.md`'s "Utility Scripts" section for what each one does before running anything you haven't used before.

---

Welcome to the project — don't hesitate to ask questions as you go.
