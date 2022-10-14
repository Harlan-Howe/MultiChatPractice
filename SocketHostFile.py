import socket,threading, struct
from typing import Dict, List
from SocketMessageIOFile import SocketMessageIO, MessageType


def broadcast_message_to_all(message:str, message_type=MessageType.MESSAGE):
    global user_dictionary_lock, user_dictionary, broadcast_manager
    if broadcast_manager is None:
        broadcast_manager = SocketMessageIO()

    user_dictionary_lock.acquire()
    for id in user_dictionary:
        broadcast_manager.send_message_to_socket(message, user_dictionary[id]["connection"], type=message_type)
    user_dictionary_lock.release()

def send_user_list_to_all():
    global user_dictionary_lock, user_dictionary, broadcast_manager
    if broadcast_manager is None:
        broadcast_manager = SocketMessageIO()

    #develop list of online users
    user_dictionary_lock.acquire()
    list_info = f"{len(user_dictionary)}"
    for id in user_dictionary:
        print(f"{id=}\t{user_dictionary[id]}\t{user_dictionary[id]['name']=}")
        list_info += f"\t{user_dictionary[id]['name']}"
    user_dictionary_lock.release()
    # send that message to every user.
    broadcast_message_to_all(list_info, message_type=MessageType.USER_LIST)

def listen_to_connection(connection:socket, id: int, address:str = None)->None:
    """
    a loop intended for a Thread to monitor the given socket and handle any messages that come from it. In this case,
    it is assumed that the first message received will be the name of the connection, in the format of a packed length
    of the name and then the name itself. All messages should be in the format of packed length + message.
    :param connection: the socket that will be read from
    :param address: the address of the socket (not currently used)
    :return: None
    """
    name = None
    manager = SocketMessageIO()
    while True:
        try:
            type, message = manager.receive_message_from_socket(connection)
        except (ConnectionAbortedError, ConnectionResetError) :
            print(f"{name} just disconnected.")
            user_dictionary_lock.acquire()
            del user_dictionary[id]
            user_dictionary_lock.release()
            broadcast_message_to_all(f"{'-'*6} {name} has left the conversation. {'-'*6} ")
            send_user_list_to_all()
            return

        if name is None:
            name = message
            manager.send_message_to_socket(f"Welcome, {name}!", connection)
            user_dictionary_lock.acquire()
            user_dictionary[id]["name"] = name
            user_dictionary_lock.release()
            broadcast_message_to_all(f"{'-'*6} {name} has joined the conversation. {'-'*6} ")
            send_user_list_to_all()
        else:
            broadcast_message_to_all(f"{name}: {message}")



if __name__ == '__main__':
    global user_dictionary, user_dictionary_lock, latest_id, broadcast_manager
    broadcast_manager = None
    latest_id = 0

    user_dictionary: Dict[int, Dict] = {}
    user_dictionary_lock = threading.Lock()

    mySocket = socket.socket()
    port = 3000
    mySocket.bind(('',port))
    mySocket.listen(5)
    print ("Socket is listening.")
    while True:
        connection, address = mySocket.accept()

        print (f"Got connection from {address}")

        latest_id += 1
        connectionThread = threading.Thread(target=listen_to_connection, args=(connection, latest_id, address))

        user_dictionary_lock.acquire()
        user_dictionary[latest_id] = {"name": "unknown", "connection":connection}
        user_dictionary_lock.release()
        connectionThread.start()


