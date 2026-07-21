import base64
import re

from googleapiclient.discovery import build


def build_query(mode="today"):
    """
    Build Gmail search query.
    """

    queries = {
        "today": "from:substack.com newer_than:1d",
        "yesterday": "from:substack.com newer_than:2d older_than:1d",
        "week": "from:substack.com newer_than:7d",
    }

    return queries.get(
        mode,
        queries["week"],
    )


def find_html_part(payload):
    """
    Recursively find the HTML part of an email.
    """

    if payload.get("mimeType") == "text/html":
        return payload

    for part in payload.get("parts", []):

        result = find_html_part(part)

        if result:
            return result

    return None


def extract_url(html):
    """
    Extract the best URL from a Substack email.
    """

    matches = re.findall(
        r'https://[^"\']+',
        html,
    )

    for url in matches:

        url = url.replace("&amp;", "&")

        # Articles
        if "open.substack.com/pub/" in url:
            return url.split("?")[0]

        # Notes / Threads
        if "substack.com/chat/" in url:
            return url.split("?")[0]

        # Live streams
        if "open.substack.com/live-stream/" in url:
            return url.split("?")[0]

    return ""


def detect_email_type(subject, url):
    """
    Classify the email.
    """

    if "New thread" in subject:
        return "note"

    if "Live" in subject:
        return "live"

    if "open.substack.com/pub/" in url:
        return "article"

    return "notification"


def get_substack_emails(
    creds,
    mode="week",
):

    service = build(
        "gmail",
        "v1",
        credentials=creds,
    )

    results = service.users().messages().list(
        userId="me",
        q=build_query(mode),
        maxResults=10,
    ).execute()

    messages = results.get(
        "messages",
        [],
    )

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

        html_part = find_html_part(
            email["payload"]
        )

        url = ""

        if html_part:

            data = html_part["body"].get(
                "data"
            )

            if data:

                html = (
                    base64.urlsafe_b64decode(
                        data
                    )
                    .decode(
                        "utf-8",
                        errors="ignore",
                    )
                )

                url = extract_url(html)

        subject = get_header("Subject")

        emails.append(
            {
                "subject": subject,
                "sender": get_header("From"),
                "date": get_header("Date"),
                "url": url,
                "type": detect_email_type(
                    subject,
                    url,
                ),
            }
        )

    return emails