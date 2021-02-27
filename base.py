from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen()


while True:
    client_socket, addr = server_socket.accept()
    print('Client connected from', addr)

    while True:
        buff = client_socket.recv(4096)
        print(f'Recv {len(buff)} bytes from client')

        if not buff:
            break
        else:
            client_socket.send(b'Hello world\n')
            print(f'Send hello to client')

    client_socket.close()
    print('Client disconnected from', addr)
