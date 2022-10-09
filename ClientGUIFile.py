import tkinter as tk
from tkinter import ttk
from typing import List
class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry('800x800+50+50')
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=4)
        self.root.rowconfigure(0,weight=5)
        self.root.rowconfigure(1,weight=1)

        self.user_entry_string = tk.StringVar()
        self.user_entry_string.set("User Entry")
        self.text_field = ttk.Entry(self.root, textvariable=self.user_entry_string)
        self.text_field.grid(column=0, row=1, columnspan=2)
        self.text_field.bind('<Return>', self.respond_to_text_entry)

        self.user_list_string = tk.StringVar()
        self.user_list_string.set("user list")
        self.user_list_label = ttk.Label(self.root, textvariable=self.user_list_string)
        self.user_list_label.grid(column=0, row=0)

        self.chat_response_string = tk.StringVar()
        self.chat_response_string.set("Here is the chat so far.")
        self.chat_response_label = ttk.Label(self.root, textvariable=self.chat_response_string)
        self.chat_response_label.grid(column=1, row=0)

    def run_loop(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.shut_down_socket()
        self.root.destroy()

    def set_user_list(self, users: List[str])->None:
        names = ""
        for user in users:
            names += f"{user}\n"
        self.user_list_string.set(names)

    def add_to_chat(self, entry: str)->None:
        chat_so_far = self.chat_response_string.get()
        chat_so_far += f"{entry}\n"
        self.chat_response_string.set(chat_so_far)

    def respond_to_text_entry(self, event_info):
        message = self.user_entry_string.get()
        self.message_sender(message)
        self.user_entry_string.set("")