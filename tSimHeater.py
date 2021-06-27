class tSimHeater:
	# TODO: Expose Max Temp
	# TODO: Prompt for Max Temp with alternate constructor
	# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
	dictDefaulConfig = { 'Max': 500 ,'Units'  :"degF"}

	def __init__(self,dictConfig = dictDefaulConfig):
		print(f'tSimHeater(): INIT: PLEASE ENSURE HEATER IS TOGGLED OFF!')
		self.dictConfig = dictConfig
		self.dictSCADA = { 'toggle' : { 'val': 'Off', 'get': self.GetVal,'do': self.Toggle }}
	def Toggle(self):
		self.dictSCADA['toggle']['val'] = "On" if self.dictSCADA['toggle']['val'] == "Off" else "Off"
		return self.dictSCADA['toggle']['val']
	def GetVal(self):
		return self.dictSCADA['toggle']['val']
if __name__ == "__main__":
	def demo():
		oHeater = tSimHeater()
		print(f'HEATER: Config:    {oHeater.dictConfig["Max"]}, Units: {oHeater.dictConfig["Units"]}')
		print(f'HEATER: State:     {oHeater.dictSCADA["toggle"]["get"]()}')
		print(f'HEATER: Toggling   {oHeater.dictSCADA["toggle"]["do"]()}')
		print(f'HEATER: New State: {oHeater.dictSCADA["toggle"]["get"]()}')
		print(f'HEATER: Toggling   {oHeater.dictSCADA["toggle"]["do"]()}')
		print(f'HEATER: New State: {oHeater.dictSCADA["toggle"]["get"]()}')
	demo()
