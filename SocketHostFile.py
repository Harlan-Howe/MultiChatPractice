import socket,threading, struct
from typing import Dict, List
from SocketMessageIOFile import SocketMessageIO, MessageType


def broadcast_message_to_all(message:str):
    global userDictLock, userDict, broadcast_manager
    if broadcast_manager is None:
        broadcast_manager = SocketMessageIO()

    userDictLock.acquire()
    for id in userDict:
        broadcast_manager.send_message_to_socket(message, userDict[id]["connection"])
    userDictLock.release()

def send_user_list_to_all():
    global userDictLock, userDict, broadcast_manager
    if broadcast_manager is None:
        broadcast_manager = SocketMessageIO()

    userDictLock.acquire()
    list_info = f"{len(userDict)}"
    for id in userDict:
        print(f"{id=}\t{userDict[id]}\t{userDict[id]['name']=}")
        list_info += f"\t{userDict[id]['name']}"

    print(f"{list_info=}")

    for id in userDict:
        broadcast_manager.send_message_to_socket(message=list_info, connection=userDict[id]["connection"],type=MessageType.USER_LIST)
    userDictLock.release()

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
        # print(f"Waiting for message from {name}")
        try:
            type, message = manager.receive_message_from_socket(connection)
        except ConnectionAbortedError:
            print(f"{name} disconnected.")
            userDictLock.acquire()
            del userDict[id]
            userDictLock.release()
            broadcast_message_to_all(f"{name} has left the conversation.")
            send_user_list_to_all()
            return

        if name is None:
            name = message
            manager.send_message_to_socket(f"Welcome, {name}!", connection)
            userDictLock.acquire()
            userDict[id]["name"] = name
            userDictLock.release()
            broadcast_message_to_all(f"{name} has joined the conversation.")
            send_user_list_to_all()
        else:
            manager.send_message_to_socket(f"{name}: {message}", connection)



if __name__ == '__main__':
    global userDict, userDictLock, latest_id, broadcast_manager
    broadcast_manager = None
    latest_id = 0

    userDict: Dict[int, Dict] = {}
    userDictLock = threading.Lock()

    mySocket = socket.socket()
    port = 3000
    mySocket.bind(('',port))
    mySocket.listen(5)
    print ("Socket is listening.")
    while True:
        connection, address = mySocket.accept()

        print (f"Got connection from {address}")
        # connection.send("Thank you for connecting.".encode())

        latest_id += 1
        connectionThread = threading.Thread(target=listen_to_connection, args=(connection, latest_id, address))

        userDictLock.acquire()
        userDict[latest_id] = {"name":"unknown", "connection":connection}
        userDictLock.release()


        connectionThread.start()


