import socket, threading, struct
from SocketMessageIOFile import SocketMessageIO



def listen_to_connection(connection:socket, address:str = None)->None:
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
            message = manager.receive_message_from_socket(connection)
        except ConnectionAbortedError:
            print(f"It looks like {name} has disconnected.")
            return

        if name is None:
            name = message
            manager.send_message_to_socket(f"Welcome, {name}!", connection)
        else:
            manager.send_message_to_socket(f"Acknowledging: {message}", connection)



if __name__ == '__main__':
    global connectionThreadList, connectionThreadListLock
    mySocket = socket.socket()
    connectionThreadList = []
    connectionThreadListLock = threading.Lock()
    port = 3000
    mySocket.bind(('',port))
    mySocket.listen(5)
    print ("Socket is listening.")
    while True:
        connection, address = mySocket.accept()

        print (f"Got connection from {address}")
        # connection.send("Thank you for connecting.".encode())
        connectionThread = threading.Thread(target=listen_to_connection, args= (connection, address))
        connectionThreadListLock.acquire()
        connectionThreadList.append(connectionThread)
        connectionThreadListLock.release()
        connectionThread.start()


