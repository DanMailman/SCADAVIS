# TODO: Demo OnLinux
# TODO: Demo DoZoom
# TODO: Demo tSeqCounter.GetSeqList

from datetime import datetime as dt
from time import sleep
from tkinter.constants import NO
from typing import NoReturn
from ReadWriteLock import ReadWriteLock
def SecondsSince(TS):
	return (dt.now() - TS).total_seconds()
def absdiff(n1,n2):
	return abs(n1-n2)	
def NEAR(n1,n2,e):
	return absdiff(n1,n2) <= e
def LimitVal(nVal,nLoLim,nHiLim):
	if nVal < nLoLim: return nLoLim
	if nVal > nHiLim: return nHiLim
	return nVal
class tAverager:
	def __init__(self):
		self.nSum = 0
		self.nCnt = 0
	def start(self,nNum):
		self.nSum = nNum
		self.nCnt = 1
	def add(self,nNum):
		self.nSum += nNum
		self.nCnt += 1
	def clear(self):
		self.nSum = 0
		self.nCnt = 0
	def GetAvg(self):
		return self.nSum / self.nCnt
class tSeqCounter:
	def __init__(self,**kwargs):
		self.Lock = ReadWriteLock()
		if kwargs.get('start_at') != None:
			self.nVal = kwargs['start_at']
			self.start_at = kwargs['start_at']
		else: 
			self.nVal = 0
			self.start_at = 0
	def Increment(self):
		self.Lock.AcqWrite()
		nRet = self.nVal
		self.nVal +=1
		self.Lock.RelWrite()
		return nRet
	def GetSeqNum(self):
		self.Lock.AcqRead()
		nRet = self.nVal
		self.Lock.RelRead()	
		return nRet
	def GetSeqList(self):
		nVal = self.GetSeqNum()
		return [n for n in range(self.start_at,nVal+1)]
	def IncSeqList(self):
		nVal = self.Increment()
		return [n for n in range(self.start_at,nVal+1)]
	def Reset(self):
		self.Lock.AcqWrite()
		self.nVal = 0
		self.Lock.RelWrite() 
def OnLinux():
    from platform import system
    if system().lower().startswith('lin'): return True
def DoZoom(root,bZoom):
    if (bZoom):
        if OnLinux(): root.attributes('-zoomed', True)
        else: root.state('zoomed')
    else:
        if OnLinux(): pass # root.attributes('-zoomed',False)
        else: root.state('normal')
if __name__ == "__main__":
	def demo():
		ts1 = dt.now()
		sleep(1)
		print(f"SecondSince: {SecondsSince(ts1)}")
		print(f"absdiff: {absdiff(3,2)}")
		print(f"NEAR: {NEAR(2.5,3.5,1)}")
		print(f'LimitVal: {LimitVal(3,4,10)}')
		oAverager = tAverager()
		oAverager.add(1)
		oAverager.add(3)
		oAverager.add(5)
		print(f'Averager: {oAverager.GetAvg()}: Expect 3')
		oSeqCtr = tSeqCounter()
		print(f'SeqCtr.Increment: {oSeqCtr.Increment()}')
		print(f'SeqCtr.Increment: {oSeqCtr.Increment()}')
		print(f'SeqCtr.Increment: {oSeqCtr.Increment()}')
		print(f'SeqCtr: {oSeqCtr.GetSeqNum()}: Expect 3')
	demo()