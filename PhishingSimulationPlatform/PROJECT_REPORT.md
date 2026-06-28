# PROJECT REPORT

---

## PhishGuard: Phishing Simulation & Security Awareness Platform

**A Cybersecurity Internship Project**

---

| Field | Details |
|-------|---------|
| **Submitted By** | Your Full Name |
| **Roll / Enrollment No.** | Your Roll Number |
| **Department** | Computer Science / Cyber Security |
| **College / University** | Your College Name |
| **Internship Organization** | Organization Name |
| **Project Guide** | Guide Name |
| **Academic Year** | 2025–2026 |

---

## Certificate of Originality

I hereby declare that this project titled **"PhishGuard: Phishing Simulation & Security Awareness Platform"** is my original work carried out during my cybersecurity internship. This project is intended for **authorized security awareness training only** and does not store real user passwords.

**Signature:** ___________________  
**Date:** ___________________

---

## Abstract

Phishing attacks remain the most common initial access vector in cybersecurity breaches worldwide. Organizations need practical tools to train employees and measure security awareness without causing real harm. This project presents **PhishGuard**, a web-based phishing simulation platform built using Python and Flask. The system sends mock phishing emails, hosts a realistic fake login page, logs engagement metrics safely, and delivers post-click micro-learning to educate users on missed indicators such as mismatched domains and urgent language. Passwords are never stored, ensuring ethical and privacy-conscious operation. The platform includes an admin dashboard for campaign analytics including click rate and submission rate. This project demonstrates skills in social engineering mechanics, web development, and security metrics collection.

**Keywords:** Phishing Simulation, Security Awareness, Social Engineering, Flask, Cybersecurity Training

---

## 1. Introduction

### 1.1 Background

Cyber attackers frequently use phishing emails to trick users into clicking malicious links or entering credentials on fake websites. According to industry reports, a large percentage of successful breaches begin with a phishing email. Security awareness training helps users recognize these attacks before they cause damage.

### 1.2 Problem Statement

Traditional cybersecurity training often uses slides and videos, which do not simulate the real pressure and deception of a phishing attack. There is a need for a **controlled simulation environment** that:

- Replicates realistic phishing scenarios
- Tracks user response safely
- Provides immediate feedback and education
- Generates metrics for security teams

### 1.3 Objectives

1. Build a dummy login landing page that simulates a credential-harvesting attack
2. Send mock phishing emails using Python `smtplib`
3. Log click and submission metrics **without storing passwords**
4. Display a micro-learning page explaining phishing indicators
5. Provide an admin dashboard for campaign analytics

### 1.4 Scope

This project is limited to **authorized lab and training environments**. It is not designed for unauthorized use against real victims. All pages include training disclaimers.

---

## 2. Literature Review / Related Concepts

| Concept | Description |
|---------|-------------|
| **Phishing** | Fraudulent attempt to obtain sensitive information by disguising as a trustworthy entity |
| **Social Engineering** | Manipulation of people to perform actions or divulge confidential information |
| **Spear Phishing** | Targeted phishing aimed at specific individuals or organizations |
| **Security Awareness Training** | Educational programs to help users identify and report threats |
| **Phishing Simulation** | Controlled exercises that test and improve user awareness |

Commercial tools such as KnowBe4 and GoPhish offer similar capabilities. This project implements a lightweight, educational version using open-source Python technologies suitable for internship demonstration.

---

## 3. System Design

### 3.1 Architecture

```
send_campaign.py  ──►  SMTP Email with tracking link (/t/token)
                              │
                              ▼
                         Flask Web App (app.py)
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   Link Clicked         Landing Page         Micro-Learning
   (metric logged)      (fake login)         (education page)
                              │
                        Form Submitted
                   (password NOT stored)
                              ▼
                    SQLite Database (metrics.db)
                              ▼
                      Admin Dashboard
```

### 3.2 Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask |
| Database | SQLite |
| Email | smtplib (SMTP) |
| Frontend | HTML5, CSS3, Jinja2 templates |
| Configuration | python-dotenv |

### 3.3 Modules

