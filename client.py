import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 55555

nickname = input("Choose your nickname: ").strip()
if not nickname:
    print("Nickname cannot be empty.")
    sys.exit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Could not connect to the server. Make sure server.py is running.")
    sys.exit()

def receive_messages():
    """Constantly listen for messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception:
            print("Connection closed by server.")
            client.close()
            break

def send_messages():
    """Read console input and transmit to server."""
    while True:
        try:
            text = input()
            if text.lower() == "/quit":
                client.close()
                break
            message = f"{nickname}: {text}"
            client.send(message.encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            client.close()
            break

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    send_messages()