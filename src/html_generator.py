from pathlib import Path


def generate_html(emails):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Substack Daily Roundup</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                line-height: 1.6;
                padding: 20px;
            }

            .card {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 20px;
            }

            h1 {
                margin-bottom: 30px;
            }

            h3 {
                margin: 8px 0;
            }

            .sender {
                color: #666;
                font-size: 14px;
            }

            .date {
                color: #999;
                font-size: 13px;
                margin-bottom: 10px;
            }

            a {
                text-decoration: none;
                color: blue;
            }
        </style>
    </head>

    <body>

    <h1>📬 Substack Daily Roundup</h1>
    """

    for email in emails:
        html += f"""
        <div class="card">
            <div class="sender">{email['sender']}</div>
            <h3>{email['subject']}</h3>
            <div class="date">{email['date']}</div>

            <a href="{email['url']}" target="_blank">
                Read →
            </a>
        </div>
        """

    html += """
    </body>
    </html>
    """

    Path("roundup.html").write_text(html, encoding="utf-8")