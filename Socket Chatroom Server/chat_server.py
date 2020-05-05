import socket
import select
# Select module gives us OS-level monitoring operations for things, including sockets.
# Remember there can only be '' inside "". Otherwise ther will be a syntax error.

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

# Set up the socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# To overcome "Address already in use"
# Set the socket option Reuse Addresss in the socket option level to true.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        # strip is use to remove the spaces.
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    # it will go into the except if the client breaks the script,
    # and ends the connection very agressively, or an empty message
    except:
        return False


while True: 
    # Parameters of the select.select are read list, write list and error list.
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # This means there is a new connection.
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted new connetion from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]