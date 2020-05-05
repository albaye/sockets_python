import socket

HEADERSIZE = 10
# create the socket
# AF_INET ==ipv4
# SOCK_STREAM == TCP (connection oriented)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server.
s.connect((socket.gethostname(), 1235))

# Use a while loop to be able to receive more than 1 message.
while True:
    full_msg = ''
    new_msg = True

    while True:
        # Use 16 bytes to receive a bit more than the header
        msg = s.recv(16)
        
        # If there is a new message, get the header to know the length of the message
        if new_msg:
            print(f"new message length : {msg[:HEADERSIZE]}")
            # With int, python ignores the spaces appended.
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        # if the full message is received, print it and emtpy the variable full_msg
        # also need to set new_msg to true, to be able to get the header of the ew message.
        if len(full_msg) - HEADERSIZE == msglen:
            print("full message received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''
            