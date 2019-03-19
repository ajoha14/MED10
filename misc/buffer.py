import numpy as np

class Buffer:
    def __init__(self, s):
        self.data = np.array([])
        self.size = s
    
    def add(self, lmnt):
        if len(self.data) >= self.size:
            self.data = self.data[1:]
            np.append(self.data, lmnt)
        else:
            np.append(self.data, lmnt)
    
    def removeOldest(self):
        self.data = self.data[1:]
    

