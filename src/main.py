from auth import authenticate
from gmail import get_substack_emails
from html_generator import generate_html


def main():
    creds = authenticate()

    emails = get_substack_emails(creds)

    print(f"Found {len(emails)} Substack emails.")

    generate_html(emails)

    print("✅ roundup.html created")


if __name__ == "__main__":
    main()