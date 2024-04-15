import os
import time
import threading
import keyboard
import pyperclip
import tkinter as tk
from tkinter import Text, Scrollbar
import customtkinter as ctk
from configure import SYSTEM_PROMPT
from openai import OpenAI

# Configure CustomTkinter
ctk.set_appearance_mode("Dark")  # Options: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Other themes: "green", "dark-blue"

# Initialize OpenAI client
API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

def update_scrollbar(text_widget, scrollbar):
    """Adjusts scrollbar visibility based on the text content."""
    text_widget.update_idletasks()
    scrollbar.pack(side='right', fill='y') if text_widget.yview()[1] < 1 else scrollbar.pack_forget()

def handle_gpt_response(text, text_widget, scrollbar):
    """Handles streaming responses from OpenAI's GPT model."""
    try:
        stream = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices:
                update_text_widget(text_widget, chunk.choices[0].delta.content, scrollbar)
    except Exception as e:
        update_text_widget(text_widget, str(e), scrollbar)

def update_text_widget(text_widget, message, scrollbar):
    """Updates the text widget with new messages and manages the scrollbar."""
    if message:
        try:
            text_widget.configure(state='normal')
            text_widget.insert(tk.END, message)
            text_widget.see(tk.END)
            text_widget.configure(state='disabled')
            update_scrollbar(text_widget, scrollbar)
        except tk.TclError:
            pass  # Ignore the error if the widget has been deleted

def capture_clipboard():
    """Captures text from the clipboard and triggers response handling."""
    keyboard.send('ctrl+c')
    time.sleep(0.5)  # Allow time for clipboard update
    text = pyperclip.paste()
    setup_gui(text)

def setup_gui(text):
    """Sets up the GUI elements and starts the application."""
    window = create_window()
    text_widget, scrollbar = create_text_widget(window)

    # Fade-in effect
    for i in range(11):
        alpha_value = i * 0.1
        window.attributes('-alpha', alpha_value)
        window.update()
        window.after(50)

    window.focus_force()  # Focus the window

    threading.Thread(target=handle_gpt_response, args=(text, text_widget, scrollbar), daemon=True).start()
    window.mainloop()

def create_window():
    """Creates and configures the main application window."""
    window = ctk.CTk()
    window.title("GPT-4 Response")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 600
    window_height = 400
    x_coordinate = screen_width - window_width - 10
    y_coordinate = screen_height - window_height - 50
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    window.attributes('-topmost', True)
    window.attributes('-alpha', 0)  # Set initial transparency to 0

    return window


def create_text_widget(window):
    """Creates the text widget and scrollbar within the window."""
    text_widget = Text(window, wrap='word', font=('Helvetica Neue', 12),
                       padx=10, pady=10, borderwidth=0, highlightthickness=0,
                       foreground='white', background='black', state='disabled')
    scrollbar = Scrollbar(window, command=text_widget.yview)
    text_widget['yscrollcommand'] = scrollbar.set
    text_widget.pack(padx=10, pady=10, fill='both', expand=True)
    return text_widget, scrollbar

keyboard.add_hotkey('ctrl+c+g', capture_clipboard)
keyboard.wait()
