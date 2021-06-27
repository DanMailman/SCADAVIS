from threading import Thread
from datetime import datetime as dt
from Utilities import SecondsSince
from time import sleep
from Utilities import tAverager, tSeqCounter

class tSimTempActuator(Thread):
		
	dictDefaultConfig = { 'MinPos': 0,   'MaxPos':  100, 'PosUnits': 'mm', 
	                      'MinTemp': 75, 'MaxTemp': 90, 'TempUnits': 'DegF', 'HystSecs': 3}
	def __init__(self, eEndSim, oSeqCtr, oTherm, dictConfig = dictDefaultConfig):
		print(f"ACTUATOR SIM: INIT.") 
		Thread.__init__(self)
		self.eEndSim = eEndSim; self.oSeqCtr = oSeqCtr; self.oTherm = oTherm
		self.dictConfig = dictConfig
        
		self.Slope = ( self.dictConfig['MaxPos']  - self.dictConfig['MinPos'] ) /\
		      		 ( self.dictConfig['MaxTemp'] - self.dictConfig['MinTemp'] )
		self.dictSCADA = { 'pos': { 'val': self.dictConfig['MinPos'], 'get': self.GetPos }}
		self.StartTime = dt.now()
		self.TempAverager = tAverager()
	def run(self):
		print(f"\t ACTUATOR SIM: PRE-LOOP: nHystSecs: {self.dictConfig['HystSecs']}.") 
		self.StartAvgTime = dt.now()
		self.TempAverager.add(self.oTherm.GetTemp())
		print(f"\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: ENTER.") 
		while True:
			if self.eEndSim.is_set(): 
				print(f"\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: END SIM: Break!") 
				break
			self.TempAverager.add(self.oTherm.GetTemp())
			if SecondsSince(self.StartAvgTime) >= self.dictConfig['HystSecs']:
				TempAvg = self.TempAverager.GetAvg()
				self.dictSCADA['pos']['val'] = self.DegToDiv(TempAvg)
				self.TempAverager.start(TempAvg) # TODO: Consider oTherm.GetTemp()
				self.StartAvgTime = dt.now()
				print("\t ACTUATOR SIM: T({}): HYSTERESIS: {} Secs, AvgTemp: {}, POS: {}.".
						format(self.oSeqCtr.GetSeqNum(),
						       self.dictConfig['HystSecs'],
							   int(TempAvg),
							   self.dictSCADA['pos']['get']())) 
			sleep (1)
		print(f'\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): THREADED LOOP: EXIT!')
	def GetPos(self):
		return self.dictSCADA['pos']['val']
	def DegToDiv(self,Deg):
		if Deg < self.dictConfig['MinTemp']: 
			Div = self.dictConfig['MinPos']
		elif Deg > self.dictConfig['MaxTemp']:
			Div = self.dictConfig['MaxPos']
		else:
			Div = int(self.dictConfig['MinPos'] + (self.Slope * (Deg - self.dictConfig['MinTemp'])))
		# print(f'\t ACTUATOR SIM: T({self.oSeqCtr.GetSeqNum()}): DegToDiv({int(Deg)}): {Div}.')
		return Div
if __name__ == "__main__":
	from threading import Event
	from tSimHeater import tSimHeater
	from tSimThermometer import tSimThermometer
	def demo():
		print(f"ACTUATOR DEMO: ENTER.") 
		eEndSim = Event() ; eEndSim.clear(); oSeqCtr = tSeqCounter()
		oActuator = tSimTempActuator(eEndSim,oSeqCtr, tSimThermometer(tSimHeater()))
		oActuator.start()
		oActuator.oTherm.oHeater.Toggle()
		GET_TEMP = oActuator.oTherm.dictSCADA['temp']['get']
		def GET_POS(): return oActuator.dictSCADA['pos']['get']()
		print(f'ACTUATOR DEMO: PRE-LOOP: HEATING: Temp: {GET_TEMP()}, ACTUATOR: Meas: {GET_POS()}')
		nStartCoolingTemp = 150; bCooling = False
		print(f"ACTUATOR DEMO: LOOP: ENTER.") 
		while True:
			Temp = GET_TEMP()
			if (Temp >= oActuator.dictConfig['MaxTemp']) or (Temp >= nStartCoolingTemp):
				oActuator.oTherm.oHeater.Toggle() 
				bCooling = True
				tsStartCooling = dt.now()
				print(f'ACTUATOR DEMO: LOOP: START COOLING: Temp: {GET_TEMP()}, ACTUATOR: Meas: {GET_POS()}')
				
			if bCooling and (Temp <= oActuator.oTherm.dictConfig['Ambient']) and (SecondsSince(tsStartCooling) > oActuator.dictConfig['HystSecs']): 
				print(f'ACTUATOR DEMO: LOOP: FINISHED COOLING: Temp: {GET_TEMP()}, ACTUATOR: Meas: {GET_POS()}')
				break
			print('ACTUATOR DEMO: T({}): {}, Temp: {}, ACTUATOR: Meas: {}.'.
				 format(oSeqCtr.GetSeqNum(), "Cooling" if bCooling else "Heating",Temp, GET_POS()))
			sleep(1)
			oSeqCtr.Increment()
		eEndSim.set()
		print(f"main(): ACTUATOR DEMO: RETURN.") 
		 
	demo()