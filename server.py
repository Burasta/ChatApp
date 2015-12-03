import sys
import socket
import select

HOST = ''
SERVER_LIST = []  # Not actually servers, but sockets.
PORT = 6000
RECV_BUFFER = 4096


def server():
    # Create a socket. First argument designates IPv4, second designates TCP
    ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Parse the socket layer.
    ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind global variables HOST and PORT to this socket.
    ser_socket.bind((HOST, PORT))
    # Initialize socket listening.
    ser_socket.listen(10)

    # Add this socket to the Server List.
    SERVER_LIST.append(ser_socket)

    # Print 'Connecting' message.
    print(" Starting server connection listening on port ", str(PORT))

    while 1:
        # Create variables to hold information.
        ready_to_read, ready_to_write, in_error = select.select(SERVER_LIST, [], [], 0)

        for sock in ready_to_read:
            # Indicates a new connection request:
            if sock == ser_socket:
                sockfd, addr = ser_socket.accept()
                SERVER_LIST.append(sockfd)

                print("Client: (%s, %s) " % addr)

                broadcast(ser_socket, sockfd, "[%s:%s] entered the chat.\n" % addr)

            # An already-present user does something.
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    # Is there any data present?
                    if data:
                        broadcast(ser_socket, sock, "\r" + '[' + str(sock.getpeername()) + ']' + data)
                    else:  # the socket is broken and needs to be removed.
                        if sock in SERVER_LIST:
                            SERVER_LIST.remove(sock)

                        broadcast(ser_socket, sock, "Client (%s, %s) has gone offline.\n" % addr)

                except:
                    broadcast(ser_socket, sock, "Client (%s, %s) has gone offline.\n" % addr)
                    continue

    ser_socket.close()


    def broadcast(ser_socket, sock, message):
        for socket in SERVER_LIST:
            if socket != sock and socket != sock:
                try:
                    socket.send(message)
                except:
                    socket.close()
                    if socket in SERVER_LIST:
                        SERVER_LIST.remove(socket)

if __name__ == "__main__":
    sys.exit(server())
