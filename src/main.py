from email.utils import parsedate_to_datetime

from auth import authenticate
from dashboard import (
    apply_filters,
    choose_creator,
    choose_time_range,
    choose_view,
)
from gmail import get_substack_emails
from html_generator import generate_html
from read_tracker import is_read, mark_read


def main():

    mode, title = choose_time_range()

    view = choose_view()

    creds = authenticate()

    emails = get_substack_emails(
        creds,
        mode,
    )

    emails.sort(
        key=lambda e: parsedate_to_datetime(e["date"]),
        reverse=True,
    )

    creator = choose_creator(emails)

    emails = apply_filters(
        emails,
        view,
        creator,
        is_read,
    )

    print(f"\nFound {len(emails)} matching emails.\n")

    for i, email in enumerate(
        emails,
        start=1,
    ):
        print(f"{i}. {email['subject']}")

    selection = input(
        "\nMark item as Finished (Enter number or press Enter): "
    ).strip()

    if selection:

        try:

            index = int(selection) - 1

            if (
                0 <= index < len(emails)
                and emails[index]["url"]
            ):

                mark_read(
                    emails[index]["url"]
                )

                print("✅ Marked as Finished")

        except ValueError:
            print("Invalid selection.")

    subtitle = title

    if view == "unfinished":
        subtitle += " • Unfinished"
    else:
        subtitle += " • All Content"

    if creator:
        subtitle += f" • {creator}"

    generate_html(
        emails,
        subtitle,
    )


if __name__ == "__main__":
    main()