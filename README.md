# 📬 Substack Creator Companion

A lightweight Python application that turns Substack emails into a clean dashboard.

Instead of browsing Gmail, this tool organizes your Substack activity into one HTML page with quick links to articles, notes, live sessions and notifications.

---

## Features

- Gmail OAuth authentication
- Today / Yesterday / Last 7 Days filters
- Creator filter
- Read tracking (Mark as Finished)
- HTML dashboard
- Article detection
- Note detection
- Live session detection
- Notification detection

---

## Tech Stack

- Python
- Gmail API
- Google OAuth
- HTML
- JSON

---

## Project Structure

```
src/
├── auth.py
├── dashboard.py
├── gmail.py
├── html_generator.py
├── main.py
└── read_tracker.py
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the following files in the project root:

- `credentials.json`
- `token.json` (generated after first login)

Run:

```bash
python3 src/main.py
```

---

## Notes

- This repository is maintained as a private working project.
- Sensitive files are excluded using `.gitignore`.
- Future public release, if any, will be as a web application.

---

## Version

Current Version: **v1.0**