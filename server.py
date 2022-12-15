from datetime import datetime
import json
import socket
import threading
import time
from socket import error as SocketError
import errno

FORMAT = 'utf-8'
ADDR = ('localhost', 10101)

class CentralServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR) 

    def handle_client(self, connection, adress):
        try:
            print(f'Conexão de {adress}')
            while True:
                data = connection.recv(1024)
                #print ('received "%s"' % data)
                if data:
                    print ('sending data back to the client')
                    connection.sendall(data)
                else:
                    print ('Sem mais conexão', adress)
                    break
                time.sleep(2)
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise            
            print("Distribuído disconectado")
            pass


    def start(self):
        print('Esperando conexão')
        self.server.listen()
        while True:
            connection, adress = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, adress))
            thread.start()

    def menu(self):
        while True:
            option = input('Qual andar deseja controlar ou monitorar:\n1. Primeiro Andar\n2. Segundo Andar\n\n')
            while option != '1' and option != '2' and option != '3' and option != '4' and option != '5':
                option = input('Opção inválida. Digite uma das seguintes opções:\n1. Primeiro Andar\n2. Segundo Andar\n\n')
            if option == '1':
                print(f'Medição dos sensores:')
            elif option == '2':
                print(f'Qual sensor deve ser acionado ? \n')


central_server = CentralServer()
thread = threading.Thread(target=central_server.menu, args=[])
thread.start()
print('[STARTING] server is starting...')
central_server.start()
