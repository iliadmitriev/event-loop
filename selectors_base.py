from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
import selectors

selector = selectors.DefaultSelector()


def server():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    srv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    srv_sock.bind(('0.0.0.0', 5000))
    srv_sock.listen()
    selector.register(
        fileobj=srv_sock,
        events=selectors.EVENT_READ,
        data=accept_connection
    )


def accept_connection(srv_sock):
    client_socket, addr = srv_sock.accept()
    print('Client connected from', addr)
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_socket):
    buff = client_socket.recv(4096)
    remote_addr = client_socket.getpeername()
    print(f'Recv {len(buff)} bytes from client {remote_addr}')

    if buff:
        client_socket.send(
            b'HTTP/1.1 200 OK\r\n'
            b'Content-Length: 11\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'Hello World'
        )
        print(f'Send data to client {remote_addr}')
        selector.unregister(client_socket)
        client_socket.close()
    else:
        selector.unregister(client_socket)
        client_socket.close()
        print(f'Client disconnected from {remote_addr}')


def event_loop():
    while True:

        try:

            events = selector.select()

            for k, _ in events:
                callback = k.data
                callback(k.fileobj)

        except KeyboardInterrupt:
            print('Terminated')
            exit(0)


if __name__ == '__main__':
    server()
    event_loop()
