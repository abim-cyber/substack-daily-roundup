from email.utils import parsedate_to_datetime

from auth import authenticate
from dashboard import apply_filters
from gmail import get_substack_emails
from html_generator import generate_html
from read_tracker import is_read


def generate_dashboard(
    mode,
    view,
    creator=None,
):
    """
    Generate the dashboard and return
    (number_of_items, html_path)
    """

    creds = authenticate()

    emails = get_substack_emails(
        creds,
        mode,
    )

    emails.sort(
        key=lambda e: parsedate_to_datetime(e["date"]),
        reverse=True,
    )

    emails = apply_filters(
        emails,
        view,
        creator,
        is_read,
    )

    if mode == "today":
        subtitle = "Today"

    elif mode == "yesterday":
        subtitle = "Yesterday"

    else:
        subtitle = "Last 7 Days"

    if view == "unfinished":
        subtitle += " • Unfinished"
    else:
        subtitle += " • All Content"

    if creator:
        subtitle += f" • {creator}"

    html_path = generate_html(
        emails,
        subtitle,
    )

    return len(emails), html_path