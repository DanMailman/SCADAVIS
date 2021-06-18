class tSimHeater:
	# TODO: Expose Max Temp
	# TODO: Prompt for Max Temp with alternate constructor
	# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
	def __init__(self,nMaxTemp,sUnits):
		print(f'tSimHeater(): INIT: PLEASE ENSURE HEATER IS TOGGLED OFF!')
		self.OnOff = "Off"
		self.nMaxTemp = nMaxTemp
		self.sUnits = sUnits
	def Toggle(self):
		self.OnOff = "On" if self.OnOff == "Off" else "Off"
		#print(f'tSimHeater(): TOGGLED: {self.OnOff}!.')
	def State(self):
		return self.OnOff
	def GetMaxTemp(self):
		return self.nMaxTemp

if __name__ == "__main__":
	def main():
		nHEATER_MAX  = 500; sHEATER_UNITS = "degF"
		oHeater = tSimHeater(nHEATER_MAX,sHEATER_UNITS)
		print(f'HEATER: Max Temp: {oHeater.GetMaxTemp()}')
		print(f'HEATER: Initial State: {oHeater.State()}')
		print(f'HEATER: Toggling {oHeater.Toggle()}')
		print(f'HEATER: New State: {oHeater.State()}')
		print(f'HEATER: Toggling {oHeater.Toggle()}')
		print(f'HEATER: New State: {oHeater.State()}')
	main()
