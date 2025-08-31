from toffee import Bundle, Signal, Signals
from testbench.device import SimpleBusCmd

class CacheRtn:
    def __init__(self, valid: bool, rdata: int, cmd: int, user: int):
        self.cmd = cmd
        self.rdata = rdata  # [63:0]
        self.valid = valid
        self.user = user

    def __str__(self):
        return f"CacheRtn: valid: {self.valid}, rdata: 0x{self.rdata:08X}, cmd: {SimpleBusCmd(self.cmd).name}, user: {self.user}"

class HandShakeBundle(Bundle):
    ready, valid = Signals(2)

    async def is_valid(self):
        return self.valid.value == 1

    async def is_ready(self):
        return self.ready.value == 1

    async def wait_valid(self) -> int:
        clock_step = 0
        while not await self.is_valid():
            await self.step(1)
            clock_step += 1
        return clock_step

    async def wait_ready(self) -> int:
        clock_step = 0
        while not await self.is_ready():
            await self.step(1)
            clock_step += 1
        return clock_step

    async def wait_handshake(self) -> int:
        clock_step = 0
        while True:
            if self.ready.value == 1 and self.valid.value == 1:
                return clock_step
            clock_step += 1
            await self.step(1)

    def curr_is_ready(self) -> bool:
        return self.ready.value == 1

    def curr_is_valid(self) -> bool:
        return self.valid.value == 1

    def curr_is_handshake(self) -> bool:
        return self.ready.value == 1 and self.valid.value == 1

class BaseBundle(Bundle):
    clock, reset = Signals(2)

    class IO(Bundle):
        #, flush
        empty = Signal()

    io = IO.from_prefix("io_")

    async def rst(self):
        self.reset.value = 1
        await self.step(2)
        self.reset.value = 0
        await self.step(2)

    async def is_empty(self):
        return self.io.empty.value == 1

class SRAMReqRtn:
    def __init__(self, addr: int, size: int, cmd: int, wmask: int, wdata: int):
        self.addr = addr
        self.size = size
        self.cmd = cmd
        self.wmask = wmask
        self.wdata = wdata

class SRAMReqBundle(HandShakeBundle):
    class BitsSRAMReq(Bundle):
        addr, size, cmd, wmask, wdata = Signals(5)

    bits = BitsSRAMReq.from_prefix("bits_")

    async def recv_req_block(self) -> SRAMReqRtn:
        self.ready.value = 1
        await self.step(1)
        await self.wait_valid()
        addr = self.bits.addr.value
        size = self.bits.size.value
        cmd = SimpleBusCmd(self.bits.cmd.value)
        wmask = self.bits.wmask.value
        wdata = self.bits.wdata.value
        await self.step()
        self.ready.value = 0
        await self.step()
        return SRAMReqRtn(addr, size, cmd, wmask, wdata)

    def recv_req(self) -> SRAMReqRtn:
        addr = self.bits.addr.value
        size = self.bits.size.value
        cmd = SimpleBusCmd(self.bits.cmd.value)
        wmask = self.bits.wmask.value
        wdata = self.bits.wdata.value
        return SRAMReqRtn(addr, size, cmd, wmask, wdata)

class SRAMRespBundle(HandShakeBundle):
    class BitsSRAMResp(Bundle):
        cmd, rdata = Signals(2)

    bits = BitsSRAMResp.from_prefix("bits_")

    async def send_resp_block(self, cmd, rdata):
        await self.wait_ready()
        self.valid.value = 1
        self.bits.cmd.value = cmd
        self.bits.rdata.value = rdata
        await self.step()
        self.valid.value = 0
        await self.step()

    async def send_resp(self, cmd, rdata):
        self.valid.value = 1
        self.bits.cmd.value = cmd
        self.bits.rdata.value = rdata

class RequestBundle(HandShakeBundle):
    class BitsRequest(Bundle):
        addr, size, cmd, wmask, wdata, user = Signals(6)

    bits = BitsRequest.from_prefix("bits_")

    async def request_block(self, addr, size, cmd, wmask, wdata, user):
        await self.wait_ready()
        self.bits.addr.value = addr
        self.bits.size.value = size
        self.bits.cmd.value = cmd
        self.bits.wmask.value = wmask
        self.bits.wdata.value = wdata
        self.bits.user.value = user
        self.valid.value = 1
        await self.step(2)
        self.valid.value = 0
        await self.step(1)

    # async def try_request(self, addr, size, cmd, wmask, wdata, user):
    #     """ 返回所等待的时钟的非阻塞方法，如果不可请求则返回 False """
    #     await self.request_block(addr, size, cmd, wmask, wdata, user)

