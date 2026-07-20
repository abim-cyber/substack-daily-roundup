from pathlib import Path


def create_section(title, emails):

    if not emails:
        return ""

    html = f"<h2>{title} ({len(emails)})</h2>"

    for email in emails:

        read_button = ""

        if email["url"]:
            read_button = (
                f'<a class="button" href="{email["url"]}" '
                f'target="_blank">Read →</a>'
            )

        html += f"""
        <div class="card">
            <div class="sender">{email["sender"]}</div>
            <h3>{email["subject"]}</h3>
            <div class="date">{email["date"]}</div>
            {read_button}
        </div>
        """

    return html


def generate_html(emails):

    articles = [e for e in emails if e["type"] == "article"]
    notes = [e for e in emails if e["type"] == "note"]
    live = [e for e in emails if e["type"] == "live"]
    notifications = [
        e for e in emails
        if e["type"] == "notification"
    ]

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Substack Daily Roundup</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin: auto;
    padding: 40px;
    background: #fafafa;
}}

h1 {{
    margin-bottom: 40px;
}}

h2 {{
    margin-top: 40px;
    border-bottom: 2px solid #ddd;
    padding-bottom: 10px;
}}

.card {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
}}

.sender {{
    color: gray;
    font-size: 14px;
}}

.date {{
    color: gray;
    margin: 15px 0;
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

<h1>📬 Substack Daily Roundup</h1>

{create_section("📚 Articles", articles)}

{create_section("💬 Notes", notes)}

{create_section("🔴 Live", live)}

{create_section("🔔 Notifications", notifications)}

</body>

</html>
"""

    Path("roundup.html").write_text(
        html,
        encoding="utf-8",
    )

    print("✅ roundup.html created")