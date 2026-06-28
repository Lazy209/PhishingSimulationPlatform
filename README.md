# PhishGuard — Phishing Simulation Platform

**Cybersecurity Internship Project**

A controlled security awareness lab built with Python and Flask. Simulates phishing campaigns, tracks engagement safely, and delivers post-click micro-learning.

> **Authorized use only.** For lab environments with explicit consent from all participants.

## Submit This Project to College

1. **Edit your details** in `project_info.py` (name, roll number, college, guide)
2. **Read** `SUBMISSION_GUIDE.md` for the full checklist
3. **Export** `PROJECT_REPORT.md` to PDF and attach screenshots
4. **Zip** the folder (exclude `.venv`) and submit

**Quick run for evaluator:** Double-click `run.bat` → open http://127.0.0.1:5000

| Document              | Purpose                        |
|-----------------------|--------------------------------|
| `PROJECT_REPORT.md`   | Full academic project report   |
| `SUBMISSION_GUIDE.md` | What to submit and how to demo |
| `project_info.py`     | Your student/college details   |

## Features

| Component               | Description                                                                |
|-------------------------|----------------------------------------------------------------------------|
| **Mock phishing email** | `smtplib` script sends a realistic HTML email with a unique tracking link  |
| **Dummy login page**    | Microsoft-style landing page at `/verify/<token>`                          |
| **Safe metrics**        | Logs clicks, page views, and form submissions — **never stores passwords** |
| **Micro-learning**      | Post-submit education page explaining missed phishing indicators           |
| **Admin dashboard**     | Campaign stats, click/submit rates, and event timeline                     |

## Architecture

```
send_campaign.py  ──►  SMTP email with /t/<token> link
                              │
                              ▼
                         app.py (Flask)
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   track_click()      landing_page()      microlearning()
   (link_clicked)     (landing_viewed)    (training_viewed)
         │                    │
         │              submit_credentials()
         │              (form_submitted — no password stored)
         ▼
   SQLite metrics.db  ◄──  admin_dashboard()
```

## Quick Start

### 1. Install dependencies

```powershell
cd PhishingSimulationPlatform
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```powershell
copy .env.example .env
```

Edit `.env` with your SMTP credentials (Gmail App Password, Mailtrap, etc.) and admin login.

### 3. Start the web server

```powershell
python app.py
```

Open http://127.0.0.1:5000

### 4. Send a test campaign

Dry run (generates link without sending email):

```powershell
python send_campaign.py --email your-test@example.com --dry-run
```

Send real email (requires SMTP config):

```powershell
python send_campaign.py --email your-test@example.com --name "Your Name"
```

### 5. Walk through the simulation

1. Click the tracking link in the email (or paste the dry-run URL)
2. View the fake login page
3. Submit any dummy credentials
4. Read the micro-learning page
5. Check metrics at http://127.0.0.1:5000/admin

## Security Design

- **No password persistence** — the password field is read and immediately discarded
- **Hashed recipient IDs** — email addresses stored as SHA-256 prefixes, not plaintext
- **Unique tokens** — each recipient gets a cryptographically random tracking token
- **Training disclaimer** — simulation footer in email and landing page

## Event Types

| Event             | Trigger                                           |
|-------------------|---------------------------------------------------|
| `link_clicked`    | User clicks email tracking link                   |
| `landing_viewed`  | Fake login page loaded                            |
| `form_submitted`  | Login form submitted (username length only logged)|
| `training_viewed` | Micro-learning page viewed                        |

## Internship Presentation Points

1. **Social engineering mechanics** — urgency, spoofed branding, credential harvesting flow
2. **Web development** — Flask routing, Jinja2 templates, form handling
3. **Security metrics** — click rate, submission rate, funnel analysis
4. **Defensive awareness** — domain verification, sender inspection, reporting workflows
5. **Ethical constraints** — consent, data minimization, no credential storage

## Project Structure

```
PhishingSimulationPlatform/
├── app.py              # Flask web application
├── send_campaign.py    # SMTP campaign sender
├── database.py         # SQLite metrics layer
├── config.py           # Environment configuration
├── requirements.txt
├── .env.example
├── templates/          # HTML pages
├── static/css/         # Stylesheets
└── data/               # SQLite database (auto-created)
```

## SMTP Providers for Testing

- **Gmail** — enable 2FA, create an [App Password](https://myaccount.google.com/apppasswords)
- **Mailtrap** — sandbox inbox for safe testing (recommended for demos)
- **MailHog / Papercut** — local SMTP servers for offline labs

## License & Ethics

This project is for **educational and authorized security awareness training** only. Misuse for unauthorized phishing is illegal and unethical.
