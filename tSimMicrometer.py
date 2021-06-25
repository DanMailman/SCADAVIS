from Utilities import LimitVal

class tSimMicrometer:
	def __init__(self, oActuator, MinDiv, MaxDiv,sUnits):
		# TODO: What if Min != 0
		print(f'tSimMicrometer(): INIT!')
		self.oActuator = oActuator
		self.MinDiv	= MinDiv
		self.MaxDiv = MaxDiv
		self.sUnits = sUnits
	def GetMeas(self):
		return LimitVal(self.oActuator.GetMeas(), self.MinDiv,self.MaxDiv)
	def GetUnits(self):
		return self.sUnits
if __name__ == "__main__":
	from threading import Event
	from tSimHeater import tSimHeater
	from tSimThermometer import tSimThermometer
	from Utilities import tSeqCounter
	class tMMDevice:
		from Utilities import LimitVal
		def __init__(self,nMin,nMax,sUnits):
			self.nMin = nMin
			self.nMax = nMax
			self.nVal = nMin
			self.sUnits = sUnits
		def GetMeas(self):
			self.nVal +=1
			return self.nVal
			
	def main():
		nMin = 0; nMax = 10; nCnt = nMin
		sUnits = 'mm'
		oMMDevice = tMMDevice(nMin,nMax,sUnits)
		oMMeter = tSimMicrometer(oMMDevice,nMin,nMax,sUnits)
		oMMeter.GetUnits()
		while nCnt < nMax:
			nCnt +=1
			print(f"oMMeter: {oMMeter.GetMeas()} {oMMeter.GetUnits()}")
	main()
