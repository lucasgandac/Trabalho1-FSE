import socket
import sys
from sensores import Sensores

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10101)
print ( 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    # Send data
    message = 'This is the message.  It will be repeated.'
    print ( 'sending "%s"' % message)
    #sock.sendall(message.encode('utf-8'))

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    read_sensor = Sensores("teste")
    msg = str(read_sensor.read_state())
    print(msg.encode('utf-8'))

    sock.sendall(msg.encode('utf-8'))
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print ( 'received "%s"' % data)

finally:
    print ( 'closing socket')
    sock.close()
