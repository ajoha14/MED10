import numpy as np
class Buffer:
    def __init__(self, sz=5):
        self.data = np.array([])
        self.size = sz

    def add(self, lmnt):
        if len(self.data) >= self.size:
            self.data = self.data[1:]
            self.data = np.append(self.data, lmnt)
        else:
            self.data = np.append(self.data, lmnt)

    def removeOldest(self):
        self.data = self.data[1:]
    

