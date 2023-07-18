import socket
import sys
import threading

class Server:
    def __init__(self, port):
        self.host = ''
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.publishers = {}
        self.subscribers = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started and listening on port {self.port}...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New client connected: {client_address}")
                self.client_sockets.append(client_socket)

                # Create a thread to handle the client connection
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()

        except KeyboardInterrupt:
            self.shutdown()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if data:
                    print(f"Received from client: {data}")

                    if data.strip() == 'terminate':
                        break

                    if client_socket in self.publishers.values():
                        self.publish_message(data, client_socket)
                    elif client_socket in self.subscribers.values():
                        topic, message = data.split(":", 1)
                        print(f"Subscriber received message on topic '{topic}': {message}")

        except ConnectionResetError:
            pass
        finally:
            client_socket.close()
            self.client_sockets.remove(client_socket)
            if client_socket in self.publishers.values():
                publisher = next(key for key, value in self.publishers.items() if value == client_socket)
                del self.publishers[publisher]
            elif client_socket in self.subscribers.values():
                subscriber = next(key for key, value in self.subscribers.items() if value == client_socket)
                del self.subscribers[subscriber]

    def publish_message(self, message, sender_socket):
        topic, _ = message.split(":", 1)
        for subscriber_socket in self.subscribers.values():
            if subscriber_socket != sender_socket and self.subscribers.get(topic) == subscriber_socket:
                subscriber_socket.sendall(message.encode())

    def shutdown(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()
        print("Server stopped.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = Server(port)
    server.start()