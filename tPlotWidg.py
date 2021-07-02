from tkinter import Tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Utilities import DoZoom, OnLinux, tSeqCounter

dictDefaults = {'Cfg'    : {'InchH': 3.5, 'InchW':4,'DPI': 100, 'Style': 'ggplot'},
                'X-Axis' : { 'Name': 'Sequence', 'GetVals': tSeqCounter().IncSeqList, 'LoLim': 0, 'HiLim': 10},
                'Y-Vects': [{'Name': 'Y1', 'GetVals': tSeqCounter().IncSeqList, 'LoLim': 0, 'HiLim': 10,'Color':'red',  'Marker':'o'},
                            {'Name': 'Y2', 'GetVals': tSeqCounter(start_at = 1).IncSeqList, 'LoLim': 0, 'HiLim': 10,'Color':'blue', 'Marker':'o'}]}
class tPlotWidg:
    def __init__(self,root,dctCfg = dictDefaults):
        self.root = root
        self.dctCfg = dctCfg		
        self.fig = plt.figure(figsize=(self.dctCfg['Cfg']['InchW'],
                                       self.dctCfg['Cfg']['InchH']),
                             dpi=self.dctCfg['Cfg']['DPI'])
        self.PlotCanvas = FigureCanvasTkAgg(self.fig,self.root)
        style.use(self.dctCfg['Cfg']['Style'])
        self.SubPlot = self.fig.add_subplot(1,1,1)
        self.minX = self.dctCfg['X-Axis']['LoLim']
        self.maxX = self.dctCfg['X-Axis']['HiLim']
        self.minY = 0; self.maxY = 0
        for idx in range(len(self.dctCfg['Y-Vects'])):
            oPlot, = self.SubPlot.plot([],[],'o')
            self.dctCfg['Y-Vects'][idx]['Plot'] = oPlot
            self.minY = min(self.minY,self.dctCfg['Y-Vects'][idx]['LoLim'])
            self.maxY - max(self.maxY,self.dctCfg['Y-Vects'][idx]['HiLim'])
    def Update(self):
        def DoAnimationFrame(frame): 
            # NOTE: # frame: required: https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
            #print ("DoAnimationFrame(): ENTER")
            vX = self.dctCfg['X-Axis']['GetVals']()
            self.SubPlot.set_xlim(min(self.minX,min(vX)),max(self.maxX,max(vX)))
            #print(f"vX: {vX}, minX: {self.minX}, maxX: {self.maxX}")
            for idx in range(len(self.dctCfg['Y-Vects'])):
                vY = self.dctCfg['Y-Vects'][idx]['GetVals']()
                self.minY = min(self.minY,min(vY)); self.maxY = max(self.maxY,max(vY))
                #print(f"vY: {vY}, minY: {self.minY}, maxY: {self.maxY}")
                self.dctCfg['Y-Vects'][idx]['Plot'].set_data(vX,vY)
            self.SubPlot.set_ylim(self.minY,self.maxY)
        return DoAnimationFrame

    def GetWidg(self):
            return self.PlotCanvas.get_tk_widget()
    def Start(self):
        self.Animation = animation.FuncAnimation(self.fig,self.Update(), interval=1000)
    
if __name__ == "__main__":
    def demo():
        root = Tk()
        root.geometry('1200x700+200+100')
        root.title("Test Window")
        DoZoom(root,False)
        root.config(background='#fafafa')
        oPlotWidg = tPlotWidg(root)
        oPlotWidg.GetWidg().grid(column=1,row=1)
        oPlotWidg.Start()
        root.mainloop()
    demo()