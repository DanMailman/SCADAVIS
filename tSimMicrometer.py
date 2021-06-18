from Utilities import LimitVal
from time import sleep
class tSimMicrometer:
	def __init__(self, oActuator, MinDiv, MaxDiv,sUnits):
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
	class tTestActuator:
		def __init__(self,nVal,sUnits):
			self.Meas = nVal
			self.sUnits = sUnits
		def GetMeas(self):
			return self.Meas
		def GetUnits(self):
			return self.sUnits
	def main():
		nTestVal = 50
		sTestUnits = "mm"
		oActuator = tTestActuator(nTestVal,sTestUnits)
		oMMeter = tSimMicrometer(oActuator,0,100,sTestUnits)
		print(f"oMMeter: {oMMeter.GetMeas()} {oMMeter.GetUnits()}: Expect: {nTestVal} {nTestVal}")
	main()
