import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def load_grub_config():
    """Load the GRUB configuration file."""
    try:
        with open("/etc/default/grub", "r") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load GRUB configuration: {e}")
        return ""

def save_grub_config(content):
    """Save changes to the GRUB configuration file."""
    try:
        with open("/etc/default/grub", "w") as file:
            file.write(content)
        messagebox.showinfo("Success", "GRUB configuration saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save GRUB configuration: {e}")

def update_grub():
    """Run the GRUB update command."""
    try:
        result = subprocess.run(["sudo", "update-grub"], capture_output=True, text=True, check=True)
        messagebox.showinfo("Update GRUB", f"GRUB updated successfully!\n\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to update GRUB:\n{e.stderr}")

def open_file():
    """Open GRUB configuration file in a text editor widget."""
    content = load_grub_config()
    text_editor.delete("1.0", tk.END)
    text_editor.insert("1.0", content)

def save_file():
    """Save the edited GRUB configuration file."""
    content = text_editor.get("1.0", tk.END)
    save_grub_config(content)

# Initialize the GUI application
app = tk.Tk()
app.title("GRUB Configuration Manager")
app.geometry("800x600")

# Create a text editor
text_editor = ScrolledText(app, wrap=tk.WORD, font=("Courier", 12))
text_editor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Create buttons
button_frame = tk.Frame(app)
button_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Button(button_frame, text="Load Config", command=open_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Save Config", command=save_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update GRUB", command=update_grub).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Exit", command=app.quit).pack(side=tk.RIGHT, padx=5)

# Load initial GRUB configuration
open_file()

# Run the application
app.mainloop()

