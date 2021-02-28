from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from select import select

tasks = []
to_read = {}
to_write = {}


def server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen()
    return accept_connection(server_socket)


def accept_connection(server_socket):
    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()   # read
        print('Client connected from', addr)

        tasks.append(send_message(client_socket))


def send_message(client_socket):
    while True:
        yield 'read', client_socket

        addr = client_socket.getpeername()
        buff = client_socket.recv(4096)     # read
        print(f'Recv {len(buff)} bytes from client {addr}')

        if buff:

            yield 'write', client_socket

            client_socket.send(            # write
                b'HTTP/1.1 200 OK\r\n'
                b'Content-Length: 11\r\n'
                b'Content-Type: text/plain\r\n'
                b'\r\n'
                b'Hello World'
            )
            print(f'Send data to client {addr}')
            client_socket.close()  # we don't need keepalive
            break
        else:
            print(f'Client disconnected from {addr}')
            client_socket.close()
            break


def event_loop():
    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            operation, sock = next(task)

            if operation == 'read':
                to_read[sock] = task
            if operation == 'write':
                to_write[sock] = task

        except StopIteration:
            pass


if __name__ == '__main__':
    srv_task = server()
    tasks.append(srv_task)
    event_loop()
