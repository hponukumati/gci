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
    frame = tk.Frame(root)
    frame.pack(fill='x', padx=10, pady=5)

    entry = tk.Entry(frame, textvariable=app_paths[i], width=0)
    entry.pack(side='left', padx=5)

    button = tk.Button(frame, text=f"Select Application for Gesture {i}", command=lambda i=i: select_application(i))
    button.pack(side='left', padx=5)

    frame.pack(anchor='center')  # Center the frame

# Center the Save and Exit button
save_button = tk.Button(root, text="Save and Exit", command=save_and_exit)
save_button.pack(pady=20)
save_button.pack(anchor='center')

root.mainloop()
