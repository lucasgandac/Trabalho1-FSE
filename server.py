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

FORMAT = "utf-8"
ADDR = ("localhost", 10101)
dados = {
    "LUZ_1": "DESLIGADO",
    "LUZ_2": "DESLIGADO",
    "AR": "DESLIGADO",
    "PROJ": "DESLIGADO",
    "TEMP" : "Ainda não foi realizada a leitura"}

class CentralServer:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
    
    #dados = "Não possui dados ainda"
    #q = Queue()

    def send_command(self, command):
        ADDR_DIST =  ("localhost", 10102)
        sock_dist = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_dist.connect(ADDR_DIST)
        msg = command
        msg = json.dumps(msg)
        sock_dist.sendall(msg.encode("utf-8"))

    def handle_client(self, connection, adress):
        global dataReceive 
        try:
            print(f"Conexão de {adress}")
            while True:
                    data = connection.recv(1024)
                    #print ("received "%s"" % data)
                    if data:
                        #print ("sending data back to the client")
                        #print(self.data)
                        #data =data.replace("'", '"')
                        #print(data)
                        dataFormat = data.decode("utf-8")
                        dataFormat = dataFormat.partition("}")[0]
                        dataReceive = dataFormat + '}'
                        #print("\n\n\n")
                        #print(dataReceive)
                        #print("\n\n\n")                        
                        #print(dados)
                        #print(dados)
                        #print(data)
                        #self.q.put(data.decode("utf-8")    )
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
            connection, adress = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, adress))
            thread.start()
            central_server.menu()

    def formata_valores(self, dados):
            dados = json.loads(dados)
            print(type(dados))
            
            print("-----------------", dados, "-----------")
            print("-------------------------------------------------")
            print("|   Código   |      Sensor     |     Estado    |\n")
            print("|------------|-----------------|---------------|\n")
            print("|   LUZ_1   |      Luz 01     |   ", dados["LUZ_1"],"     |\n")
            print("|   LUZ_2   |      Luz 02     |   ", dados["LUZ_2"],"     |\n")
            print("|     AR     | Ar Condicionado |   ", dados["AR"],"     |\n")
            print("|    PROJ    |     Projetor    |   ", dados["PROJ"],"     |\n")
            print("|  Temp e Umid   |   ", dados["TEMP"],"     |\n")
            print("|  Pessoas na Sala   |   ", dados["PES"],"     |\n")

        
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
            while option != "1" and option != "2":
                option = input("Opção inválida.\n\n")
            if option == "1":
                #comando = input("Digite o nome do sensor que deseja ligar ou desligar \n")
                #dados_sensor = self.send_command(comando)
                current_time = datetime.datetime.now()
                self.logging("Atualizou a visualizacao dos dados: ", current_time) 
                self.formata_valores(dataReceive)
                #print(dataReceive)
                #dataReceive = None
                #print("\n\n\n")
            elif option == "2":
                comando = input("Digite o código do sensor que deseja ligar ou desligar \n")
                dados_sensor = self.send_command(comando)
                current_time = datetime.datetime.now()
                msg = "Acionou o sensor " + comando + " "
                self.logging(msg, current_time)
                time.sleep(1)
                self.formata_valores(dataReceive)

central_server = CentralServer()
#thread = threading.Thread(target=central_server.menu, args=[])
#thread.start()
#print("[STARTING] server is starting...")
central_server.start()
