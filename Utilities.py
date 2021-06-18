from datetime import datetime as dt
from time import sleep
def SecondsSince(TS):
	return (dt.now() - TS).total_seconds()
def absdiff(n1,n2):
	return abs(n1-n2)	
def NEAR(n1,n2,e):
	return absdiff(n1,n2) <= e
if __name__ == "__main__":
	def main():
		ts1 = dt.now()
		sleep(1)
		print(f"SecondSince: {SecondsSince(ts1)}")
		print(f"absdiff: {absdiff(3,2)}")
		print(f"NEAR: {NEAR(2.5,3.5,1)}")
	main()