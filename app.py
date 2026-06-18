import os
import re
from html import escape

import boto3
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
)

ses = None
if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
    ses = boto3.client(
        "ses",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

LOGO_URL = "https://thefourseaonpainting.s3.us-east-1.amazonaws.com/logo-white.png"

PROJECTS = [
    {"id": 1, "title": "Interior Painting", "category": "Interior", "location": "Fairfax, VA", "before": "/static/images/gallery/b2.jpeg", "after": "/static/images/gallery/b1.jpeg"},
    {"id": 2, "title": "Exterior Painting", "category": "Exterior", "location": "Burke, VA", "before": "/static/images/gallery/b4.jpeg", "after": "/static/images/gallery/b3.jpeg"},
    {"id": 3, "title": "Home Renovation", "category": "Interior", "location": "Springfield, VA", "before": "/static/images/gallery/b6.jpeg", "after": "/static/images/gallery/b5.jpeg"},
    {"id": 4, "title": "Exterior Refresh", "category": "Exterior", "location": "Alexandria, VA", "before": "/static/images/gallery/b8.jpeg", "after": "/static/images/gallery/b7.jpeg"},
    {"id": 5, "title": "Room Transformation", "category": "Interior", "location": "McLean, VA", "before": "/static/images/gallery/b10.jpeg", "after": "/static/images/gallery/b9.jpeg"},
    {"id": 6, "title": "Full Home Repaint", "category": "Exterior", "location": "Woodbridge, VA", "before": "/static/images/gallery/b12.jpeg", "after": "/static/images/gallery/b11.jpeg"},
]


def _first_name(full_name: str) -> str:
    parts = full_name.strip().split()
    return parts[0] if parts else "there"


def build_owner_email(data: dict) -> str:
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip() or "Not provided"
    message = data.get("message", "").strip()
    first = _first_name(name)

    return f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background-color:#e8eef4;font-family:Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#e8eef4;font-family:Arial,sans-serif;">
    <tr>
      <td align="center" style="padding:24px 16px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#ffffff;">
          <tr>
            <td align="center" style="background-color:#0a1628;padding:24px 32px;">
              <img src="{LOGO_URL}" alt="The Four Season Painting" height="72" style="display:block;height:72px;border:0;margin:0 auto;">
            </td>
          </tr>
          <tr>
            <td style="background-color:#5bb8f5;height:4px;line-height:4px;font-size:4px;">&nbsp;</td>
          </tr>
          <tr>
            <td style="background-color:#ffffff;padding:32px 32px 8px;font-family:Arial,sans-serif;">
              <h1 style="margin:0 0 8px;color:#0a1628;font-size:22px;font-weight:bold;font-family:Arial,sans-serif;">New Quote Request</h1>
              <p style="margin:0;color:#666666;font-size:14px;font-family:Arial,sans-serif;">A visitor submitted the contact form on your website.</p>
            </td>
          </tr>
          <tr>
            <td style="padding:8px 32px 0;font-family:Arial,sans-serif;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="padding:16px 0;border-bottom:1px solid #e5e7eb;">
                    <p style="margin:0 0 4px;color:#999999;font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:1px;font-family:Arial,sans-serif;">Name</p>
                    <p style="margin:0;color:#0a1628;font-size:15px;font-family:Arial,sans-serif;">{escape(name)}</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 0;border-bottom:1px solid #e5e7eb;">
                    <p style="margin:0 0 4px;color:#999999;font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:1px;font-family:Arial,sans-serif;">Email</p>
                    <p style="margin:0;font-size:15px;font-family:Arial,sans-serif;">
                      <a href="mailto:{escape(email)}" style="color:#5bb8f5;text-decoration:none;font-family:Arial,sans-serif;">{escape(email)}</a>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 0;border-bottom:1px solid #e5e7eb;">
                    <p style="margin:0 0 4px;color:#999999;font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:1px;font-family:Arial,sans-serif;">Phone</p>
                    <p style="margin:0;color:#0a1628;font-size:15px;font-family:Arial,sans-serif;">{escape(phone)}</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 0;border-bottom:1px solid #e5e7eb;">
                    <p style="margin:0 0 4px;color:#999999;font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:1px;font-family:Arial,sans-serif;">Message</p>
                    <p style="margin:0;color:#0a1628;font-size:15px;line-height:1.5;font-family:Arial,sans-serif;">{escape(message)}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:24px 32px 32px;font-family:Arial,sans-serif;">
              <a href="mailto:{escape(email)}" style="display:inline-block;background-color:#0a1628;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:50px;font-weight:bold;font-size:14px;font-family:Arial,sans-serif;">Reply to {escape(first)}</a>
            </td>
          </tr>
          <tr>
            <td style="background-color:#f1f5f9;padding:20px 32px;text-align:center;font-family:Arial,sans-serif;">
              <p style="margin:0;color:#999999;font-size:12px;font-family:Arial,sans-serif;">Sent via the contact form on thefourseasonpainting.com</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_client_email(data: dict) -> str:
    name = data.get("name", "").strip()
    first = _first_name(name)

    return f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background-color:#e8eef4;font-family:Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#e8eef4;font-family:Arial,sans-serif;">
    <tr>
      <td align="center" style="padding:24px 16px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#ffffff;">
          <tr>
            <td align="center" style="background-color:#0a1628;padding:24px 32px;">
              <img src="{LOGO_URL}" alt="The Four Season Painting" height="72" style="display:block;height:72px;border:0;margin:0 auto;">
            </td>
          </tr>
          <tr>
            <td style="background-color:#5bb8f5;height:4px;line-height:4px;font-size:4px;">&nbsp;</td>
          </tr>
          <tr>
            <td style="background-color:#ffffff;padding:32px;font-family:Arial,sans-serif;">
              <h1 style="margin:0 0 16px;color:#0a1628;font-size:22px;font-weight:bold;font-family:Arial,sans-serif;">Thanks, {escape(first)}! We got your message.</h1>
              <p style="margin:0 0 28px;color:#666666;font-size:15px;line-height:1.6;font-family:Arial,sans-serif;">We appreciate you reaching out to The Four Season Painting. A member of our team will get back to you within 24 hours.</p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="font-family:Arial,sans-serif;">
                    <a href="https://thefourseasonpainting.com/#gallery" style="display:inline-block;background-color:#0a1628;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:50px;font-weight:bold;font-size:14px;font-family:Arial,sans-serif;">View Our Work</a>
                  </td>
                  <td style="padding-left:12px;font-family:Arial,sans-serif;">
                    <a href="tel:+17034771631" style="display:inline-block;background-color:#ffffff;color:#0a1628;text-decoration:none;padding:11px 24px;border-radius:50px;font-weight:bold;font-size:14px;border:2px solid #0a1628;font-family:Arial,sans-serif;">(703) 477-1631</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#f1f5f9;padding:20px 32px;text-align:center;font-family:Arial,sans-serif;">
              <p style="margin:0 0 8px;color:#666666;font-size:13px;font-weight:bold;font-family:Arial,sans-serif;">The Four Season Painting · Northern Virginia</p>
              <p style="margin:0;color:#999999;font-size:11px;font-family:Arial,sans-serif;">You're receiving this email because you submitted the contact form on our website.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


EMAIL_FORMAT_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
URL_RE = re.compile(r"https?://", re.IGNORECASE)
INJECTION_RE = re.compile(
    r"javascript:|data:|vbscript:|onload\s*=|onerror\s*=",
    re.IGNORECASE,
)
SQL_RE = re.compile(
    r"'\s*or|;[\s]*drop|union[\s]+select|--",
    re.IGNORECASE,
)
SPAM_WORDS_RE = re.compile(
    r"casino|viagra|cryptocurrency|bitcoin|forex|loan offer|click here|free money|make money fast",
    re.IGNORECASE,
)


def validate_contact_input(data: dict) -> bool:
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    for field in (name, email, phone, message):
        if not field:
            continue
        if "<" in field or ">" in field:
            return False
        if INJECTION_RE.search(field):
            return False
        if SQL_RE.search(field):
            return False
        if SPAM_WORDS_RE.search(field):
            return False

    email_lower = email.lower()
    if any(char in email for char in ("\n", "\r")) or "%0a" in email_lower or "%0d" in email_lower:
        return False

    if not EMAIL_FORMAT_RE.match(email):
        return False

    if URL_RE.search(name):
        return False

    if len(message) < 10 or len(message) > 3000:
        return False

    if len(URL_RE.findall(message)) > 3:
        return False

    return True


@app.route("/")
def index():
    return render_template(
        "index.html",
        projects=PROJECTS,
        elfsight_app_id=os.getenv("ELFSIGHT_APP_ID"),
    )


@app.route("/sitemap.xml")
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://thefourseasonpainting.com/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
</urlset>"""
    return Response(xml, mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    txt = """User-agent: *
Allow: /
Sitemap: https://thefourseasonpainting.com/sitemap.xml"""
    return Response(txt, mimetype="text/plain")


@app.route("/contact", methods=["POST"])
@limiter.limit("5 per minute")
def contact():
    data = request.get_json(silent=True) or {}

    if not data.get("name") or not data.get("email") or not data.get("message"):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    if not validate_contact_input(data):
        return jsonify({"success": False, "error": "Message could not be sent."}), 400

    if not ses:
        return jsonify({"success": False, "error": "Email service is not configured."}), 503

    from_email = os.getenv("FROM_EMAIL")
    contact_email = os.getenv("CONTACT_EMAIL")

    if not from_email or not contact_email:
        return jsonify({"success": False, "error": "Email service is not configured."}), 503

    name = data.get("name", "").strip()
    submitter_email = data.get("email", "").strip()

    try:
        ses.send_email(
            Source=os.getenv("FROM_EMAIL"),
            Destination={"ToAddresses": [contact_email]},
            ReplyToAddresses=[submitter_email],
            Message={
                "Subject": {"Data": f"New Quote Request — {name}"},
                "Body": {"Html": {"Data": build_owner_email(data)}},
            },
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    try:
        ses.send_email(
            Source=os.getenv("FROM_EMAIL"),
            Destination={"ToAddresses": [submitter_email]},
            Message={
                "Subject": {"Data": "We received your message — The Four Season Painting"},
                "Body": {"Html": {"Data": build_client_email(data)}},
            },
        )
    except Exception:
        pass

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
