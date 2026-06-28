"""
Send a mock phishing email for an authorized security awareness campaign.

Usage:
    python send_campaign.py --email test@example.com
    python send_campaign.py --email test@example.com --dry-run
"""

import argparse
import secrets
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
from database import create_campaign, create_recipient, init_db


def build_tracking_url(token: str) -> str:
    return f"{config.BASE_URL}/t/{token}"


def build_email_html(recipient_name: str, tracking_url: str) -> str:
    return f"""\
<!DOCTYPE html>
<html>
<body style="font-family:Segoe UI,Arial,sans-serif;color:#333;max-width:600px;margin:0 auto;">
  <div style="background:#0078d4;padding:16px 24px;">
    <span style="color:#fff;font-size:18px;font-weight:600;">Microsoft 365 Security</span>
  </div>
  <div style="padding:24px;border:1px solid #e0e0e0;border-top:none;">
    <p>Hello {recipient_name},</p>
    <p><strong>Action required within 24 hours:</strong> Unusual sign-in activity was detected
    on your organizational account. To prevent suspension, verify your credentials immediately.</p>
    <p style="text-align:center;margin:28px 0;">
      <a href="{tracking_url}"
         style="background:#0078d4;color:#fff;padding:12px 28px;text-decoration:none;border-radius:4px;font-weight:600;">
        Verify Account Now
      </a>
    </p>
    <p style="font-size:13px;color:#666;">
      If you did not request this, ignore this message.<br>
      Microsoft Corporation · One Microsoft Way · Redmond, WA
    </p>
    <hr style="border:none;border-top:1px solid #eee;margin:24px 0;">
    <p style="font-size:11px;color:#999;">
      [Authorized security awareness simulation — for training purposes only]
    </p>
  </div>
</body>
</html>
"""


def build_email_text(recipient_name: str, tracking_url: str) -> str:
    return f"""\
Hello {recipient_name},

Action required within 24 hours: Unusual sign-in activity was detected on your account.
Verify your credentials immediately:

{tracking_url}

[Authorized security awareness simulation — for training purposes only]
"""


def send_phishing_email(
    target_email: str,
    recipient_name: str = "Employee",
    campaign_name: str | None = None,
    dry_run: bool = False,
) -> dict:
    init_db()
    campaign_name = campaign_name or config.CAMPAIGN_NAME
    token = secrets.token_urlsafe(16)

    campaign_id = create_campaign(campaign_name)
    create_recipient(campaign_id, target_email, token)
    tracking_url = build_tracking_url(token)

    result = {
        "campaign_id": campaign_id,
        "token": token,
        "tracking_url": tracking_url,
        "target_email": target_email,
        "sent": False,
    }

    if dry_run:
        print("\n[DRY RUN] Email not sent.\n")
        print(f"  To:      {target_email}")
        print(f"  Subject: [Action Required] Verify your Microsoft 365 account")
        print(f"  Link:    {tracking_url}\n")
        return result

    if not config.SMTP_USERNAME or not config.SMTP_PASSWORD:
        raise SystemExit(
            "SMTP credentials missing. Copy .env.example to .env and configure SMTP settings."
        )

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Action Required] Verify your Microsoft 365 account"
    message["From"] = config.SMTP_FROM
    message["To"] = target_email

    text_part = MIMEText(build_email_text(recipient_name, tracking_url), "plain")
    html_part = MIMEText(build_email_html(recipient_name, tracking_url), "html")
    message.attach(text_part)
    message.attach(html_part)

    context = ssl.create_default_context()
    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_FROM, target_email, message.as_string())

    result["sent"] = True
    print(f"\nCampaign email sent to {target_email}")
    print(f"Tracking URL: {tracking_url}\n")
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Send an authorized phishing simulation email."
    )
    parser.add_argument("--email", required=True, help="Recipient test email address")
    parser.add_argument("--name", default="Employee", help="Recipient display name")
    parser.add_argument("--campaign", default=None, help="Campaign name")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate tracking link without sending email",
    )
    args = parser.parse_args()

    send_phishing_email(
        target_email=args.email,
        recipient_name=args.name,
        campaign_name=args.campaign,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
