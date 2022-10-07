import socket, struct, threading
from SocketMessageIOFile import SocketMessageIO, MessageType


def listen_for_messages(connection: socket):

    while(True):
        type, message = manager.receive_message_from_socket(connection)
        print(f"{type=}\t{message=}")
        if type == MessageType.MESSAGE:
            print(f"MSG: {message}")
        elif type == MessageType.USER_LIST:
            update_user_list(message)
            print("------------------")
            for i in range(len(user_list)):
                print(f"{i}\t{user_list[i]}")
            print("------------------")

def update_user_list(message: str)->None:
    global user_list
    print(f"{message=}")

    parts = message.split("\t")
    print(f"{parts=}")
    user_list.clear()
    num_users = int(parts[0])
    for i in range(1,num_users+1):
        user_list.append(parts[i])

if __name__ == '__main__':
    global manager, user_list
    user_list = []
    mySocket = socket.socket()
    manager = SocketMessageIO()
    name = input("What is your name? ")

    port = 3000
    mySocket.connect(('127.0.0.1', port))
    # print (mySocket.recv(1024).decode())
    # print (f"Sending {len(name)=}")
    manager.send_message_to_socket(name, mySocket)
    # acknowledgement = manager.receive_message_from_socket(mySocket)
    # print(acknowledgement)

    listener_thread = threading.Thread(target=listen_for_messages, args=(mySocket,))
    listener_thread.start()
    while True:
        msg = input ("What is the message? ")
        manager.send_message_to_socket(msg, mySocket)
        # acknowledgement = manager.receive_message_from_socket(mySocket)
        # print(acknowledgement)