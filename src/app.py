import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

from companion import generate_dashboard
from auth import authenticate
from gmail import get_substack_emails


# ------------------------
# Helpers
# ------------------------

def load_creators():

    try:

        creds = authenticate()

        emails = get_substack_emails(
            creds,
            "week",
        )

        creators = sorted(
            {
                email["sender"]
                .split("<")[0]
                .replace('"', "")
                .strip()
                for email in emails
            }
        )

        creator_combo["values"] = [
            "All Creators",
            *creators,
        ]

        creator_combo.current(0)

    except Exception:

        creator_combo["values"] = [
            "All Creators"
        ]

        creator_combo.current(0)


def generate():

    creator = creator_combo.get()

    if creator == "All Creators":
        creator = None

    try:

        count, html_file = generate_dashboard(
            mode=time_var.get(),
            view=view_var.get(),
            creator=creator,
        )

        webbrowser.open(
            html_file.as_uri()
        )

        messagebox.showinfo(
            "Success",
            f"Dashboard created!\n\n{count} items found.",
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e),
        )


# ------------------------
# Window
# ------------------------

root = tk.Tk()

root.title("📬 Substack Creator Companion")
root.geometry("520x560")
root.resizable(False, False)

root.lift()
root.attributes("-topmost", True)
root.after(
    200,
    lambda: root.attributes(
        "-topmost",
        False,
    ),
)

# ------------------------
# Header
# ------------------------

title = tk.Label(
    root,
    text="📬 Substack Creator Companion",
    font=("Helvetica", 20, "bold"),
)

title.pack(
    pady=(20, 5),
)

subtitle = tk.Label(
    root,
    text="Read your Substack inbox without opening Gmail",
    fg="gray",
)

subtitle.pack(
    pady=(0, 25),
)

# ------------------------
# Time Range
# ------------------------

frame1 = ttk.LabelFrame(
    root,
    text="Time Range",
    padding=15,
)

frame1.pack(
    fill="x",
    padx=20,
    pady=10,
)

time_var = tk.StringVar(
    value="today",
)

ttk.Radiobutton(
    frame1,
    text="Today",
    variable=time_var,
    value="today",
).pack(anchor="w")

ttk.Radiobutton(
    frame1,
    text="Yesterday",
    variable=time_var,
    value="yesterday",
).pack(anchor="w")

ttk.Radiobutton(
    frame1,
    text="Last 7 Days",
    variable=time_var,
    value="week",
).pack(anchor="w")

# ------------------------
# View
# ------------------------

frame2 = ttk.LabelFrame(
    root,
    text="View",
    padding=15,
)

frame2.pack(
    fill="x",
    padx=20,
    pady=10,
)

view_var = tk.StringVar(
    value="unfinished",
)

ttk.Radiobutton(
    frame2,
    text="Unfinished Only",
    variable=view_var,
    value="unfinished",
).pack(anchor="w")

ttk.Radiobutton(
    frame2,
    text="All Content",
    variable=view_var,
    value="all",
).pack(anchor="w")

# ------------------------
# Creator
# ------------------------

frame3 = ttk.LabelFrame(
    root,
    text="Creator",
    padding=15,
)

frame3.pack(
    fill="x",
    padx=20,
    pady=10,
)

creator_combo = ttk.Combobox(
    frame3,
    state="readonly",
)

creator_combo.pack(
    fill="x",
)

# ------------------------
# Generate Button
# ------------------------

generate_button = ttk.Button(
    root,
    text="🚀 Generate Dashboard",
    command=generate,
)

generate_button.pack(
    pady=(20, 30),
)

load_creators()

root.mainloop()