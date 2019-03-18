import numpy as np
import heartpy as hp
from time import sleep


class hrProcesser:
    def __init__(self, baud):
        self.ptf = 'C:/Users/Anders S. Johansen/Desktop/data.txt'
        self.buffer = np.array([])
        self.baud = baud
        self.sampleLength = 2
        
    def hrBuffer(self, hr):
        hr = hr/20
        if len(self.buffer) >= self.baud * self.sampleLength:
            self.buffer = self.buffer[1:]
            self.buffer = np.append(self.buffer, hr)
        else:
            self.buffer = np.append(self.buffer, hr)

    def measure(self):
        if len(self.buffer) >= self.baud * self.sampleLength:
            wd,measurements = hp.process(np.array(self.buffer),self.baud)

    def test(self):
        with open(self.ptf) as f:
            raw = f.read().splitlines()
            raw = np.array(raw, dtype=float)
            raw = hp.get_data(self.ptf)
            print(raw)
            for i in raw:
                self.hrBuffer(i)
                self.measure()

cl = hrProcesser(1000)
cl.test()
    
