import json
from pathlib import Path


FILE_NAME = "read_status.json"


def load_read_status():
    """
    Load read articles/notes from disk.
    """

    path = Path(FILE_NAME)

    if not path.exists():
        return {}

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        return {}


def save_read_status(status):
    """
    Save read status.
    """

    Path(FILE_NAME).write_text(
        json.dumps(
            status,
            indent=4,
        ),
        encoding="utf-8",
    )


def is_read(url):

    if not url:
        return False

    status = load_read_status()

    return status.get(url, False)


def mark_read(url):

    if not url:
        return

    status = load_read_status()

    status[url] = True

    save_read_status(status)