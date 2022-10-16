import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import List


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.geometry('800x800+50+50')  # an 800 x 800 window, offset on screen by (50, 50).

        self.user_entry_string = None
        self.text_field = None
        self.user_list_text = None
        self.chat_so_far = ""
        self.chat_response_text = None

        self.build_GUI_elements()

        # these are two additional methods (yes, really!) that will be set by an external class so that we can call them
        # from inside this class once they have been set. But for now, they're None.
        self.shut_down_socket = None
        self.tell_my_client_to_send_message = None

    def build_GUI_elements(self):
        # set the relative sizes of the columns and rows in this grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=6)
        self.root.rowconfigure(1, weight=1)

        # the bottom frame is where the user is prompted to type something, along with the text field to type it.
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=6)
        bottom_frame.grid(column=0, row=1, columnspan=2, sticky='new')
        entry_label = ttk.Label(bottom_frame, text='Enter what you want to say here:')
        entry_label.grid(column=0, row=0, sticky='e')
        self.user_entry_string = tk.StringVar()
        self.text_field = ttk.Entry(bottom_frame, textvariable=self.user_entry_string)
        self.text_field.grid(column=1, row=0, sticky='ew')
        self.text_field.bind('<Return>', self.respond_to_text_entry)

        # This is where the user list is kept.
        self.user_list_text = ScrolledText(self.root, width=20, background="black", foreground="white")
        self.user_list_text.grid(column=0, row=0, sticky='ns')
        self.user_list_text['state'] = 'disabled'  # not editable by user

        # this is where the transcript of the chat is kept.
        self.chat_response_text = ScrolledText(self.root, background='#bbbbbb')
        self.chat_response_text.grid(column=1, row=0, sticky='ns')
        self.chat_response_text['state'] = 'disabled'  # not editable by user

    def run_loop(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.shut_down_socket()
        self.root.destroy()

    def set_user_list(self, users: List[str]) -> None:
        names = ""
        for user in users:
            names += f"{user}\n"

        self.user_list_text['state'] = 'normal'
        self.user_list_text.replace(1.0, 'end', names)
        self.user_list_text['state'] = 'disabled'

    def add_to_chat(self, entry: str) -> None:
        self.chat_so_far += entry+"\n"
        self.chat_response_text['state'] = 'normal'
        self.chat_response_text.replace(1.0, 'end', self.chat_so_far)
        self.chat_response_text['state'] = 'disabled'

    def respond_to_text_entry(self, event_info):
        message = self.user_entry_string.get()
        self.tell_my_client_to_send_message(message)
        self.user_entry_string.set("")
