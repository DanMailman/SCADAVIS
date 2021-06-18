from threading import Thread
from datetime import datetime as dt
from Utilities import SecondsSince
from time import sleep
from Utilities import tAverager, tSeqCounter

class tSimTempActuator(Thread):
	def __init__(self, eEndSim, oSeqCtr, oTherm, nMin, nMax, sUnits, nMinDeg, nMaxDeg, nHystSecs):
		print(f"ACTUATOR SIM: INIT.") 
		Thread.__init__(self)
		self.eEndSim = eEndSim
		self.oSeqCtr = oSeqCtr
		self.oTherm = oTherm
		self.nMin = nMin
		self.nMax = nMax
		self.sUnits = sUnits
		self.nMinDeg = nMinDeg
		self.nMaxDeg = nMaxDeg
		self.Slope = ( self.nMax  - self.nMin ) / ( self.nMaxDeg - self.nMinDeg )
		self.nHystSecs = nHystSecs
		self.nVal = nMin
		self.StartTime = dt.now()
		self.TempAverager = tAverager()
	def run(self):
		print(f"\t ACTUATOR SIM: PRE-LOOP: nHystSecs: {self.nHystSecs}.") 
		self.StartAvgTime = dt.now()
		self.TempAverager.add(self.oTherm.GetTemp())
		print(f"\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: ENTER.") 
		while True:
			if self.eEndSim.is_set(): 
				print(f"\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: END SIM: Break!") 
				break
			self.TempAverager.add(self.oTherm.GetTemp())
			if SecondsSince(self.StartAvgTime) >= self.nHystSecs:
				TempAvg = self.TempAverager.GetAvg()
				self.nVal = self.DegToDiv(TempAvg)
				self.TempAverager.start(TempAvg) # TODO: Consider oTherm.GetTemp()
				self.StartAvgTime = dt.now()
				print(f"\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): HYSTERISIS: nHystSecs: {self.nHystSecs}, AvgTemp: {int(TempAvg)}, DIVs: {self.nVal}.") 
			sleep (1)
		print(f'\t ACTUATOR SIM: tMicrometerSim(): T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: EXIT!')
	def DegToDiv(self,Deg):
		if Deg < self.nMinDeg: 
			Div = self.nMin
		elif Deg > self.nMaxDeg: 
			Div = self.nMax
		else:
			Div = int(self.nMin + (self.Slope * (Deg - self.nMinDeg)))
		# print(f'\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): DegToDiv({int(Deg)}): {Div}.')
		return Div
	def GetMeas(self):
		return self.nVal
if __name__ == "__main__":
	from threading import Event
	from tSimHeater import tSimHeater
	from tSimThermometer import tSimThermometer
	def main():
		print(f"ACTUATOR DEMO: ENTER.") 
		eEndSim = Event()
		eEndSim.clear()
		oSeqCtr = tSeqCounter()
		nHEATER_MAX  = 500; sHEATER_UNITS = "degF"
		oHeater = tSimHeater(nHEATER_MAX,sHEATER_UNITS)
		
		nAMBIENT_TEMPERATURE = 70; nTEMP_CHG_RATE = 2
		oTherm = tSimThermometer(oHeater, nAMBIENT_TEMPERATURE, nTEMP_CHG_RATE) # Gets max temp from heater

		
		nACTUATOR_MIN  = 0; nACTUATOR_MAX = 100; nACTUATOR_MIN_TEMP = 100; nACTUATOR_MAX_TEMP = 135
		nACTUATOR_HYST_SECS = 3; sACTUATOR_UNITS = "mm"
		oActuator = tSimTempActuator(eEndSim,oSeqCtr, oTherm,
									 nACTUATOR_MIN, nACTUATOR_MAX, sACTUATOR_UNITS,
									 nACTUATOR_MIN_TEMP, nACTUATOR_MAX_TEMP, nACTUATOR_HYST_SECS)
		oActuator.start()
		oHeater.Toggle()
		print(f'ACTUATOR DEMO: PRE-LOOP: HEATING: Temp: {oTherm.GetTemp()}, ACTUATOR: Meas: {oActuator.GetMeas()}')
		nStartCoolingTemp = 150; bCooling = False
		print(f"ACTUATOR DEMO: LOOP: ENTER.") 
		while True:
			Temp = oTherm.GetTemp()
			if (Temp >= oHeater.GetMaxTemp()) or (Temp >= nStartCoolingTemp):
				oHeater.Toggle() 
				bCooling = True
				tsStartCooling = dt.now()
				print(f'ACTUATOR DEMO: LOOP: START COOLING: Temp: {oTherm.GetTemp()}, ACTUATOR: Meas: {oActuator.GetMeas()}')
				
			if bCooling and (Temp <= nAMBIENT_TEMPERATURE) and (SecondsSince(tsStartCooling) > nACTUATOR_HYST_SECS): 
				print(f'ACTUATOR DEMO: LOOP: FINISHED COOLING: Temp: {oTherm.GetTemp()}, ACTUATOR: Meas: {oActuator.GetMeas()}')
				break
			print(f'ACTUATOR DEMO: T({oSeqCtr.GetSeqNum()}): {"Cooling" if bCooling else "Heating"}, Temp: {Temp}, ACTUATOR: Meas: {oActuator.GetMeas()}.')
			sleep(1)
			oSeqCtr.Increment()
		eEndSim.set()
		print(f"main(): ACTUATOR DEMO: RETURN.") 
		 
	main()