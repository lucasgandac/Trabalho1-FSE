import RPi.GPIO as gpio
import time
import adafruit_dht
import board 
from read_json import Mapping


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
        
    def __init__(self, arg) -> None:
        self.sensores_list = self.sensores_list
        self.arg = arg


    mapeamento = Mapping()

    def map_port(self):
        map_portas, map_conexao = self.mapeamento.sendMapping(int(self.arg))
        self.sensores_list = map_portas
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
        if(self.sensores_list['DHT22'] == 4):
            dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        elif(self.sensores_list['DHT22'] == 18):
            dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
        try:
            time.sleep(2)
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            data = "Temp:  {:.1f} C    Umidade: {}% ".format(temperature_c, humidity)
            return data
        
        except Exception as error:
            dhtDevice.exit()
            #print(error)
            return "Atualize por favor"
    
    def read_state(self):
        self.map_port()
        msg = {
            "LUZ_1": "DESLIGADO",
            "LUZ_2": "DESLIGADO",
            "AR": "DESLIGADO",
            "PROJ": "DESLIGADO",
            "ALARME": "DESLIGADO",
            "SPres": "DESLIGADO",
            "SFum":"DESLIGADO",
            "SJan":"DESLIGADO",
            "SPor":"DESLIGADO"
        }
    
        for key, value in self.sensores_list.items():
            if (key == "COUNT_IN" or key == "COUNT_OUT" or key == "DHT22"):
                pass
            elif gpio.input(value):
                msg[key] = "LIGADO"
            else:
                msg[key] = "DESLIGADO"
        time.sleep(0.2)
        entr = gpio.input(self.sensores_list["COUNT_IN"])
        sai = gpio.input(self.sensores_list["COUNT_OUT"])
        dht = self.dht22()
        print(dht)
        msg["TEMP"] = dht
        return msg, entr, sai
        
        
    def change_state(self, sensorName):
        self.map_port()
        try:
            porta = self.sensores_list[sensorName]
            if gpio.input(porta):
                gpio.output(porta, 0)
            else:
                gpio.output(porta, 1)
        except:
            return "Não foi possível ligar"

    def turnAll_On(self):
        self.map_port()
        try:
            gpio.output(self.sensores_list['LUZ_1'], 1)
            gpio.output(self.sensores_list['LUZ_2'], 1)
            gpio.output(self.sensores_list['AR'], 1)
            gpio.output(self.sensores_list['PROJ'], 1)
        except:
            return "Não foi possível ligar"
        
    def turnAll_Off(self):
        self.map_port()
        try:
            gpio.output(self.sensores_list['LUZ_1'], 0)
            gpio.output(self.sensores_list['LUZ_2'], 0)
            gpio.output(self.sensores_list['AR'], 0)
            gpio.output(self.sensores_list['PROJ'], 0)
        except:
            return "Não foi possível ligar"