import socket, struct
from SocketMessageIOFile import SocketMessageIO






if __name__ == '__main__':
    mySocket = socket.socket()
    manager = SocketMessageIO()
    name = input("What is your name? ")

    port = 3000
    mySocket.connect(('127.0.0.1',port))
    # print (mySocket.recv(1024).decode())
    # print (f"Sending {len(name)=}")
    manager.send_message_to_socket(name, mySocket)
    acknowledgement = manager.receive_message_from_socket(mySocket)
    print(acknowledgement)
    while True:
        msg = input ("What is the message? ")
        manager.send_message_to_socket(msg, mySocket)
        acknowledgement = manager.receive_message_from_socket(mySocket)
        print(acknowledgement)