from toffee.model import Model, driver_hook

class SyncFIFORef(Model):
    def __init__(self, size=16):
        super().__init__()
        self.size = size
        self.data = []
        self.last = 0

    @driver_hook("agent.enqueue")
    def enqueue(self, data):
        if len(self.data) < self.size:
            self.data.append(data)

    @driver_hook("agent.dequeue")
    def dequeue(self):
        if len(self.data) > 0:
            self.last = self.data.pop(0)
        return self.last

    @driver_hook("agent.read_write")
    def read_write(self, data):
        temp = self.dequeue()
        self.enqueue(data)
        return temp

    @driver_hook("agent.reset")
    def reset(self):
        self.data = []
        self.last = 0
