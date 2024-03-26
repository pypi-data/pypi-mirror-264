import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8830)
message = 'This is the message.  It will be repeated.'
my_str_as_bytes = str.encode(message)

try:

    # Send data
    print(f'sending {message}')
    sent = sock.sendto(my_str_as_bytes, server_address)

    # Receive response
    while True:
        print('waiting to receive')
        data, server = sock.recvfrom(4096)
        print(f'received {data.decode()}')

finally:
    print('closing socket')
    sock.close()
