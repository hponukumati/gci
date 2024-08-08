import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

def save_settings(settings):
    with open('gesture_settings.json', 'w') as f:
        json.dump(settings, f)

def load_settings():
    if os.path.exists('gesture_settings.json'):
        with open('gesture_settings.json', 'r') as f:
            return json.load(f)
    return {str(i): '' for i in range(1, 6)}

def select_application(gesture_num):
    file_path = filedialog.askopenfilename()
    if file_path:
        app_paths[gesture_num].set(file_path)

def save_and_exit():
    settings = {str(i): app_paths[i].get() for i in range(1, 6)}
    save_settings(settings)
    messagebox.showinfo("Settings Saved", "Application settings have been saved.")
    root.destroy()

# Load existing settings
settings = load_settings()

# Create the main window
root = tk.Tk()
root.title("Gesture to Application Mapper")

app_paths = {i: tk.StringVar(value=settings[str(i)]) for i in range(1, 6)}

# Create UI elements
for i in range(1, 6):
    label = tk.Label(root, text=f"Gesture {i} (1 Finger = {i}):")
    label.grid(row=i, column=0, padx=10, pady=5, sticky='e')
    
    entry = tk.Entry(root, textvariable=app_paths[i], width=50)
    entry.grid(row=i, column=1, padx=10, pady=5)
    
    button = tk.Button(root, text="Select Application", command=lambda i=i: select_application(i))
    button.grid(row=i, column=2, padx=10, pady=5)

tk.Button(root, text="Save and Exit", command=save_and_exit).grid(row=6, column=1, pady=20)

root.mainloop()
