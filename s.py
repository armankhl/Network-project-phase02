import socket
import threading
import os
from datetime import datetime

class ClientHandler:
    def __init__(self, control_socket, data_port):
        self.control_socket = control_socket
        self.data_port = data_port
        self.data_socket = None
        self.data_connection = None

    def open_data_socket(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('127.0.0.1', self.data_port))
        return data_socket

    def start_data_connection(self):
        self.data_socket = self.open_data_socket()
        self.send_response(150, "Data connection established")

    def close_data_connection(self):
        if self.data_socket:
            self.data_socket.close()
            self.data_socket = None
        if self.data_connection:
            self.data_connection.close()
            self.data_connection = None

    def send_response(self, code, message):
        response = f"{code} {message}\r\n"
        self.control_socket.send(response.encode("utf-8"))

    def handle_list(self, path):
        try:
            if not self.data_socket:
                self.send_response(425, "Data connection not established")
                return

            if not path:
                directory_path = os.getcwd()
            elif os.path.isabs(path):
                directory_path = path
            else:
                directory_path = os.path.join(os.getcwd(), path)

            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                self.send_response(550, f"Directory not found: {directory_path}")
                return

            file_list = os.listdir(directory_path)
            file_info_list = [f"{file}\t{os.path.getsize(os.path.join(directory_path, file))} bytes" for file in file_list]

            self.start_data_connection()

            for file_info in file_info_list:
                self.data_socket.send(file_info.encode("utf-8") + b'\r\n')

            self.send_response(226, "Transfer complete")
        except Exception as e:
            print(f"Error handling LIST command: {e}")
            self.send_response(550, f"Error handling LIST command: {e}")
        finally:
            self.close_data_connection()

def handle_client(control_socket, data_port):
    client_handler = ClientHandler(control_socket, data_port)

    while True:
        command = control_socket.recv(1024).decode("utf-8")
        if not command:
            break

        parts = command.split()
        cmd = parts[0].upper()

        if cmd == "LIST":
            path = parts[1] if len(parts) > 1 else ""
            client_handler.handle_list(path)
        elif cmd == "QUIT":
            break
        else:
            client_handler.send_response(502, "Command not implemented")

    control_socket.close()

def start_server():
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.bind(('127.0.0.1', 21))
    control_socket.listen(5)
    print("FTP server listening on port 21")

    while True:
        client_socket, addr = control_socket.accept()
        print(f"Accepted connection from {addr}")
        data_port = 3000  # Use a fixed data port for simplicity
        threading.Thread(target=handle_client, args=(client_socket, data_port)).start()

if __name__ == "__main__":
    start_server()
