# Submission Guide — PhishGuard Project

Use this guide when submitting your cybersecurity internship project to college or organization.

---

## What to Submit

| Item | File / Folder | Description |
|------|---------------|-------------|
| **Source code** | `PhishingSimulationPlatform/` (entire folder) | Python + Flask application |
| **Project report** | `PROJECT_REPORT.md` | Convert to PDF for submission |
| **Setup instructions** | `README.md` | How to install and run |
| **Student details** | `project_info.py` | Edit with your name, roll no., college |
| **Screenshots** | Take from running website | Home, demo, admin dashboard, micro-learning |

---

## Before You Submit

1. Open `project_info.py` and fill in your **name, roll number, college, guide name**.
2. Run the website and take **4–5 screenshots**:
   - Homepage (`http://127.0.0.1:5000`)
   - Fake login page (click **Try Demo**)
   - Micro-learning page (after submitting dummy credentials)
   - Admin dashboard (`/admin` — login: `admin` / `change-me`)
3. Export `PROJECT_REPORT.md` to **PDF** (Word, Google Docs, or VS Code Markdown PDF extension).
4. Zip the project folder (exclude `.venv` folder to reduce size).

---

## How to Run (For Evaluator)

### Windows

```powershell
cd PhishingSimulationPlatform
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Or double-click **`run.bat`**.

Open browser: **http://127.0.0.1:5000**

### Demo Without Email

1. Open http://127.0.0.1:5000
2. Click **Try Live Demo**
3. Enter any dummy email/password on fake login page
4. Read micro-learning page
5. Login to admin: http://127.0.0.1:5000/admin (`admin` / `change-me`)

---

## Project Highlights (For Viva / Presentation)

- **Problem:** Phishing is the #1 initial access vector in breaches.
- **Solution:** Controlled simulation + metrics + instant training.
- **Tech stack:** Python, Flask, SQLite, smtplib, HTML/CSS.
- **Security:** Passwords are never stored; emails are hashed.
- **Ethics:** Authorized training only; disclaimers on all pages.

---

## Admin Login (Default)

- **URL:** http://127.0.0.1:5000/admin
- **Username:** `admin`
- **Password:** `change-me`

Change these in `.env` before final submission if required.
