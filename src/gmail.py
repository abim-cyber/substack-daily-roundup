import base64
import re
from urllib.parse import unquote

from googleapiclient.discovery import build


def find_html_part(payload):
    """Find the HTML part of an email."""
    if payload.get("mimeType") == "text/html":
        return payload

    for part in payload.get("parts", []):
        result = find_html_part(part)
        if result:
            return result

    return None


def extract_article_url(html):
    """Extract the best article URL from a Substack email."""

    matches = re.findall(r'https://[^"\']+', html)

    for url in matches:

        url = url.replace("&amp;", "&")

        # Direct article
        if "open.substack.com/pub/" in url:
            return url.split("?")[0]

        if ".substack.com/p/" in url:
            return url.split("?")[0]

        # Decode redirect links
        if "next=https" in url:
            try:
                real = url.split("next=")[1]
                real = real.split("&")[0]
                real = unquote(real)

                if ".substack.com/p/" in real:
                    return real

            except Exception:
                pass

    return ""


def get_substack_emails(creds):

    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        q="from:substack.com newer_than:7d",
        maxResults=10,
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        email = service.users().messages().get(
            userId="me",
            id=message["id"],
        ).execute()

        headers = email["payload"]["headers"]

        def get_header(name):
            return next(
                (
                    h["value"]
                    for h in headers
                    if h["name"] == name
                ),
                "",
            )

        html_part = find_html_part(email["payload"])

        article_url = ""

        if html_part:

            data = html_part["body"].get("data")

            if data:

                html = base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore",
                )

                article_url = extract_article_url(html)

        subject = get_header("Subject")

        email_type = "article"

        if "New thread" in subject:
            email_type = "note"

        elif "Live" in subject:
            email_type = "live"

        elif article_url == "":
            email_type = "notification"

        emails.append(
            {
                "subject": subject,
                "sender": get_header("From"),
                "date": get_header("Date"),
                "url": article_url,
                "type": email_type,
            }
        )

    return emails