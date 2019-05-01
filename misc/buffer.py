class Buffer:
    def __init__(self, size=5):
        self.data = []
        self.size = size

    def add(self, newData):
        if self.isFull():
            self.data.pop(0)# = self.data[1:]
            self.data.append(newData)
        else:
            self.data.append(newData)

    def removeOldest(self):
        self.data = self.data[1:]

    def isFull(self):
        if len(self.data) >= self.size:
            return True
        else:
            return False

    def flush(self):
        self.data = []

