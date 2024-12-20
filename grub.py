import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
                    grub_default = line.split("=")[1].strip().strip('"')

                    # Handle numeric index
                    if grub_default.isdigit():
                        entries = get_grub_entries()
                        index = int(grub_default)
                        return entries[index] if index < len(entries) else None

                    # Handle submenu paths (e.g., "1>2")
                    if ">" in grub_default:
                        entries = get_grub_entries()
                        indices = list(map(int, grub_default.split(">")))
                        entry = entries[indices[0]] if indices[0] < len(entries) else None
                        return entry

                    # Handle direct match with entry names
                    return grub_default
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
app.geometry("500x300")
app.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TCombobox", font=("Arial", 12))

# Header label
header_label = ttk.Label(app, text="Select Default GRUB Entry", font=("Arial", 16, "bold"))
header_label.pack(pady=10)

# Dropdown to list GRUB entries
default_entry_var = tk.StringVar()
entries = get_grub_entries()
def entry_dropdown_update():
    current_default = get_current_default()
    if current_default and current_default in entries:
        default_entry_var.set(current_default)
    else:
        default_entry_var.set("Select an entry")

entry_dropdown = ttk.Combobox(app, textvariable=default_entry_var, values=entries, state="readonly")
entry_dropdown.pack(pady=10, padx=20, fill=tk.X)

entry_dropdown_update()

def set_default_action():
    entry = default_entry_var.get()
    if entry == "Select an entry":
        messagebox.showerror("Error", "Please select an entry.")
    else:
        set_default_entry(entry)

# Buttons
button_frame = tk.Frame(app, bg="#f0f0f0")
button_frame.pack(pady=20)

set_default_button = ttk.Button(button_frame, text="Set Default", command=set_default_action)
set_default_button.pack(pady=10)

app.mainloop()

