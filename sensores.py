import RPi.GPIO as gpio
import time
import adafruit_dht
    
    
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
        

    def dht22(self):
        self.map_port()
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            data = "Temperatura:  {:.1f} C    Umidade: {}% ".format(temperature_c, humidity)
            return data
        
        except Exception as error:
            dhtDevice.exit()
            return "Nao foi possivel recolher temperatura e umidade"
    
    def read_state(self):
        self.map_port()
        msg = {
            'LUZ_1': 'DESLIGADA',
            'LUZ_2': 'DESLIGADA',
            'AR': 'DESLIGADA',
            'PROJ': 'DESLIGADA',
            'ALARME': 'DESLIGADA',
            'SPres': 'DESLIGADA',
            'SFum':'DESLIGADA',
            'SJan':'DESLIGADA',
            'SPor':'DESLIGADA'
        }
    
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
            if gpio.input(self.SFum):
                msg["SFum"] = "LIGADA"
            else:
                msg["SFum"] = "DESLIGADA"
            if gpio.input(self.SJan):
                msg["SJan"] = "LIGADA"
            else:
                msg["SJan"] = "DESLIGADA"
            if gpio.input(self.SPor):
                msg["SPor"] = "LIGADA"
            else:
                msg["SPor"] = "DESLIGADA"
            if gpio.input(self.SPres):
                msg["SPres"] = "LIGADA"
            else:
                msg["SPres"] = "DESLIGADA" 
            
            return msg
        
        
    def change_state(self, sensorName):
        self.map_port()
        dict = {
            "LUZ_1": 18,
            "LUZ_2": 23,
            "AR" : 24
        }
        print("Valor sensor:", dict[sensorName])
        porta = dict[sensorName]
        print(dict)
        if gpio.input(porta):
            gpio.output(porta, 0)
        else:
            gpio.output(porta, 1)