## CLIENT
## AWS version

import sys
import socket
import threading


# For recieving new messages
def receive():
    # Keep Receiving Messages From Server (second message and onwards)
    while True:
        try:
            message = client_socket.recv(2048).decode()
            # Set conditional so that when server sends "disconnected", while breaks
            if message != "you_are_now_disconnected":
                print(message)
            else:
                break
        except:
            client_socket.close()
            break


# For sending new messages
def write():
    while True:
        try:
            message = input() 
            if message != "quit":
                client_socket.send((f"{username}: " + message).encode())
            else:
                client_socket.send("quit".encode())
                break
        except:
            client_socket.close()
            break


# The run function
def run():
    try:
        # Starting threads for receiving from server
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        # Starting threads for writing to server
        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        # Generally for when server closes randmomly
        pass


# The main program body
if __name__ == '__main__':
    # Parsing username from command-line program call: python tcp_client.py <username>
    username = sys.argv[1] 

    # Connecting with server 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("34.229.53.146", 8080))                     

    # Sending server the username from command-line
    client_socket.send(username.encode())

    # Displaying connection confirmation from server (always the first message server sends)   (The second message is "{username} joined!")
    print(client_socket.recv(2048).decode())

    # Calling the run function
    run()