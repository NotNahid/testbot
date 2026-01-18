import tkinter as tk
from tkinter import scrolledtext
import threading
# Import the function from the other file
from chatbot_logic import get_bot_response 

def send_message(event=None):
    msg = message_entry.get()
    if msg:
        # 1. Show User Message
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + msg + "\n")
        chat_history.config(state=tk.DISABLED)
        
        # 2. Clear Input
        message_entry.delete(0, tk.END)
        
        # 3. Get Bot Response
        # We run this directly. If your bot gets slow, we can add threading later.
        response = get_bot_response(msg)
        display_response(response)

def display_response(response):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bot: " + response + "\n\n")
    chat_history.yview(tk.END) # Auto-scroll to bottom
    chat_history.config(state=tk.DISABLED)

# --- GUI Setup ---
root = tk.Tk()
root.title("Final Year Project Chatbot")
root.geometry("500x600")

# Chat History Area
chat_history = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, font=("Segoe UI", 10))
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Input Area Frame
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.X)

# Entry Box
message_entry = tk.Entry(input_frame, font=("Segoe UI", 12))
message_entry.bind("<Return>", send_message) # Press Enter to send
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Send Button
send_button = tk.Button(input_frame, text="Send", command=send_message, bg="#e1e1e1", width=10)
send_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()
