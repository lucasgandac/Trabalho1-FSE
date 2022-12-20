from datetime import datetime
import json
import socket
import threading
import datetime
from socket import error as SocketError
import errno
from queue import Queue
import ast
import time
from read_json import Mapping
from _thread import *
mapeamento = Mapping()
por, con = mapeamento.sendMapping(1)
port_central = con['PORTA_CENTRAL']
ip_central = str(con['IP_CENTRAL'])

FORMAT = "utf-8"
ADDR = (ip_central, port_central)
dados = {
    "LUZ_1": "DESLIGADO",
    "LUZ_2": "DESLIGADO",
    "AR": "DESLIGADO",
    "PROJ": "DESLIGADO",
    "TEMP" : "Ainda não foi realizada a leitura"}

distribuidos = []

class CentralServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
    
    #dados = "Não possui dados ainda"
    #q = Queue()

    def send_command(self, command, sala):
        print(sala)
        distObj = distribuidos[int(sala)]
        distObj = distObj['ID']
        print(distObj)
        splitAdress = distObj.split(':')
        ip = splitAdress[0]
        port = int(splitAdress[1])
        #ADDR_DIST =  ("164.41.98.28", 10102)
        ADDR_DIST =  (ip, port)
        sock_dist = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_dist.connect(ADDR_DIST)
        msg = command
        msg = json.dumps(msg)
        sock_dist.sendall(msg.encode("utf-8"))
    
    def verificaDistribuido(self, dados):
        found = 0
        dados = json.loads(dados)
        for idx, dis in enumerate(distribuidos): 
            if(dis['ID'] == dados['ID']):
                distribuidos[idx] = dados
                #distribuidos.pop(idx)
                #distribuidos.append(dados)
                found = 1
        if(found==0):
            distribuidos.append(dados)
            
    
    def handle_client(self, connection, adress):
        global dataReceive 
        try:
            print("Distibuído conectado")
            while True:
                    data = connection.recv(1024)
                    #print ("received "%s"" % data)
                    if data:
                        dataFormat = data.decode("utf-8")
                        dataFormat = dataFormat.partition("}")[0]
                        dataReceive = dataFormat + '}'
                        teste = self.verificaDistribuido(dataReceive)
                        connection.sendall(data)
                    else:
                        print ("Sem mais conexão", adress)
                        break
                    time.sleep(2)
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise            
            print("Distribuído disconectado")
            pass


    def start(self):
        print("Esperando conexão")
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.handle_client, (connection,address ))
            #central_server.menu()
            
            
    def formata_valores(self):
            for idx, sala in enumerate(distribuidos):
                print("\n-------------------- Sala", idx, "---------------------")
                print("-------------------------------------------------")
                print("|   Código   |      Sensor     |     Estado    |\n")
                print("|------------|-----------------|---------------|\n")
                print("|   LUZ_1   |      Luz 01     |   ", sala["LUZ_1"],"     |\n")
                print("|   LUZ_2   |      Luz 02     |   ", sala["LUZ_2"],"     |\n")
                print("|     AR     | Ar Condicionado |   ", sala["AR"],"     |\n")
                print("|    PROJ    |     Projetor    |   ", sala["PROJ"],"     |\n")
                print("|  Temp e Umid  |  ", sala["TEMP"],"  |\n")
                print("|  Pessoas na Sala   |   ", sala["PES"],"     |\n")

        
    def logging(self, msg, time):
        with open('log.txt', 'a') as f:
            cm = msg + "as " + str(time)
            f.write(cm + '\n')


    def menu(self):
        while True:
            #shared_variable = self.q.get()
            #print(shared_variable)
            #self.formata_valores(self.dataReceive)
            #print(dataReceive)
            option = input("Qual ação deseja efetuar:\n1. Visualizar sensores\n2. Ativar ou desativar sensor\n")
            print("Há um delay para refletir os valores reais, especialmente temperatura\n\n")
            #self.formata_valores(self.dataReceive)
            while option != "1" and option != "2" and option != "3":
                option = input("Opção inválida.\n\n")
            if option == "1":
                #comando = input("Digite o nome do sensor que deseja ligar ou desligar \n")
                #dados_sensor = self.send_command(comando)
                current_time = datetime.datetime.now()
                self.logging("Atualizou a visualizacao dos dados: ", current_time) 
                self.formata_valores()
                #print(dataReceive)
                #dataReceive = None
                #print("\n\n\n")
            elif option == "2":
                sala = input("Digite a sala que deseja controlar \n")
                if sala.isdigit() and int(sala) < len(distribuidos):
                    comando = input("Digite o código do sensor que deseja ligar ou desligar \n")
                    dados_sensor = self.send_command(comando, sala)
                    current_time = datetime.datetime.now()
                    msg = "Acionou o sensor " + comando + " "
                    self.logging(msg, current_time)
                    time.sleep(1)
                    self.formata_valores()
                else:
                    print("Sala invalida \n")
            elif option == '3':
                print(len(distribuidos))
                for x in distribuidos:
                    print(x)

central_server = CentralServer()
thread = threading.Thread(target=central_server.menu, args=[])
thread.start()
print("[STARTING] server is starting...")
central_server.start()
