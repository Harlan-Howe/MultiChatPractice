import socket
import threading

from ClientGUIFile import ClientGUI
from SocketMessageIOFile import SocketMessageIO, MessageType


def listen_for_messages(connection: socket):
    global keep_listening
    while keep_listening:
        try:
            message_type, message = manager.receive_message_from_socket(connection)
        except ConnectionAbortedError as CAErr:
            print(CAErr)
            keep_listening = False
            break
        print(f"{message_type=}\t{message=}")
        if message_type == MessageType.MESSAGE:
            handle_receive_message(message)
        elif message_type == MessageType.USER_LIST:
            handle_user_list_update(message)

    print("listen_for_messages is over.")


def handle_user_list_update(tab_delimited_user_list_string:str) -> None:
    update_user_list(tab_delimited_user_list_string)
    print("------------------")
    for i in range(len(user_list)):
        print(f"{i}\t{user_list[i]}")
    print("------------------")
    client_gui.set_user_list(user_list)


def handle_receive_message(message:str) -> None:
    print(f"MSG: {message}")
    client_gui.add_to_chat(message)


def update_user_list(message: str) -> None:
    global user_list
    print(f"{message=}")

    parts = message.split("\t")
    print(f"{parts=}")
    user_list.clear()
    num_users = int(parts[0])
    for i in range(1, num_users+1):
        user_list.append(parts[i])
    client_gui.set_user_list(parts[1:0])


def send_message(message: str) -> None:
    manager.send_message_to_socket(message, mySocket)


def close_socket():
    global keep_listening
    keep_listening = False
    mySocket.close()


if __name__ == '__main__':
    global manager, user_list, client_gui, mySocket, listener_thread, keep_listening
    client_gui = ClientGUI()
    user_list = []
    mySocket = socket.socket()
    manager = SocketMessageIO()
    name = input("What is your name? ")

    port = 3000
    mySocket.connect(('127.0.0.1', port))
    manager.send_message_to_socket(name, mySocket)
    keep_listening = True
    listener_thread = threading.Thread(target=listen_for_messages, args=(mySocket,))
    listener_thread.start()

    # telling the GUI about two methods in this class that it can call.
    client_gui.tell_my_client_to_send_message = send_message
    client_gui.shut_down_socket = close_socket

    client_gui.run_loop()
