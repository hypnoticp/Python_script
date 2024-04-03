import sys
import socket
import threading

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join(f'{x:0{digits}x}' for x in s)
        text = ''.join(chr(x) if 32 <= x < 127 else '.' for x in s)
        result.append(f'{hexa:<{length * (digits + 1)}} {text}')

    return '\n'.join(result)

def receive_from(connection):
    buffer = b""
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print(f"Error receiving data: {e}")

    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        print(hexdump(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer) == 0:
            break

        print(f"[<==] Received {len(local_buffer)} bytes from localhost")
        print(hexdump(local_buffer))

        remote_socket.send(local_buffer)
        print("[==>] Sent to remote")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer) == 0:
            break

        print(f"[<==] Received {len(remote_buffer)} bytes from remote")
        print(hexdump(remote_buffer))

        client_socket.send(remote_buffer)
        print("[==>] Sent to localhost")

    client_socket.close()
    remote_socket.close()

def server_loop():
    local_host = input("Enter LOCAL_HOST: ")
    local_port = input("Enter LOCAL_PORT: ")

    # 验证端口输入
    while not local_port.isdigit():
        print("Invalid input. Please enter a valid port number.")
        local_port = input("Enter LOCAL_PORT: ")

    local_port = int(local_port)

    remote_host = input("Enter REMOTE_HOST: ")
    remote_port = input("Enter REMOTE_PORT: ")

    # 验证端口输入
    while not remote_port.isdigit():
        print("Invalid input. Please enter a valid port number.")
        remote_port = input("Enter REMOTE_PORT: ")

    remote_port = int(remote_port)

    receive_first = True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"Error binding to {local_host}:{local_port}: {e}")
        sys.exit(0)

    print(f"Listening on {local_host}:{local_port}")
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print(f"Received incoming connection from {addr[0]}:{addr[1]}")

        proxy_thread = threading.Thread(target=proxy_handler,
                    args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

if __name__ == '__main__':
    server_loop()
