from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from select import select

sock_list = []


def server():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    srv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    srv_sock.bind(('0.0.0.0', 5000))
    srv_sock.listen()
    return srv_sock


def accept_connection(srv_sock):
    client_socket, addr = srv_sock.accept()
    print('Client connected from', addr)
    sock_list.append(client_socket)


def send_message(client_socket):
    buff = client_socket.recv(4096)
    remote_addr = client_socket.getpeername()
    print(f'Recv {len(buff)} bytes from client {remote_addr}')

    if buff:
        client_socket.send(b'Hello world\n')
        print(f'Send hello to client')
    else:
        client_socket.close()
        print(f'Client disconnected from {remote_addr}')


def event_loop():
    while True:

        try:

            read_sock_list, _, _ = select(sock_list, [], [])

            for sock in read_sock_list:
                if sock is server_socket:
                    accept_connection(sock)
                else:
                    send_message(sock)

        except KeyboardInterrupt:
            print('Terminated')
            exit(0)


if __name__ == '__main__':
    server_socket = server()
    sock_list.append(server_socket)
    event_loop()
