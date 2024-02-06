import socket
HOST = 'localhost'
PORT = 8080
print("\n****************************************************************")
print(r"""
                   _______                               
            /\     |     |  |\        /|    /\    |\    |
           /  \    |_____|  | \      / |   /  \   | \   |
          /____\   |    \   |  \    /  |  /____\  |  \  |
         /	\  |     \  |   \  /   | /      \ |   \ |
        /        \ |      \ |    \/    |/        \|    \|
""")
print("\n****************************************************************")

def send_LIST_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        print(f'Response from server: {response}')   
    client_socket.close()

def send_RETR_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode('utf-8'))
        file_name = input("please input the file name: ")
        directory = "E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\network-project-phase02-armanus-co\\Client\\" + file_name
        file = open(directory , 'wb')
        data = client_socket.recv(1024)
        while (data):
            file.write(data)
            data = client_socket.recv(1024)
        file.close()
    Result = client_socket.recv(1024).decode('utf-8')
    print(Result)
    client_socket.close()

def send_STORE_request(request):
    RQ = request.split()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode('utf-8'))
        directory = "E:\\Amozeshi\\UNI\\UNI T5\\Computer Networking\\network-project-phase02-armanus-co\\Client\\" + RQ[1]
        file = open(directory , 'rb')
        data = file.read(1024) 
        while (data):
            client_socket.send(data)
            data = file.read(1024)
        file.close()
    Result = client_socket.recv(1024).decode('utf-8')
    print(Result)
    client_socket.close()

def send_DELE_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request.encode('utf-8'))
    confirm = client_socket.recv(1024).decode('utf-8')
    last_check = input(confirm)
    client_socket.sendall(last_check.encode('utf-8'))
    Result = client_socket.recv(1024).decode('utf-8')
    print(Result)
    client_socket.close()
def Get_order():
    
    request = input("Want You Want to Do? \n 1) <LIST /path/directory> :     See server files   \n 2) <RETR /path/file.txt> :      Download file from server  \n 3) <STORE /client-path /server-path> :     Upload file to server   \n 4) <DELE /path/file.jpg> :        Delete a file from server\n")
    if 'LIST' in request:
        send_LIST_request(request)
    elif 'RETR' in request:
        send_RETR_request(request)
    elif 'STORE' in request:
        send_STORE_request(request)
    elif 'DELE' in request:
        send_DELE_request(request)

    
if __name__ == '__main__':
    Get_order()
