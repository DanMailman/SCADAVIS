from datetime import datetime as dt
from time import sleep
from Utilities import SecondsSince, LimitVal
class tSimThermometer:
    dictDefaultConfig = { 'Min': -50, 'Max': 500, 'Units' : 'DegF', 'Ambient': 70, 'Rate': 3 }
    def __init__(self, oHeater, dictConfig = dictDefaultConfig):
        self.oHeater = oHeater
        self.dictConfig = dictConfig
        self.LastReadTime = dt.now()
        self.dictSCADA = { 'temp': { 'val': self.dictConfig['Ambient'], 'get': self.GetTemp }}
        print("tSimThermomoter(): INIT: Time {} Temp: {}, Rate: {}".
              format(int(round(SecondsSince(self.LastReadTime),0)),
                     self.dictSCADA['temp']['val'],
                     self.dictConfig['Rate']))
    def GetTemp(self):
        NegPos = 1 if self.oHeater.dictSCADA['toggle']['get']() == "On" else -1
        """ 
        print('tSimThermomoter(): GetTemp(): {} + ({} * {} * {}) ==>> {}.'
                .format(int(round(self.dictSCADA['temp']['val'],
                NegPos,self.dictConfig['Rate'],
                SecondsSince(self.LastReadTime))))) 
        """
        self.dictSCADA['temp']['val'] = int(round(self.dictSCADA['temp']['val'] + 
                        (NegPos * 
                        self.dictConfig['Rate'] * 
                        SecondsSince(self.LastReadTime)),0))
        self.dictSCADA['temp']['val'] = LimitVal(self.dictSCADA['temp']['val'],
                            self.dictConfig['Ambient'],
                            self.dictConfig['Max'])
        self.LastReadTime = dt.now()
        #print(f"tSimThermomoter(): {self.dictSCADA['temp']['val']}")
        return self.dictSCADA['temp']['val']
if __name__ == "__main__":
    from tSimHeater import tSimHeater
    def demo():
        oTherm = tSimThermometer(tSimHeater()) 
        oTherm.oHeater.dictSCADA['toggle']['do']()
        print(f'THERMOMETER: Temp: {oTherm.dictSCADA["temp"]["get"]()}')
        nStartCoolingTemp = 80; bCooling = False
        while True:
            print('THERMOMETER: {}, Temp: {}'.
                    format("Cooling" if bCooling else "Heating",
                           oTherm.dictSCADA['temp']['get']()))
            Temp = oTherm.dictSCADA['temp']['get']()
            if (Temp >= oTherm.dictConfig['Max']) or (Temp >= nStartCoolingTemp):
                oTherm.oHeater.dictSCADA['toggle']['do']()
                bCooling = True
            if (bCooling and (Temp <= oTherm.dictConfig['Ambient'])) :
                break
            sleep(1)
        print(f"main(): Exit Thermometer Demo!")
    demo()