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
central_adress = ("164.41.98.28", 10101)
#print ( 'connecting to %s port %s' % central_adress)
#sock.connect(central_adress)

FORMAT = 'utf-8'
#ADDR = ("164.41.98.28", 10102)

parser = argparse.ArgumentParser()
parser.add_argument('--arg', type=int, required=True, help='An integer argument for the class')
args = parser.parse_args()

mapeamento = Mapping()
por, con = mapeamento.sendMapping(int(args.arg))
port_central = con['PORTA_CENTRAL']
port_distr = con['PORTA_DIST']
ip_central = str(con['IP_CENTRAL'])
ip_dist = str(con['IP_DIST'])


central_adress = (ip_central, port_central)
ADDR = (ip_dist, port_distr)

#mapeamento = Mapping()
#map_portas, map_conexao = mapeamento.sendMapping(args.arg)
#print(map_conexao)

class DistributedServer:
    def __init__(self, arg) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arg = arg
        self.server.bind(ADDR) 
        
    numPessoas = 0

    def countPeople(self, c_in, c_out):
        if(c_in==1):
            print("Entraro")
            self.numPessoas = self.numPessoas + 1
        if(c_out==1):
            if(self.numPessoas > 0):
                self.numPessoas = self.numPessoas - 1
            print("Sairo")
        return self.numPessoas
    
    def send_central(self):
        try:
            sock.connect(central_adress)
            while True:
                # Send data

                # Look for the response
                amount_received = 0

                read_sensor = Sensores(args.arg)
                #read_sensor.change_state("AR")
                msg, entr, sai = read_sensor.read_state()
                numP = self.countPeople(entr, sai)
                print(self.numPessoas)
                js = {
                    "PESSOAS" : numP
                }
                id = ip_dist + ':' + str(port_distr)
                print(id)
                #print(type(msg))
                #print(msg)
                msg['PES'] = str(numP)
                msg['ID'] = id
                msg = json.dumps(msg)
                print(msg)
                sock.sendall(msg.encode('utf-8'))
                print("\n")
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
                    if(data=="LIGA"):
                        controla_sensor.turnAll_On()
                    elif(data=="DESLIGA"):
                        controla_sensor.turnAll_Off()
                    else:
                        controla_sensor.change_state(data)
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
