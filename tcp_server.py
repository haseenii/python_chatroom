## SERVER
## AWS cloud version
import socket
import threading


# Sending Messages To All Connected Clients
def broadcast(message, user_socket):         
    for user in users:
        if user[0] != user_socket:
            user[0].send(message)


# Handling Messages From Clients
def handle(user):
    while True:
        # Broadcasting Messages
        message = user.recv(2048)
        if message.decode() == "quit":
            user.send("you_are_now_disconnected".encode())
            exiting_username = get_username(user)
            remove_user(user)
            print(f"[{exiting_username} just left the chat]")
            broadcast((f"[{exiting_username} just left the chat]").encode(), user)
            break
        else:
            broadcast(message, user)


# Getting username given socket object
def get_username(user_socket):
    for user in users:
        if user[0] == user_socket:
            return user[1]
        

# Getting rid of user from users[]
def remove_user(user_socket):
    for user in users:
        if user[0] == user_socket:
            users.remove(user)


# The run function
def run():
    # Establishing new connections and passing them on to handle()
    while True:
        # Accept client connection request
        connection, address = server_socket.accept()

        # Receive client username (always the first thing the client sends)
        username = connection.recv(2048).decode()

        # Add new client's info to users[] 
        users.append((connection, username))    

        # Announce the new connection we just formed
        print(f"[{username} just joined from {address}]")
        broadcast(f"{username} joined!".encode(), connection)
        connection.send('Connected to server!'.encode())

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(connection,))
        thread.start()


# The main program body
if __name__ == '__main__':
    # Host and port info 
    host = "0.0.0.0"
    port = 0

    # Starting Server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Making server listen for new connection requests from clients.
    server_socket.listen()
    print("[Server is ON and listening for new connections...]")

    # List of (connection, username) tuple
    users = []

    # makes the server to be able to accept and handle clients
    run()