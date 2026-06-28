"""
Phishing Simulation Platform — Flask web application.

AUTHORIZED USE ONLY: Run this tool only in controlled lab environments with
explicit written consent from all participants. Never deploy against real users
without organizational approval.
"""

import secrets
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import config
import project_info
from database import (
    create_campaign,
    create_recipient,
    get_campaign_summary,
    get_recent_events,
    get_recipient_by_token,
    init_db,
    log_event,
)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
init_db()


@app.context_processor
def inject_project_info():
    return {
        "project": {
            "student_name": project_info.STUDENT_NAME,
            "roll_number": project_info.ROLL_NUMBER,
            "college_name": project_info.COLLEGE_NAME,
            "department": project_info.DEPARTMENT,
            "internship_organization": project_info.INTERNSHIP_ORGANIZATION,
            "guide_name": project_info.GUIDE_NAME,
            "academic_year": project_info.ACADEMIC_YEAR,
            "project_title": project_info.PROJECT_TITLE,
            "project_subtitle": project_info.PROJECT_SUBTITLE,
            "keywords": project_info.KEYWORDS,
        }
    }


def client_ip() -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_authenticated"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


@app.route("/demo")
def demo():
    """One-click demo — no email required."""
    campaign_id = create_campaign("Website Demo")
    token = secrets.token_urlsafe(16)
    create_recipient(campaign_id, "demo@training.local", token)
    return redirect(url_for("track_click", token=token))


@app.route("/t/<token>")
def track_click(token: str):
    recipient = get_recipient_by_token(token)
    if not recipient:
        abort(404)

    log_event(
        recipient_id=recipient["id"],
        event_type="link_clicked",
        ip_address=client_ip(),
        user_agent=request.headers.get("User-Agent"),
    )
    return redirect(url_for("landing_page", token=token))


@app.route("/verify/<token>", methods=["GET"])
def landing_page(token: str):
    recipient = get_recipient_by_token(token)
    if not recipient:
        abort(404)

    log_event(
        recipient_id=recipient["id"],
        event_type="landing_viewed",
        ip_address=client_ip(),
        user_agent=request.headers.get("User-Agent"),
    )
    return render_template(
        "landing.html",
        token=token,
        campaign_name=config.CAMPAIGN_NAME,
    )


@app.route("/verify/<token>", methods=["POST"])
def submit_credentials(token: str):
    """
    Log that a form was submitted. Passwords are NEVER stored — the field is
    discarded immediately after confirming submission occurred.
    """
    recipient = get_recipient_by_token(token)
    if not recipient:
        abort(404)

    username = (request.form.get("username") or "").strip()
    # Password is intentionally read and discarded — never logged or persisted.
    _ = request.form.get("password")

    log_event(
        recipient_id=recipient["id"],
        event_type="form_submitted",
        ip_address=client_ip(),
        user_agent=request.headers.get("User-Agent"),
        metadata=f"username_length={len(username)}" if username else "empty_username",
    )
    return redirect(url_for("microlearning", token=token))


@app.route("/learn/<token>")
def microlearning(token: str):
    recipient = get_recipient_by_token(token)
    if not recipient:
        abort(404)

    log_event(
        recipient_id=recipient["id"],
        event_type="training_viewed",
        ip_address=client_ip(),
        user_agent=request.headers.get("User-Agent"),
    )
    return render_template(
        "microlearning.html",
        real_domain="microsoft.com",
        fake_domain=request.host,
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session["admin_authenticated"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@require_admin
def admin_dashboard():
    campaigns = get_campaign_summary()
    events = get_recent_events()
    totals = {
        "recipients": sum(c["recipients"] or 0 for c in campaigns),
        "clicks": sum(c["clicks"] or 0 for c in campaigns),
        "submissions": sum(c["submissions"] or 0 for c in campaigns),
    }
    if totals["recipients"]:
        totals["click_rate"] = round(100 * totals["clicks"] / totals["recipients"], 1)
        totals["submit_rate"] = round(100 * totals["submissions"] / totals["recipients"], 1)
    else:
        totals["click_rate"] = 0
        totals["submit_rate"] = 0

    return render_template(
        "admin_dashboard.html",
        campaigns=campaigns,
        events=events,
        totals=totals,
    )


if __name__ == "__main__":
    init_db()
    print("\n  Phishing Simulation Platform")
    print("  ------------------------------")
    print("  Authorized training use only.\n")
    print(f"  App:   {config.BASE_URL}")
    print(f"  Admin: {config.BASE_URL}/admin\n")
    app.run(host=config.HOST, port=config.PORT, debug=True)
