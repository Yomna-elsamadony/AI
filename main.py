import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import json
import os
import pygame

pygame.mixer.init()

SOUND_FILE = 'F:\Files\Music & Sound Effects & Intros\Vids & FX\Boom.mp3'

HISTORY_FILE = 'chat_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

def find_response(user_message, history):
    for stored_message, response in history.items():
        if user_message.lower() in stored_message.lower():
            return response
    return None

def play_sound():
    if os.path.exists(SOUND_FILE):
        pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.play()

def send_message():
    user_message = message_entry.get("1.0", tk.END).strip()
    message_entry.delete("1.0", tk.END)
    conversation_history.config(state=tk.NORMAL)
    conversation_history.insert(tk.END, f"You: {user_message}\n")
    conversation_history.config(state=tk.DISABLED)

    response = find_response(user_message, history)
    if response:
        play_sound()
        conversation_history.config(state=tk.NORMAL)
        conversation_history.insert(tk.END, f"ChatBot: {response}\n")
        conversation_history.config(state=tk.DISABLED)
    else:
        answer = messagebox.askyesno("New Response", "No response found. Do you want to add a new response?")
        if answer:
            response = simpledialog.askstring("Input", "Please enter the response:")
            if response:
                history[user_message] = response
                save_history(history)
                play_sound()
                conversation_history.config(state=tk.NORMAL)
                conversation_history.insert(tk.END, f"ChatBot: {response}\n")
                conversation_history.config(state=tk.DISABLED)

window = tk.Tk()
window.title("ChatBot")

window.configure(bg='white')

conversation_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg='dark slate gray')
conversation_history.pack(expand=True, fill="both") #

message_entry = tk.Text(window, height=3, bg='powder blue')
message_entry.pack(fill="x")

send_button = tk.Button(window, text="Send", command=send_message, bg='lemonchiffon4')
send_button.pack()

message_entry.focus()

history = load_history()

window.mainloop()