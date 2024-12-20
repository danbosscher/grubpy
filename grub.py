import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def get_grub_entries():
    """Retrieve a list of current GRUB menu entries."""
    try:
        result = subprocess.run(["grep", "^menuentry", "/boot/grub/grub.cfg"], capture_output=True, text=True, check=True)
        entries = [line.split("'")[1] for line in result.stdout.splitlines()]
        return entries
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve GRUB entries: {e}")
        return []

def set_default_entry(entry):
    """Set the default GRUB menu entry."""
    try:
        with open("/etc/default/grub", "r") as file:
            lines = file.readlines()

        with open("/etc/default/grub", "w") as file:
            for line in lines:
                if line.startswith("GRUB_DEFAULT="):
                    file.write(f"GRUB_DEFAULT=\"{entry}\"\n")
                else:
                    file.write(line)

        subprocess.run(["sudo", "update-grub"], check=True)
        messagebox.showinfo("Success", f"Default entry set to: {entry}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set default entry: {e}")

def add_custom_entry(title, command):
    """Add a custom GRUB menu entry."""
    custom_entry = f"menuentry '{title}' {{\n    {command}\n}}\n"
    try:
        with open("/etc/grub.d/40_custom", "a") as file:
            file.write(custom_entry)
        subprocess.run(["sudo", "update-grub"], check=True)
        messagebox.showinfo("Success", f"Custom entry added: {title}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add custom entry: {e}")

def delete_entry(entry):
    """Delete an existing custom GRUB menu entry."""
    try:
        with open("/etc/grub.d/40_custom", "r") as file:
            lines = file.readlines()

        with open("/etc/grub.d/40_custom", "w") as file:
            skip = False
            for line in lines:
                if line.startswith(f"menuentry '{entry}'"):
                    skip = True
                if skip and line.strip() == "}":
                    skip = False
                    continue
                if not skip:
                    file.write(line)

        subprocess.run(["sudo", "update-grub"], check=True)
        messagebox.showinfo("Success", f"Entry deleted: {entry}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete entry: {e}")

# Initialize the GUI application
app = tk.Tk()
app.title("GRUB Entry Manager")
app.geometry("600x400")

# Dropdown to list GRUB entries
default_entry_var = tk.StringVar()
default_entry_var.set("Select an entry")
entries = get_grub_entries()

entry_dropdown = tk.OptionMenu(app, default_entry_var, *entries)
entry_dropdown.pack(pady=10)

def set_default_action():
    entry = default_entry_var.get()
    if entry == "Select an entry":
        messagebox.showerror("Error", "Please select an entry.")
    else:
        set_default_entry(entry)

def add_entry_action():
    title = title_entry.get()
    command = command_entry.get("1.0", tk.END).strip()
    if title and command:
        add_custom_entry(title, command)
    else:
        messagebox.showerror("Error", "Both title and command are required.")

def delete_entry_action():
    entry = default_entry_var.get()
    if entry == "Select an entry":
        messagebox.showerror("Error", "Please select an entry to delete.")
    else:
        delete_entry(entry)

# Buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Set Default", command=set_default_action).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete Entry", command=delete_entry_action).pack(side=tk.LEFT, padx=5)

title_label = tk.Label(app, text="Custom Entry Title")
title_label.pack()
title_entry = tk.Entry(app, width=50)
title_entry.pack()

command_label = tk.Label(app, text="Custom Entry Command")
command_label.pack()
command_entry = tk.Text(app, height=5, width=50)
command_entry.pack()

tk.Button(app, text="Add Custom Entry", command=add_entry_action).pack(pady=10)

app.mainloop()

