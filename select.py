from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)


def server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen()
    return server_socket


def accept_connection(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print('Client connected from', addr)


def send_message(client_socket, addr):
    while True:
        buff = client_socket.recv(4096)
        print(f'Recv {len(buff)} bytes from client {addr}')

        if not buff:
            break
        else:
            client_socket.send(b'Hello world\n')
            print(f'Send hello to client')

    client_socket.close()
    print('Client disconnected from', addr)


if __name__ == '__main__':
    sock = server()
    accept_connection(sock)
