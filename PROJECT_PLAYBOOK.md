# 📬 Substack Creator Companion - Project Playbook
> Status: Released
>
> Version: 1.0
>
> Release Date: July 2026

## Project Vision

Substack Creator Companion is a lightweight desktop companion that helps me review my Substack activity from Gmail in one clean dashboard.

The goal is not to replace Substack. It is to make it easier to review articles, notes, live sessions and notifications from one place.

---

## Repository Policy

Repository Visibility: Private

This repository is my working project.

It will remain private while I continue improving it.

If I decide to share it publicly, I will publish it as a web application where users authenticate using their own Gmail credentials.

---

## Tech Stack

- Python
- Gmail API
- Google OAuth
- BeautifulSoup
- HTML
- CSS
- JSON

---

## Project Structure

src/
- auth.py
- gmail.py
- dashboard.py
- html_generator.py
- read_tracker.py
- main.py

---

## Version 1 Features

- Gmail Authentication
- Today / Yesterday / Last 7 Days
- Creator Filter
- Read Tracking
- HTML Dashboard
- Article Detection
- Note Detection
- Live Detection
- Notification Detection

---

## Design Decisions

- HTML dashboard instead of Streamlit
- JSON for read tracking
- Manual "Mark as Finished"
- Private GitHub repository
- Small focused Python modules

---

## Lessons Learned

- Build one feature at a time.
- Test after every change.
- Finish Version 1 before adding new ideas.
- Keep the code simple.

---

## Future Ideas

- Search
- Favorites
- AI summaries
- Dark mode

---

## Version History

### v1.0

Initial release of Substack Creator Companion.