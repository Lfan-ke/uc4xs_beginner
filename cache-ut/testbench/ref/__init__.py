from toffee.model import Model, driver_hook

class CacheRef(Model):
    def __init__(self, size=16):
        super().__init__()
        pass

    # @driver_hook("agent.reset")
    # def reset(self):
    #     self.data = []
    #     self.last = 0
