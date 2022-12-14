import RPi.GPIO as gpio


class Sensores:
  
    LUZ_1 = 18
    LUZ_2 = 23
    AR = 24
    PROJ = 25
    ALARME = 8
    SPres = 7
    SFum = 1
    SJan = 12
    SPor = 16
    COUNT_IN = 20
    COUNT_OUT = 21
    DHT22 = 4
        
    def __init__(self, config) -> None:
        self.config = config

    def map_port(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.LUZ_1, gpio.OUT)
        gpio.setup(self.LUZ_2, gpio.OUT)
        gpio.setup(self.AR, gpio.OUT)
        gpio.setup(self.PROJ, gpio.OUT)
        gpio.setup(self.ALARME, gpio.OUT)
        gpio.setup(self.SPres, gpio.IN)
        gpio.setup(self.SFum, gpio.IN)
        gpio.setup(self.SJan, gpio.IN)
        gpio.setup(self.SPor, gpio.IN)
        gpio.setup(self.COUNT_IN, gpio.IN)
        gpio.setup(self.COUNT_OUT, gpio.IN)
        gpio.setup(self.DHT22, gpio.IN)

    def read_state(self):
        self.map_port()
        msg = {
            'LUZ_1': 'DESLIGADA',
            'LUZ_1': 'DESLIGADA',
            'AR': 'DESLIGADA',
            'PROJ': 'DESLIGADA',
            'ALARME': 'DESLIGADA'
        }
        countP = 0
    
        for i in range(1):
            if gpio.input(self.LUZ_1):
                msg["LUZ_1"] = "LIGADA"
            else:
                msg["LUZ_1"] = "DESLIGADA"
            if gpio.input(self.LUZ_2):
                msg["LUZ_2"] = "LIGADA"
            else:
                msg["LUZ_2"] = "DESLIGADA"
            if gpio.input(self.AR):
                msg["AR"] = "LIGADA"
            else:
                msg["AR"] = "DESLIGADA"
            if gpio.input(self.PROJ):
                msg["PROJ"] = "LIGADA"
            else:
                msg["PROJ"] = "DESLIGADA"
            if gpio.input(self.ALARME):
                msg["ALARME"] = "LIGADA"
            else:
                msg["ALARME"] = "DESLIGADA"
            if gpio.input(self.COUNT_IN):
                countP = countP + 1
            else:
                pass
            if gpio.input(self.COUNT_OUT):
                print("Alguem saiu no predio")
                if countP > 0 and countP != 0:
                    countP = countP - 1
            else:
                pass
            if gpio.input(self.SFum):
                print("Sensor de fumaça ligado")
            else:
                print("Sensor de fumaça desligado")
            if gpio.input(self.SJan):
                print("Janela aberta")
            else:
                print("Janela fechada")
            if gpio.input(self.SPor):
                print("Porta aberta")
            else:
                print("Porta fechada")
    
            return msg
            # print(f"Ha {countP} pessoas na sala")
            # msg_to_send = json.dumps(msg).encode("ascii")
            # sock.send(msg_to_send)
