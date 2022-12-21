import json

class Mapping:
    
    connection_list = {
    "IP_CENTRAL" : None,
    "PORTA_CENTRAL" : None,
    "IP_DIST" : None,
    "PORTA_DIST" : None
}

    sensores_list = {
        "LUZ_1": None,
        "LUZ_2": None,
        "AR" : None,
        "PROJ" : None,
        "ALARME" : None,
        "SPres" : None,
        "SFum" : None,
        "SJan" : None,
        "SPor" : None,
        "COUNT_IN" : None,
        "COUNT_OUT" : None,
        "DHT22" : None
    }
    def __init__(self):
        self.valor = None
        self.f = None
        self.data = None

    def sendMapping(self, config):
        if(config==1):
            self.f = open('sala-01.json')
        elif(config==2):
            self.f = open('sala-02.json')
        elif(config==3):
            self.f = open('sala-03.json')
        self.data = json.load(self.f)
        return self.mapping(), self.connectData()


    def mapOutputs(self):
        self.sensores_list['LUZ_1'] = self.data['outputs'][0]['gpio']
        self.sensores_list['LUZ_2'] = self.data['outputs'][1]['gpio']
        self.sensores_list['PROJ'] = self.data['outputs'][2]['gpio']
        self.sensores_list['AR'] = self.data['outputs'][3]['gpio']
        self.sensores_list['ALARME'] = self.data['outputs'][4]['gpio']

    def mapInputs(self):
        self.sensores_list['SPres'] = self.data['inputs'][0]['gpio']
        self.sensores_list['SFum'] = self.data['inputs'][1]['gpio']
        self.sensores_list['SJan'] = self.data['inputs'][2]['gpio']
        self.sensores_list['SPor'] = self.data['inputs'][3]['gpio']
        self.sensores_list['COUNT_IN'] = self.data['inputs'][4]['gpio']
        self.sensores_list['COUNT_OUT'] = self.data['inputs'][5]['gpio']


    def mapTemp(self):
        self.sensores_list['DHT22'] = self.data['sensor_temperatura'][0]['gpio']

    def connectData(self):
        self.connection_list['IP_CENTRAL'] = self.data['ip_servidor_central']
        self.connection_list['PORTA_CENTRAL'] = self.data['porta_servidor_central']
        self.connection_list['IP_DIST'] = self.data['ip_servidor_distribuido']
        self.connection_list['PORTA_DIST'] = self.data['porta_servidor_distribuido']
        return self.connection_list

    def mapping(self):
        self.mapOutputs()
        self.mapInputs()
        self.mapTemp()
        return self.sensores_list