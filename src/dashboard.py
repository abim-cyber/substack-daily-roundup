def choose_time_range():

    print("""
==============================
📬 Substack Creator Companion
==============================

TIME RANGE

1. Today
2. Yesterday
3. Last 7 Days
""")

    while True:

        choice = input("Choose: ").strip()

        if choice == "1":
            return "today", "Today"

        if choice == "2":
            return "yesterday", "Yesterday"

        if choice == "3":
            return "week", "Last 7 Days"

        print("Please choose 1, 2 or 3.\n")


def choose_view():

    print("""
VIEW

1. 📚 All Content
2. ✅ Unfinished Only
""")

    while True:

        choice = input("Choose: ").strip()

        if choice == "1":
            return "all"

        if choice == "2":
            return "unfinished"

        print("Please choose 1 or 2.\n")


def choose_creator(emails):

    creators = sorted(
        {
            email["sender"]
            .split("<")[0]
            .strip()
            .replace('"', "")
            for email in emails
        }
    )

    print("\nCREATOR\n")
    print("0. All Creators")

    for i, creator in enumerate(
        creators,
        start=1,
    ):
        print(f"{i}. {creator}")

    while True:

        choice = input("\nChoose: ").strip()

        if choice == "" or choice == "0":
            return None

        try:

            index = int(choice) - 1

            if 0 <= index < len(creators):
                return creators[index]

        except ValueError:
            pass

        print("Please choose a valid creator.\n")


def apply_filters(
    emails,
    view,
    creator,
    is_read,
):

    filtered = emails

    if view == "unfinished":

        filtered = [
            email
            for email in filtered
            if not (
                email["url"]
                and is_read(email["url"])
            )
        ]

    if creator:

        filtered = [
            email
            for email in filtered
            if creator in email["sender"]
        ]

    return filtered