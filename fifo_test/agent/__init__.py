from toffee import Agent
from toffee.agent import *
from bundle import SyncFIFOBundle

class SyncFIFOAgent(Agent):
    def __init__(self, bundle: SyncFIFOBundle):
        super().__init__(bundle)
        self.bundle = bundle

    @driver_method()
    async def reset(self):
        self.bundle.common.rst_n.value = 0
        await self.monitor_step(5)
        self.bundle.common.rst_n.value = 1
        await self.monitor_step(2)

    @driver_method()
    async def enqueue(self, data):
        await self.bundle.enqueue(data)

    @driver_method()
    async def dequeue(self):
        return await self.bundle.dequeue()

    @driver_method()
    async def read_write(self, data):
        return await self.bundle.read_write(data)

    @driver_method()
    async def is_empty(self):
        return await self.bundle.is_empty()

    @driver_method()
    async def is_full(self):
        return await self.bundle.is_full()

    @monitor_method()
    async def monitor_once(self):
        return self.bundle.as_dict()
