from threading import Condition, Lock
class ReadWriteLock:
    # What It Does: Lock with non-exclusive read locks, exclusive write-locks
    # How It Works: Condition Variable and Read Lock Counter
    def __init__(self):
        self.condReadable = Condition(Lock())
        self.nReaders = 0
    def AcqRead(self):
        self.condReadable.acquire()
        try:
            self.nReaders +=1
        finally:
            self.condReadable.release()
    def RelRead(self):
        self.condReadable.acquire()
        try:
            self.nReaders -= 1
            if self.nReaders == 0:
                self.condReadable.notifyAll()
        finally:
            self.condReadable.release()
    def AcqWrite(self):
        self.condReadable.acquire()
        while self.nReaders > 0:
            self.condReadable.wait()
    def RelWrite(self):
        self.condReadable.release()