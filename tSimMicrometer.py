from sys import dont_write_bytecode
from Utilities import LimitVal

class tSimMicrometer:
	dictDefaultConfig = { 'Min': 0, 'Max': 100, 'Units': 'mm'}
	def __init__(self, oDevToMeasure, dictConfig = dictDefaultConfig):
		# TODO: What if Min != 0
		print(f'tSimMicrometer(): INIT!')
		self.oDev = oDevToMeasure
		self.dictConfig = dictConfig
		self.dictSCADA = { 'pos': self.GetMeas }
	def GetMeas(self):
		return LimitVal(self.oDev.dictSCADA['pos'](), 
					    self.dictConfig['Min'],
						self.dictConfig['Max'])
	def GetUnits(self):
		return self.sUnits
if __name__ == "__main__":
	class tMMDevice:
		dictDefaultConfig = { 'Min': 0, 'Max': 10, 'Units': 'mm'}
		def __init__(self,dictConfig = dictDefaultConfig):
			self.dictConfig = dictConfig
			self.nVal = 0
			self.dictSCADA  = { 'pos': self.GetMeas}
		def GetMeas(self):
			self.nVal +=1
			return self.nVal
			
	def demo():
		oMMeter = tSimMicrometer(tMMDevice())
		for i in range(10):
			print(f"oMMeter: {oMMeter.dictSCADA['pos']()} {oMMeter.dictConfig['Units']}")
	demo()
