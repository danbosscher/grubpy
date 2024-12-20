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

def get_current_default():
    """Retrieve the current default GRUB entry."""
    try:
        with open("/etc/default/grub", "r") as file:
            for line in file:
                if line.startswith("GRUB_DEFAULT="):
                    return line.split("=")[1].strip().strip('"')
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve current default entry: {e}")
        return None

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

# Initialize the GUI application
app = tk.Tk()
app.title("GRUB Default Selector")
app.geometry("400x200")

# Dropdown to list GRUB entries
default_entry_var = tk.StringVar()
entries = get_grub_entries()
current_default = get_current_default()
if current_default and current_default in entries:
    default_entry_var.set(current_default)
else:
    default_entry_var.set("Select an entry")

entry_dropdown = tk.OptionMenu(app, default_entry_var, *entries)
entry_dropdown.pack(pady=10)

def set_default_action():
    entry = default_entry_var.get()
    if entry == "Select an entry":
        messagebox.showerror("Error", "Please select an entry.")
    else:
        set_default_entry(entry)

# Buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Set Default", command=set_default_action).pack(padx=5)

app.mainloop()

