
""" 
Allows network communication by using 'sockets'
    Sockets are the fundamental building blocks for network communication,
    allowing applications to send and receive data over a network
"""
import socket

# Using threads allow us to handle multiple clients simultaneously
import threading

# most common encoding on the internet
ENCODING = "utf-8"

# Size of the buffer used to receive data. Data is sent in chunks, and this
# determines the maximum size of each chunk. 1024 bytes (1 KB)
BUFFER_SIZE = 1024

# List to store client sockets. Each socket object represents a
# connection to a specific client
client_sockets = []

# List to store client threads
client_threads = []


# cleans up by removing any client socket & thread
# that are no longer neened
def remove_client(client_socket):
    # remove client from the list
    client_sockets.remove(client_socket)

    # Remove the client thread as well
    for thread in client_threads:
        if thread.client_socket == client_socket:
            client_threads.remove(thread)
            break
    client_socket.close()


# Will run on a seperate thread for each connected client
def handle_client(client_socket):

    # Continuesly tries to receive messages from the client
    while True:
        try:
            # Receives data from the client socket
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            # Empty message indicates the client has disconnected
            # client_socket.getpeername() returns the address and port of the client
            if not message:
                print(f"{client_socket.getpeername()} disconnected")
                break

            # Broadcast the message to all other clients
            for other_client in client_sockets:
                if other_client != client_socket:
                    try:
                        other_client.sendall(message.encode(ENCODING))
                    except Exception as e:
                        # Client likely disconnected; remove them
                        remove_client(other_client)

                        print(f"Error sending to client: {e}")

                        # break inner loop as well, since the other client is removed
                        break
        except Exception as e:
            print(f"Communication Error: {e}")
            break

    # Terminate connection by removing client
    remove_client(client_socket)


""" 
creates the server's socket
    socket.AF_INET:     specifies that we're using ipv4
    socket.SOCK_STREAM: specifies that we're using TCP
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows us to reuse the same port if the server closed recently
# prevents "address already in use" erros while developing
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

'''
a socket it's just an 'endpoint'
bind() connects this endpoint to an IP address and port

  IP address:  identifies the machine on the network
  Port number: identifies a specific service or application
               running on that machine
'''
server_socket.bind(("localhost", 49152))

""" 
listen() makes the server start listening for incoming connections
    The parameter specifies the max number of 'queued connections,
    not how many connections the server can handle. 
"""
server_socket.listen()

print("Server is listening...")


# infinite loop on the main-thread, so the server continously
# accepts new connections
while True:
    try:
        # accepts a new connection.
        #   accept() blocks until a client connects
        client_socket, addr = server_socket.accept()
        print(f"Client connected: {addr}")

        client_sockets.append(client_socket)

        """  
        creates a new thread to handle the client
            target=handle_client:  specifies that the handle_client function 
                                   should be run in the thread

            args=(client_socket,): passes client_socket as an argument to the
                                   handle_client function. 
                                   IMPORTANT: args needs to be a 'tuple' hence the 
                                              , after client_socket
        """
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket,))

        # sets the thread as a daemon thread. Daemon threads automatically terminate when
        # the main program exits. This is important so that the server can be shut down cleanly.
        client_thread.daemon = True

        # adds the client's socket as an attribute to the thread object. Helpful for removing
        # the correct thread when a client disconnects
        client_thread.client_socket = (client_socket)

        # append new client_thread to list
        client_threads.append(client_thread)

        # start running the new thread simultaneously with the main-thread
        client_thread.start()
    except Exception as e:
        print(f"Error accepting connections: {e}")
