import socket
import sys
from sensores import Sensores
import threading
import time
import json 
from socket import error as SocketError
import errno
import difflib
import argparse
from read_json import Mapping


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
central_adress = ('localhost', 10101)
#print ( 'connecting to %s port %s' % central_adress)
#sock.connect(central_adress)

FORMAT = 'utf-8'
ADDR = ('localhost', 10102)

parser = argparse.ArgumentParser()
parser.add_argument('--arg', type=int, required=True, help='An integer argument for the class')
args = parser.parse_args()

#mapeamento = Mapping()
#map_portas, map_conexao = mapeamento.sendMapping(args.arg)
#print(map_conexao)

class DistributedServer:
    def __init__(self, arg) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR) 
        self.arg = arg

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

                read_sensor = Sensores(args.arg)
                #read_sensor.change_state("AR")
                msg = read_sensor.read_state()
                msg = json.dumps(msg)
                #print(msg)
                #print(msg.encode('utf-8'))

                sock.sendall(msg.encode('utf-8'))
                print("\n\n\n")
                #args = parser.parse_args()
                print(args)
                #print(msg)
                print("\n\n\n")
                #while amount_received < amount_expected:
                    #data = sock.recv(1024)
                    #amount_received += len(data)
                    #print ( 'received "%s"' % data)
                #time.sleep(2)
        finally:
            print ( 'closing socket')
            #sock.close()

    def handle_client(self, connection, adress):
        try:
            print(f'Conexão de {adress}')
            while True:
                data = connection.recv(1024)
                data = data.decode("utf-8")
                data = data[1:-1]
                var = "oi"
                controla_sensor = Sensores(args.arg)
                #print ('received "%s"' % data)
                if data:
                    print(data)
                    controla_sensor.change_state(data)
                    #for i,s in enumerate(difflib.ndiff(var, data)):
                        #print(s[0], s[-1], i)
                    #connection.sendall(data('utf-8'))
                    #dados = controla_sensor.read_state()
                    #connection.sendall(dados)
                else:
                    print ('Sem mais conexão', adress)
                    break
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise
            pass

    def start(self):
        print('Esperando conexão')
        self.server.listen()
        while True:
            connection, adress = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, adress))
            thread.start()
            
distr_server = DistributedServer(args.arg)
thread = threading.Thread(target=distr_server.send_central, args=[])
thread.start()
print('[STARTING] server is starting...')
distr_server.start()
