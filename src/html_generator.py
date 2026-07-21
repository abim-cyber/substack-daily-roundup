from pathlib import Path

from read_tracker import is_read


APP_DIR = (
    Path.home()
    / "Documents"
    / "Substack Creator Companion"
)

APP_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_FILE = APP_DIR / "roundup.html"


def create_section(title, emails):

    if not emails:
        return ""

    html = f"<h2>{title} ({len(emails)})</h2>"

    for email in emails:

        status = ""

        if email["url"] and is_read(email["url"]):
            status = """
            <div class="finished">
                ✅ Finished
            </div>
            """

        button = ""

        if email["url"]:

            button_text = {
                "article": "📖 Read Article",
                "note": "💬 Open Note",
                "live": "🔴 Join Live",
                "notification": "Open",
            }.get(email["type"], "Open")

            button = (
                f'<a class="button" '
                f'href="{email["url"]}" '
                f'target="_blank">'
                f'{button_text}</a>'
            )

        html += f"""
        <div class="card">

            <div class="sender">
                {email["sender"]}
            </div>

            <h3>{email["subject"]}</h3>

            <div class="date">
                {email["date"]}
            </div>

            {status}

            {button}

        </div>
        """

    return html


def generate_html(emails, title="Last 7 Days"):

    articles = [
        e for e in emails
        if e["type"] == "article"
    ]

    notes = [
        e for e in emails
        if e["type"] == "note"
    ]

    live = [
        e for e in emails
        if e["type"] == "live"
    ]

    notifications = [
        e for e in emails
        if e["type"] == "notification"
    ]

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>Substack Creator Companion</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin:auto;
    padding:40px;
    background:#fafafa;
}}

h1 {{
    margin-bottom:10px;
}}

.subtitle {{
    color:gray;
    font-size:20px;
    margin-bottom:30px;
}}

.summary {{
    background:#f4f4f4;
    padding:15px;
    border-radius:10px;
    margin:25px 0;
    font-weight:bold;
}}

h2 {{
    margin-top:40px;
    border-bottom:2px solid #ddd;
    padding-bottom:10px;
}}

.card {{
    background:white;
    border-radius:12px;
    padding:20px;
    margin:20px 0;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}}

.sender {{
    color:gray;
    font-size:14px;
}}

.date {{
    color:gray;
    margin:15px 0;
}}

.finished {{
    color:green;
    font-weight:bold;
    margin:10px 0;
}}

.button {{
    display:inline-block;
    padding:10px 18px;
    background:#2563eb;
    color:white;
    text-decoration:none;
    border-radius:8px;
}}

.button:hover {{
    background:#1d4ed8;
}}

</style>

</head>

<body>

<h1>📬 Substack Creator Companion</h1>

<div class="subtitle">
Viewing:
<strong>{title}</strong>
</div>

<div class="summary">

📚 {len(articles)} Articles |
💬 {len(notes)} Notes |
🔴 {len(live)} Live |
🔔 {len(notifications)} Notifications

</div>

{create_section("📚 Articles", articles)}

{create_section("💬 Notes", notes)}

{create_section("🔴 Live", live)}

{create_section("🔔 Notifications", notifications)}

</body>

</html>
"""

    OUTPUT_FILE.write_text(
        html,
        encoding="utf-8",
    )

    print(f"✅ Dashboard created: {OUTPUT_FILE}")

    return OUTPUT_FILE