class ResponseBundle(HandShakeBundle):
    class BitsResponse(Bundle):
        cmd, rdata, user = Signals(3)

    bits = BitsResponse.from_prefix("bits_")

    async def response_block(self) -> CacheRtn:
        self.ready.value = 1
        await self.step(1)
        await self.wait_valid()
        cmd = self.bits.cmd.value
        rdata = self.bits.rdata.value
        user = self.bits.user.value
        self.ready.value = 0
        await self.step(1)
        return CacheRtn(True, rdata, cmd, user)

class MemReqBundle(SRAMReqBundle):
    pass

class MemRespBundle(SRAMRespBundle):
    pass

class CohReqBundle(HandShakeBundle):
    class BitsCohReq(Bundle):
        addr, size, cmd, wmask, wdata = Signals(5)

    bits = BitsCohReq.from_prefix("bits_")

class CohRespBundle(HandShakeBundle):
    class BitsCohResp(Bundle):
        cmd, rdata = Signals(2)

    bits = BitsCohResp.from_prefix("bits_")

class MMIOReqBundle(SRAMReqBundle):
    pass

class MMIORespBundle(SRAMRespBundle):
    pass

class CacheBundle(Bundle):
    base = BaseBundle()
    req = RequestBundle.from_prefix("io_in_req_")
    resp = ResponseBundle.from_prefix("io_in_resp_")
    mem_req = MemReqBundle.from_prefix("io_out_mem_req_")
    mem_resp = MemRespBundle.from_prefix("io_out_mem_resp_")
    coh_req = CohReqBundle.from_prefix("io_out_coh_req_")
    coh_resp = CohRespBundle.from_prefix("io_out_coh_resp_")
    mmio_req = MMIOReqBundle.from_prefix("io_mmio_req_")
    mmio_resp = MMIORespBundle.from_prefix("io_mmio_resp_")

    async def request(self, addr, size, cmd, wmask, wdata, user):
        await self.request_block(addr, size, cmd, wmask, wdata, user)
        return await self.response_block()

    async def reset(self):
        await self.base.rst()

    async def is_empty(self):
        return await self.base.is_empty()

    async def is_flush(self):
        return await self.base.is_flush()

    async def request_block(self, addr, size, cmd, wmask, wdata, user):
        await self.req.request_block(addr, size, cmd, wmask, wdata, user)

    async def response_block(self) -> CacheRtn:
        return await self.resp.response_block()

    def recv_resp(self) -> CacheRtn:
        cmd = self.resp.bits.cmd.value
        rdata = self.resp.bits.rdata.value
        user = self.resp.bits.user.value
        valid = self.resp.valid.value == 1
        return CacheRtn(valid, rdata, cmd, user)

    async def send_mem_resp_block(self, cmd, rdata):
        await self.mem_resp.send_resp_block(cmd, rdata)

    async def recv_mem_req_block(self) -> SRAMReqRtn:
        return await self.mem_req.recv_req_block()

    async def send_mmio_resp_block(self, cmd, rdata):
        await self.mmio_resp.send_resp_block(cmd, rdata)

    async def recv_mmio_req_block(self) -> SRAMReqRtn:
        return await self.mmio_req.recv_req_block()

    def send_mem_resp(self, cmd, rdata):
        self.mem_resp.send_resp(cmd, rdata)

    def recv_mem_req(self) -> SRAMReqRtn:
        return self.mem_req.recv_req()

    def send_mmio_resp(self, cmd, rdata):
        self.mmio_resp.send_resp(cmd, rdata)

    def recv_mmio_req(self) -> SRAMReqRtn:
        return self.mmio_req.recv_req()

    def hook(self, dut, funcs: list):
        self.dut = dut
        for i in funcs:
            self.dut.StepRis(i)

    def get_queue(self):
        if getattr(self, "resp_queue", None) is None:
            self.resp_queue = []
        return self.resp_queue

    def clean_resp_queue(self):
        self.resp_queue.clear()

    async def wait_empty(self):
        raise NotImplementedError
