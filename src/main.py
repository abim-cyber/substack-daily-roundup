from auth import authenticate
from gmail import get_substack_emails
from html_generator import generate_html
from email.utils import parsedate_to_datetime
from read_tracker import mark_read


print("""
==============================
📬 Substack Creator Companion
==============================

Choose what to load

1. Today
2. Yesterday
3. Last 7 Days
""")

choice = input("Choice: ").strip()

mode = "week"
title = "Last 7 Days"

if choice == "1":
    mode = "today"
    title = "Today"

elif choice == "2":
    mode = "yesterday"
    title = "Yesterday"

elif choice == "3":
    mode = "week"
    title = "Last 7 Days"


def main():

    creds = authenticate()

    emails = get_substack_emails(
        creds,
        mode,
    )

    emails.sort(
        key=lambda e: parsedate_to_datetime(e["date"]),
        reverse=True,
    )

    print(f"\nFound {len(emails)} Substack emails.\n")

    for i, email in enumerate(emails, start=1):

        print(f"{i}. {email['subject']}")

    selection = input(
        "\nEnter number to mark as Finished "
        "(Press Enter to skip): "
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

    generate_html(
        emails,
        title,
    )


if __name__ == "__main__":
    main()