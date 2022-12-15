import socket
import sys
from sensores import Sensores
import threading
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
central_adress = ('localhost', 10101)
#print ( 'connecting to %s port %s' % central_adress)
#sock.connect(central_adress)

FORMAT = 'utf-8'
ADDR = ('localhost', 10102)


class DistributedServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR) 

    def send_central(self):
        try:
            sock.connect(central_adress)
            while True:
                # Send data
                message = 'This is the message.  It will be repeated.'
                print ( 'sending "%s"' % message)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                read_sensor = Sensores()
                #read_sensor.change_state("AR")
                msg, teste = read_sensor.read_state()
                msg = str(msg)
                print(msg)
                print(msg.encode('utf-8'))

                sock.sendall(msg.encode('utf-8'))
                #while amount_received < amount_expected:
                    #data = sock.recv(1024)
                    #amount_received += len(data)
                    #print ( 'received "%s"' % data)
                time.sleep(2)
        finally:
            print ( 'closing socket')
            #sock.close()

    def start(self):
        print('Esperando conexão')
        self.server.listen()
        while True:
            connection, adress = self.server.accept()
            thread = threading.Thread(target=self.send_central, args=(connection, adress))
            thread.start()
            
distr_server = DistributedServer()
thread = threading.Thread(target=distr_server.send_central, args=[])
thread.start()
print('[STARTING] server is starting...')
distr_server.start()