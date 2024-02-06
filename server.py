import socket
import time
import os

def Get_Path_List(directory, layer):
    file_info = ''
    tabs = '\t' * layer
    items = os.listdir(directory)
    for item in items:
        item_path = os.path.join(directory, item)
        modified_timestamp = os.path.getmtime(item_path)
        modified_date =  time.strftime('%Y-%m-%d %H:%M', time.localtime(modified_timestamp))
        # Send the file name and its directory to the client
        file_info += f"{tabs}{modified_date}\t {item}\n"
        if os.path.isdir(item):
            file_info += Get_Path_List(item_path, 1)
    return file_info
            

def LIST(request, client_socket):
    directory = 'E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\FTP Server Files'
    request = request.split()
    try:
        rq = request[1]
        rq = rq.replace('/', "\\")
        directory = os.path.join(directory, rq)
    except:
        pass

    file_info = "\n"
    
    file_info += Get_Path_List(directory, 0)

    client_socket.sendall(file_info.encode())


def RETR(request, client_socket):
    request = request.split()
    filedir = request[1]
    filedir = filedir.replace('/', '\\')
    directory = 'E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\FTP Server Files'+filedir
    try:
        file = open(directory, 'rb')
        data = file.read(1024)
        while (data):
            client_socket.send(data)
            data = file.read(1024)
        file.close()
        client_socket.send(data)
        file.close()
        print(f"a file downloaded from server. path:{directory}")
        response = "selected file transmitted successfully."
        client_socket.sendall(response.encode())
    except:
        print("File download request failed.")
        response = "File transmission failed."
        client_socket.sendall(response.encode())

def STORE(request, client_socket):
    request = request.split()
    filedir = request[2]
    filedir = filedir.replace('/', '\\')
    directory = 'E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\FTP Server Files'+filedir
    try:
        file = open(directory, 'wb')
        data = client_socket.recv(1024)
        while (data):
            file.write(data)
            data = client_socket.recv(1024)

        file.close()
        print(f"a file stored on server. path:{directory}")
        response = "selected file transmitted successfully."
        client_socket.sendall(response.encode())
    except:
        print("a store request failed.")
        response = "File transmission failed."
        client_socket.sendall(response.encode())

def DELE(request, client_socket):
    rq = request.split()
    filedir = rq[1]
    filedir = filedir.replace('/', '\\')
    directory = 'E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\FTP Server Files' + filedir
    confirm_mesage = "Do you really wish to delete? Y/N \n"
    client_socket.send(confirm_mesage.encode())
    last_check = client_socket.recv(1024).decode
    if last_check == 'Y' or 'y':
        if os.path.exists(directory):
            os.remove(directory)
            response = "The file deleted successfully."
            client_socket.sendall(response.encode())
        else:
            response = "The file does not exist"
            client_socket.sendall(response.encode())
    else:
        response = "File deleting Canceled"
        client_socket.sendall(response.encode())

def main():
    host = 'localhost'
    port = 8080

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.bind((host, port))
    ftp_socket.listen(1)
    print("FTP server is waiting for any incomming requests...")

    while True:
        client_socket , client_address = ftp_socket.accept()
        request = client_socket.recv(4096).decode()

        if "LIST" in request:
            LIST(request, client_socket)
        elif "RETR" in request:
            RETR(request, client_socket)
        elif "STORE" in request:
            STORE(request, client_socket)
        elif "DELE" in request:
            DELE(request, client_socket)
        else:
            response = "HTTP/1.1 400 Bad Request\n\nInvalid request"
            client_socket.sendall(response.encode())

        client_socket.close()

if __name__ == '__main__':
    main()
