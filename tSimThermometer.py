from datetime import datetime as dt
from time import sleep
from Utilities import SecondsSince, LimitVal
class tSimThermometer:
    dictDefaultConfig = { 'MinTemp': -50, 'MaxTemp': 250, 'Units' : 'DegF', 'Ambient': 70, 'Rate':2 }
    def __init__(self, HTR, dictConfig = dictDefaultConfig):
        self.HTR = HTR
        self.dictConfig = dictConfig
        self.Temp = self.dictConfig['Ambient']
        self.LastReadTime = dt.now()
        self.dictSCADA = { 'temp': { 'get': self.GetTemp }}
        print("tSimThermomoter(): INIT: Time {} Temp: {}, Rate: {}".
              format(self.LastReadTime,
                     self.Temp,
                     self.dictConfig['Rate']))
    def GetTemp(self):
        NegPos = 1 if self.HTR.dictSCADA['toggle']['state'] == "On" else -1
        #print(f'tSimThermomoter(): GetTemp(): {} + ({} * {} * {}).'.format())
        self.Temp = int(round(self.Temp + 
                        (NegPos * 
                        self.dictConfig['Rate'] * 
                        SecondsSince(self.LastReadTime)),0))
        self.Temp = LimitVal(self.Temp,
                            self.dictConfig['Ambient'],
                            self.dictConfig['MaxTemp'])
        self.LastReadTime = dt.now()
        return self.Temp
if __name__ == "__main__":
    from tSimHeater import tSimHeater
    def demo():
        oTherm = tSimThermometer(tSimHeater()) 
        oTherm.HTR.dictSCADA['toggle']['do']()
        print(f'THERMOMETER: Temp: {oTherm.dictSCADA["temp"]["get"]()}')
        nStartCoolingTemp = 80; bCooling = False
        while True:
            print('THERMOMETER: {}, Temp: {}'.
                    format("Cooling" if bCooling else "Heating",
                           oTherm.dictSCADA['temp']['get']()))
            Temp = oTherm.dictSCADA['temp']['get']()
            if (Temp >= oTherm.dictConfig['MaxTemp']) or (Temp >= nStartCoolingTemp):
                oTherm.HTR.dictSCADA['toggle']['do']()
                bCooling = True
            if (bCooling and (Temp <= oTherm.dictConfig['Ambient'])) :
                break
            sleep(1)
        print(f"main(): Exit Thermometer Demo!")
    demo()