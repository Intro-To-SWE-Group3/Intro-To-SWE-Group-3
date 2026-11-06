import socket
import threading

HOST = '127.0.0.1'  # Localhost (use '0.0.0.0' to allow other machines on LAN)
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender_client=None):
    """Send message to all clients except optionally the sender."""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except Exception:
                remove_client(client)

def remove_client(client):
    """Safely disconnect and clean up client data."""
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        broadcast(f"{nickname} has left the chat.".encode('utf-8'))

def handle_client(client):
    """Listen for incoming messages from a specific client."""
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            broadcast(message, sender_client=client)
        except Exception:
            remove_client(client)
            break

def receive():
    """Main loop accepting new connections."""
    print(f"Server listening on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and record nickname
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'), sender_client=client)
        client.send("Connected to the server. Type your messages below:\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
        thread.start()

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.close()