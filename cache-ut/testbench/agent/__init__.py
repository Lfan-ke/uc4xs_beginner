from toffee import Agent
from toffee.agent import *

from testbench.device import SimpleBusCmd

class CacheAgent(Agent):
    def __init__(self, bundle: 'CacheBundle'):
        super().__init__(bundle)
        self.bundle = bundle
        self.resp_queue = getattr(bundle, "resp_queue", [])

    @driver_method()
    async def reset(self):
        await self.bundle.reset()

    @driver_method()
    async def call_read(self, addr, size):
        await self.bundle.request_block(addr, size, SimpleBusCmd.READ, 0, 0, 0)

    @driver_method()
    async def call_read_burst(self, addr, size):
        await self.bundle.request_block(addr, size, SimpleBusCmd.READ_BURST, 0, 0, 0)

    @driver_method()
    async def call_write(self, addr, size, wmask, wdata):
        await self.bundle.request_block(addr, size, SimpleBusCmd.WRITE, wmask, wdata, 0)

    @driver_method()
    async def call_write_burst(self, addr, size, wmask, wdata: list[int]):
        for i in range(7):
            await self.bundle.request_block(addr+(1<<size)*i, size, SimpleBusCmd.WRITE_BURST, wmask, wdata[i], 0)
        await self.bundle.request_block(addr+(1<<size)*7, size, SimpleBusCmd.WRITE_LAST, wmask, wdata[7], 0)

    @driver_method()
    async def recv_resp(self):
        return await self.bundle.response_block()

    async def wait_queue_empty(self):
        await self.bundle.wait_empty()

    @monitor_method()
    async def monitor_once(self):
        return self.bundle.as_dict()
