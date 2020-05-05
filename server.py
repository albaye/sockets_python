import socket
import time

HEADERSIZE = 10
# create the socket
# AF_INET ==ipv4
# SOCK_STREAM == TCP (connection oriented)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# For IP sockets, the address we bind to is a tuple of the hostname and the port number
# In this case port number is 1234
s.bind((socket.gethostname(), 1235))

# Make a queue of 5
# If full, it will reject connection
s.listen(5)

while True:
    # now our endpoint knows about the OTER end point.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = "Welcome to the server!"
    # The first part of the msg is a header.
    # the :<20 will append spaces at the end of the length (left align())
    # in this case msg has length 22, hence 8 spaces will be appended
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    # Send 8 bit buffers, 1 per character.
    clientsocket.send(bytes(msg, "utf-8"))

    while True:
        # Send a message every 3 seconds
        time.sleep(3)
        msg = f"The time is: {time.time()}"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
    