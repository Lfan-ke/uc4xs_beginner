from toffee import Agent
from toffee.agent import *

class CacheAgent(Agent):
    def __init__(self, bundle: 'CacheBundle'):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def pss(self): pass

    @monitor_method()
    async def monitor_once(self):
        return self.bundle.as_dict()
