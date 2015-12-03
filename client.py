import sys
import socket
import select


def client():
    if len(sys.argv) < 3:
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    # Receive input
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect to the chat.
    try:
        s.connect((host, port))
    except:
        print('Brandon did something wrong....')
        sys.exit()

    print("Connected to the chat. You can now start chatting.")
    sys.stdout.write('[Me] ');
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get list of sockets to read
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

        for sock in ready_to_read:
            if sock == s:
                # Get message from server
                data = sock.recv(4096)
                if not data:
                    print('\nYou have been disconnected from that chat.')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()
            else:
                # Send message.
                mes = sys.stdin.readline()
                s.send(mes)
                sys.stdout.write('[Me '); sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(client())
