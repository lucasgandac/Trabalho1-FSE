import RPi.GPIO as gpio
import time
import adafruit_dht
    
    
class Sensores:
    
    sensores_list = {
        "LUZ_1": 18,
        "LUZ_2": 23,
        "AR" : 24,
        "PROJ" : 25,
        "ALARME" : 8,
        "SPres" : 7,
        "SFum" : 1,
        "SJan" : 12,
        "SPor" : 16,
        "COUNT_IN" : 20,
        "COUNT_OUT" : 21,
        "DHT22" : 4
    }
        
    def __init__(self) -> None:
        self.sensores_list = self.sensores_list

    def map_port(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.sensores_list['LUZ_1'], gpio.OUT)
        gpio.setup(self.sensores_list['LUZ_2'], gpio.OUT)
        gpio.setup(self.sensores_list['AR'], gpio.OUT)
        gpio.setup(self.sensores_list['PROJ'], gpio.OUT)
        gpio.setup(self.sensores_list['ALARME'], gpio.OUT)
        gpio.setup(self.sensores_list['SPres'], gpio.IN)
        gpio.setup(self.sensores_list['SFum'], gpio.IN)
        gpio.setup(self.sensores_list['SJan'], gpio.IN)
        gpio.setup(self.sensores_list['SPor'], gpio.IN)
        gpio.setup(self.sensores_list['COUNT_IN'], gpio.IN)
        gpio.setup(self.sensores_list['COUNT_OUT'], gpio.IN)
        gpio.setup(self.sensores_list['DHT22'], gpio.IN)
        

    def dht22(self):
        self.map_port()
        dhtDevice = adafruit_dht.DHT22(self.sensores_list['DHT22'], use_pulseio=False)
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
            'LUZ_1': 'DESLIGADO',
            'LUZ_2': 'DESLIGADO',
            'AR': 'DESLIGADO',
            'PROJ': 'DESLIGADO',
            'ALARME': 'DESLIGADO',
            'SPres': 'DESLIGADO',
            'SFum':'DESLIGADO',
            'SJan':'DESLIGADO',
            'SPor':'DESLIGADO'
        }
    
        for key, value in self.sensores_list.items():
            if (key == 'COUNT_IN' or key == 'COUNT_OUT' or key == 'DHT22'):
                pass
            elif gpio.input(value):
                msg[key] = "LIGADO"
            else:
                msg[key] = "DESLIGADO"
        self.dht22()
        teste = "oi"
        return msg, teste
        
        
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