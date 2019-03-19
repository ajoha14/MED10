import numpy as np

class Buffer:
    def __init__(self, _size):
        self.data = np.array([])
        self.size = _size
    
    def add(lmnt):
        if len(self.data) >= self.size:
            self.data = self.data[1:]
            np.append(self.data, lmnt)
        else:
            np.append(self.data, lmnt)
    
    def removeOldest():
        self.data = self.data[1:]
    

