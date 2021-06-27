class tSimHeater:
	# TODO: Expose Max Temp
	# TODO: Prompt for Max Temp with alternate constructor
	# https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
	dictDefaulConfig = { 'Max': 500 ,'Units'  :"degF"}

	def __init__(self,dictConfig = dictDefaulConfig):
		print(f'tSimHeateConfig): INIT: PLEASE ENSURE HEATER IS TOGGLED OFF!')
		self.dictConfig = dictConfig
		self.dictSCADA = { 'toggle' : { 'state': 'Off', 'do': self.Toggle }}
	def Toggle(self):
		self.dictSCADA['toggle']['state'] = "On" if self.dictSCADA['toggle']['state'] == "Off" else "Off"
		#print(f'tSimHeater(): TOGGLED: {self.sOnOff}!.')

if __name__ == "__main__":
	def main():
		oHeater = tSimHeater()
		print(f'HEATER: Config: {oHeater.dictConfig["Max"]}, Units: {oHeater.dictConfig["Units"]}')
		print(f'HEATER: State: Toggle: {oHeater.dictSCADA["toggle"]["state"]}')
		print(f'HEATER: Toggling {oHeater.dictSCADA["toggle"]["do"]()}')
		print(f'HEATER: New State: {oHeater.dictSCADA["toggle"]["state"]}')
		print(f'HEATER: Toggling {oHeater.dictSCADA["toggle"]["do"]()}')
		print(f'HEATER: New State: {oHeater.dictSCADA["toggle"]["state"]}')
	main()
