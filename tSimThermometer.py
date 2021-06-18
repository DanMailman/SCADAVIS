from datetime import datetime as dt
from time import sleep
from tSimHeater import tSimHeater
from Utilities import SecondsSince
class tSimThermometer:
    def __init__(self, HTR, AmbientTemp, DegPerSec):
        self.HTR = HTR
        self.AmbientTemp = AmbientTemp
        self.HeaterTemp = self.HTR.GetMaxTemp()
        self.DegPerSec = DegPerSec
        self.Temp = self.AmbientTemp
        self.LastReadTime = dt.now()
        print(f'tSimThermomoter(): INIT: Time {self.LastReadTime}, Temp:{self.Temp}, Rate: {self.DegPerSec}')
    def GetTemp(self):
        NegPos = 1 if self.HTR.State() == "On" else -1
        #print(f'tSimThermomoter(): GetTemp(): {self.Temp} + ({NegPos} * {self.DegPerSec} * {int(SecondsSince(self.LastReadTime))}).')
        Temp = int(self.Temp + (NegPos * self.DegPerSec * SecondsSince(self.LastReadTime)))
        if (NegPos == 1) and (Temp >= self.HeaterTemp):
            self.Temp = self.HeaterTemp
        elif (NegPos == -1) and (Temp <= self.AmbientTemp):
            self.Temp = self.AmbientTemp
        else:
            self.Temp = Temp
        self.LastReadTime = dt.now()
        return self.Temp
if __name__ == "__main__":
    def main():
        nHEATER_MAX  = 500; sHEATER_UNITS = "degF"
        nAMBIENT_TEMPERATURE = 70; nTEMP_CHG_RATE = 2 
        oHeater = tSimHeater(nHEATER_MAX,sHEATER_UNITS)
        oHeater.Toggle()
        oThermometer = tSimThermometer(oHeater, nAMBIENT_TEMPERATURE, nTEMP_CHG_RATE) # Gets max temp from heater
        print(f'THERMOMETER: Temp: {oThermometer.GetTemp()}')
        nStartCoolingTemp = 80; bCooling = False
        while True:
            Temp = oThermometer.GetTemp()
            if (Temp >= oHeater.GetMaxTemp()) or (Temp >= nStartCoolingTemp):
                oHeater.Toggle() 
                bCooling = True
            print(f'THERMOMETER: {"Cooling" if bCooling else "Heating"}, Temp: {Temp}')
            if bCooling and (Temp <= nAMBIENT_TEMPERATURE): break
            sleep(1)
        print(f"main(): Exit Thermometer Demo!")
    main()