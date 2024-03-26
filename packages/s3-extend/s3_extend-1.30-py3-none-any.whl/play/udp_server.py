import socket
import sys
import msgpack

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('192.168.2.104', 8830)
print(f'{sys.stderr} starting up on {server_address}')
sock.bind(server_address)

while True:
    print(f'\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print(f'received {len(data)} bytes from {address}')

    print(f'{data}')
    print(msgpack.unpackb(data, raw=False))
