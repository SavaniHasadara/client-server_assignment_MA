import socket
import sys

class Client:
    def __init__(self, server_ip, port, mode, topic):
        self.server_ip = server_ip
        self.port = port
        self.mode = mode
        self.topic = topic
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.port))
        print(f"Connected to server: {self.server_ip}:{self.port}")

        try:
            while True:
                message = input("Enter message: ")

                self.client_socket.sendall(f"{self.topic}:{message}".encode())

                if message.strip() == 'terminate':
                    break

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python my_client_app.py <server_ip> <port> <mode: PUBLISHER/SUBSCRIBER> <topic>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    mode = sys.argv[3].upper()
    topic = sys.argv[4]
    client = Client(server_ip, port, mode, topic)
    client.start()