| Module | File | Purpose |
|--------|------|---------|
| Web Application | `app.py` | Routes, tracking, admin dashboard |
| Email Campaign | `send_campaign.py` | Send mock phishing emails |
| Database Layer | `database.py` | SQLite metrics storage |
| Configuration | `config.py` | Environment settings |
| Templates | `templates/` | Web pages (landing, learning, admin) |

### 3.4 Database Schema

- **campaigns** — Campaign name and creation date
- **recipients** — Hashed email identifier and unique tracking token
- **events** — Event type, timestamp, IP, user agent (no passwords)

### 3.5 Event Types

| Event | Description |
|-------|-------------|
| `link_clicked` | User clicked email tracking link |
| `landing_viewed` | Fake login page displayed |
| `form_submitted` | User submitted login form (password discarded) |
| `training_viewed` | Micro-learning page viewed |

---

## 4. Implementation

### 4.1 Fake Login Page

A Microsoft-style login page is served at `/verify/<token>`. It mimics common phishing targets to demonstrate how convincing fake pages can appear.

### 4.2 Email Campaign

The `send_campaign.py` script generates a unique token per recipient, embeds it in an HTML email, and sends via SMTP. A dry-run mode allows testing without sending email.

### 4.3 Safe Metric Collection

When a user submits the login form:

- The password field is read and **immediately discarded**
- Only `form_submitted` event is logged with username length metadata
- Recipient emails are stored as SHA-256 hash prefixes

### 4.4 Micro-Learning Module

After form submission, users are redirected to `/learn/<token>` which explains:

1. Mismatched domain names
2. Urgent or threatening language
3. Generic greetings
4. Unexpected credential requests
5. Spoofed sender display names

### 4.5 Admin Dashboard

Authenticated admins can view:

- Total recipients, clicks, submissions
- Click rate and submission rate (%)
- Campaign list and recent event timeline

---

## 5. Security & Ethics

### 5.1 Ethical Considerations

- Used only with **explicit consent** from all participants
- Clear disclaimers on email, landing page, and training page
- No real credential harvesting or password storage
- Suitable for internship demonstration and awareness labs only

### 5.2 Security Measures

- Unique cryptographic tokens per recipient
- Hashed recipient identifiers
- Admin dashboard protected by login
- No password persistence in code or database

### 5.3 Legal Notice

Unauthorized phishing is illegal in most jurisdictions. This tool must only be deployed in controlled training environments with organizational approval.

---

## 6. Testing

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Start web server | Site loads at localhost:5000 | Pass |
| Click Try Demo | Fake login page appears | Pass |
| Submit dummy credentials | Redirect to micro-learning | Pass |
| Check admin dashboard | Events logged, no passwords stored | Pass |
| Dry-run email script | Tracking URL generated | Pass |

---

## 7. Results & Discussion

The PhishGuard platform successfully demonstrates the full phishing attack chain in a safe environment:

1. **Email delivery** — Realistic urgency-based messaging
2. **User engagement** — Trackable click and submission funnel
3. **Immediate remediation** — Micro-learning reduces repeat mistakes
4. **Metrics** — Quantifiable awareness data for reporting

The admin dashboard enables calculation of **click rate** and **submission rate**, key KPIs used in enterprise security awareness programs.

---

## 8. Conclusion

This project fulfills the internship objective of building a practical cybersecurity tool addressing real-world phishing threats. It combines web development, email mechanics, database design, and security ethics into a single demonstrable platform. Future enhancements could include multi-template campaigns, PDF reports, and integration with LDAP for enterprise deployment.

---

## 9. References

1. Verizon Data Breach Investigations Report — Phishing statistics  
2. OWASP — Social Engineering awareness guidelines  
3. Flask Documentation — https://flask.palletsprojects.com/  
4. Python smtplib Documentation — https://docs.python.org/3/library/smtplib.html  
5. NIST Cybersecurity Framework — Awareness and Training  

---

## 10. Appendix

### A. How to Run

```powershell
cd PhishingSimulationPlatform
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

### B. Admin Credentials (Default)

- Username: `admin`
- Password: `change-me`

### C. Screenshot Placeholders

*(Insert screenshots here when converting to PDF)*

1. Homepage  
2. Fake login page  
3. Micro-learning page  
4. Admin dashboard  

---

**End of Report**
