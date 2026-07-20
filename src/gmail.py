import base64
import re

from googleapiclient.discovery import build


def find_html_part(payload):
    """Recursively find the HTML part of an email."""
    if payload.get("mimeType") == "text/html":
        return payload

    for part in payload.get("parts", []):
        result = find_html_part(part)
        if result:
            return result

    return None


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
                (h["value"] for h in headers if h["name"] == name),
                "",
            )

        html_part = find_html_part(email["payload"])

        article_url = ""

        if html_part:
            data = html_part["body"].get("data")

            if data:
                html = base64.urlsafe_b64decode(data).decode(
                    "utf-8",
                    errors="ignore",
                )

                matches = re.findall(r'https://[^"]+', html)

                for match in matches:
                    if "substack.com" in match:
                        article_url = match
                        break

        emails.append(
            {
                "subject": get_header("Subject"),
                "sender": get_header("From"),
                "date": get_header("Date"),
                "url": article_url,
            }
        )

    return emails