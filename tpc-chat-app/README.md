# TCP Chat Application

A simple chat and file transfer application built using Python's socket programming. This project demonstrates the fundamental concepts of networking, including TCP sockets, multi-threading, and client-server communication.

## Features

- **Multi-client support**: Multiple clients can connect and communicate via a central server.
- **Message Broadcasting**: Messages sent by one client are broadcasted to all other connected clients.
- **File Transfer**: Clients can send files to other connected users.
- **Threading for Concurrency**: The server and client use threading to handle multiple tasks simultaneously.
- **Graceful Error Handling**: Handles disconnections and communication errors efficiently.

## Installation

### Prerequisites
Ensure you have Python installed on your system (Python 3 recommended). You can check your Python version using:

```sh
python --version
```

### Clone the Repository

```sh
git clone https://github.com/ThatDudeAlex/Networking-Fundamentals.git
cd Networking-Fundamentals/tcp-chat-app
```

## Usage

### Running the Server
To start the server, run the following command:

```sh
python server.py
```

The server will listen for incoming client connections on `localhost` and port `49152`.

### Running the Client
To start a client, run:

```sh
python client.py
```

Once the 2 or more clients connect, you can start sending messages. Type a message and press Enter to send it.

#### Sending Files
To send a file, use the command:

```sh
sendfile <file_path>
```

For example:

```sh
sendfile sample.txt
```

The file will be transferred to the connected clients.

#### Exiting the Chat
To exit the chat, type:

```sh
exit
```

## Code Overview

### Server (`server.py`)
- Uses a TCP socket to accept connections.
- Maintains a list of connected clients.
- Listens for incoming messages and broadcasts them to all other clients.
- Handles client disconnections and errors gracefully.

### Client (`client.py`)
- Connects to the server using a TCP socket.
- Runs separate threads for sending and receiving messages.
- Supports sending and receiving files.
- Ensures proper message formatting and synchronization using locks.

## Future Enhancements
- **Graphical User Interface (GUI)**: Implement a user-friendly UI using Tkinter or PyQt.
- **Encryption**: Secure communication with end-to-end encryption.
- **User Authentication**: Implement login and username support.
- **Message History**: Save chat logs for later reference.

