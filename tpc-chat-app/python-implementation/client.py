""" 
Allows network communication by using 'sockets'
    Sockets are the fundamental building blocks for network communication,
    allowing applications to send and receive data over a network
"""
import socket

# Using threads allow us to run multiple functions simultaneously
#   - Sending messages
#   - Receiving messages
import threading

# Will be used to manage messages waiting to be sent
import queue
import os

# Most common encoding on the internet
ENCODING = 'utf-8'

# Size of the buffer used to receive data. Data is sent in chunks, and this
# determines the maximum size of each chunk. 1024 bytes (1 KB)
BUFFER_SIZE = 1024

"""
threading.Lock() creates a lock object
    Locks: are used to synchronize access to shared resources
           and prevent race conditions

           IMPORTANT: we need a lock to protect the print function
                      so that messages from different threads are 
                      printed in order
"""
print_lock = threading.Lock()
message_queue = queue.Queue()


# Responsible for continuously receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receives data from the server
            message = client_socket.recv(BUFFER_SIZE).decode(ENCODING)

            if message:
                # Acquires the print_lock and ensures that only one thread
                # can print to the console at a time
                with print_lock:
                    """ 
                    \r:
                        is a special character that moves the cursor to the
                        beginning of the current line

                    end="": 
                        makes it so that print() doesn't add a new line 
                        '\n' at the end of the output. We're going to override 
                         the existing line not want a new one
                    """
                    print("\r", end="")

                    """
                    os.get_terminal_size().columns:
                        gets the character width of the terminal

                        IMPORTANT: we use this to erase the previous
                                   line by printing the same number of 
                                   spaces as the terminal width
                    
                    end="\r":
                        after printing the spaces, moves the cursor back
                        to the beginning of the line. 
                    """
                    print(" " * os.get_terminal_size().columns, end="\r")

                    # Print the received message
                    print(f"Received: {message}\n")

                    # Reprint the prompt
                    print("\rEnter message: ", end="")
            else:
                print("Server disconnected")
                break
        except ConnectionResetError:  # Server closed the connection abruptly.
            print("Connection to server lost")
            break
        except Exception as e:
            print(f"Error Receiving Msg: {e}")
            break


# Responsible for sending messages to the server
def send_messages(client_socket, message_queue):
    while True:
        # Get message from the queue (blocking). if the queue is empty,
        # it will block (wait) until a message becomes available
        message = message_queue.get()

        # Sends message to the server
        client_socket.sendall(message.encode(ENCODING))


""" 
Creates the client's socket
    socket.AF_INET:     specifies that we're using ipv4
    socket.SOCK_STREAM: specifies that we're using TCP
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connects to the server
    client_socket.connect(('localhost', 49152))
except ConnectionRefusedError:
    print(f"Error: Could not connect to server")
    exit()
except Exception as e:
    print(f"Error during connection: {e}")
    exit()


# creates a new thread to run 'receive_messages'
# 'args=' takes a tuple so a trailing comma is
# neededif there's 1 element
receive_thread = threading.Thread(
    target=receive_messages, args=(client_socket,))

# creates a new thread to run 'send_messages'
send_thread = threading.Thread(
    target=send_messages, args=(client_socket, message_queue))

# sets the threads as a daemon thread. Daemon threads automatically terminate when
# the main program exits. This is important so that the program doesn't hang
# waiting for these threads to finish
receive_thread.daemon = True
send_thread.daemon = True

# start running the new threads simultaneously with the main-thread
receive_thread.start()
send_thread.start()

# infinite loop on the main-thread, so the client continously
# await user input
while True:
    message = input("Enter message: ")

    if message.lower() == 'exit':
        break

    message_queue.put(message)  # Put message in the queue
    print()  # create a blank line between new inputs

# Close the socket when exiting the loop
client_socket.close()
print("Client disconnected")
