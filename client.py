import socket

# create the socket
# AF_INET ==ipv4
# SOCK_STREAM == TCP (connection oriented)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server.
s.connect((socket.gethostname(), 1234))

# Use a while loop to be able to receive more than 1 message.
while True:
    full_msg = ''

    # Use a while loop to retrieve the whole msg.
    # No matter what buffer size we receive at a time
    # I may not be long enough.
    while True:
        # Attempt to receive data in buffer of 8 bytes at a time.
        msg = s.recv(8)
        # If message is finished, exit the while loop.
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")

    # Print the message if there is one.
    if len(full_msg) > 0:
        print(full_msg)