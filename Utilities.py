from datetime import datetime as dt
from time import sleep
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
	def __init__(self):
		self.Lock = ReadWriteLock()
		self.nVal = 0
	def Increment(self):
		self.Lock.AcqWrite()
		self.nVal +=1
		nRet = self.nVal
		self.Lock.RelWrite()
		return nRet
	def GetSeqNum(self):
		self.Lock.AcqRead()
		nRet = self.nVal
		self.Lock.RelRead()	
		return nRet
	def Reset(self):
		self.Lock.AcqWrite()
		self.nVal = 0
		self.Lock.RelWrite() 
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