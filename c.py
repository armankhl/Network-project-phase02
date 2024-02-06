import socket

class FTPClient:
    def __init__(self, host, control_port, data_port):
        self.host = host
        self.control_port = control_port
        self.data_port = data_port
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket = None

    def create_data_socket(self):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return data_socket

    def start_data_connection(self):
        self.data_socket = self.create_data_socket()
        self.data_socket.connect((self.host, self.data_port))

    def stop_data_connection(self):
        if self.data_socket:
            self.data_socket.close()
            self.data_socket = None

    def handle_data_transfer(self):
        data = self.data_socket.recv(1024).decode("utf-8")
        print(data)

    def list_files(self, path=""):
        self.start_data_connection()
        command = f"LIST {path}\r\n"
        response = self.send_command(command)

        if response.startswith("150"):
            self.handle_data_transfer()
        elif response.startswith("226"):
            print("List command successful")
        else:
            print(f"Error: {response}")

        self.stop_data_connection()

    # ... (rest of the code remains unchanged)
if __name__ == "__main__":
    client = FTPClient("127.0.0.1", 21, 20)
