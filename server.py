import socket

# create the socket
# AF_INET ==ipv4
# SOCK_STREAM == TCP (connection oriented)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# For IP sockets, the address we bind to is a tuple of the hostname and the port number
# In this case port number is 1234
s.bind((socket.gethostname(), 1234))

# Make a queue of 5
# If full, it will reject connection
s.listen(5)

while True:
    # now our endpoint knows about the OTER end point.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    # Send 8 bit buffers, 1 per character.
    clientsocket.send(bytes("Hey there!!!", "utf-8"))
    # Close the socket
    clientsocket.close()
