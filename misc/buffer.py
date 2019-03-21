class Buffer:
    def __init__(self, size=5):
        self.data = []
        self.size = size

    def add(self, lmnt):
        if len(self.data) >= self.size:
            self.data = self.data[1:]
            self.data.append(lmnt)
        else:
            self.data.append(lmnt)

    def removeOldest(self):
        self.data = self.data[1:]
    

