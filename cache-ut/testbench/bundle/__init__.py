from toffee import Bundle, Signals

class HandShakeBundle(Bundle):
    ready, valid = Signals(2)

    async def is_valid(self):
        return self.valid.value == 1

    async def is_ready(self):
        return self.ready.value == 1

    async def wait_valid(self):
        clock_step = 0
        while not await self.is_valid():
            await self.step(1)
            clock_step += 1
        return clock_step

    async def wait_ready(self):
        clock_step = 0
        while not await self.is_ready():
            await self.step(1)
            clock_step += 1
        return clock_step

class BaseBundle(Bundle):
    clock, reset = Signals(2)

    class IO(Bundle):
        empty, flush = Signals(2)

    io = IO.from_prefix("io_")

    async def reset(self):
        self.reset.value = 1
        await self.step(2)
        self.reset.value = 0
        await self.step(2)

    async def is_empty(self):
        return self.io.empty.value == 1

    async def is_flush(self):
        return self.io.flush.value == 1

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
        await self.step(1)
        await self.wait_ready()
        self.valid.value = 0
        await self.step(1)

    # async def try_request(self, addr, size, cmd, wmask, wdata, user):
    #     """ 返回所等待的时钟的非阻塞方法，如果不可请求则返回 False """
    #     await self.request_block(addr, size, cmd, wmask, wdata, user)

class ResponseBundle(HandShakeBundle):
    class BitsResponse(Bundle):
        cmd, rdata, user = Signals(3)

    bits = BitsResponse.from_prefix("bits_")

class MemReqBundle(HandShakeBundle):
    class BitsMemReq(Bundle):
        addr, size, cmd, wmask, wdata = Signals(5)

    bits = BitsMemReq.from_prefix("bits_")

class MemRespBundle(HandShakeBundle):
    class BitsMemResp(Bundle):
        cmd, rdata = Signals(2)

    bits = BitsMemResp.from_prefix("bits_")

class CohReqBundle(HandShakeBundle):
    class BitsCohReq(Bundle):
        addr, size, cmd, wmask, wdata = Signals(5)

    bits = BitsCohReq.from_prefix("bits_")

class CohRespBundle(HandShakeBundle):
    class BitsCohResp(Bundle):
        cmd, rdata = Signals(2)

    bits = BitsCohResp.from_prefix("bits_")

class MMIOReqBundle(HandShakeBundle):
    class BitsMMIOReq(Bundle):
        addr, size, cmd, wmask, wdata = Signals(5)

    bits = BitsMMIOReq.from_prefix("bits_")

class MMIORespBundle(HandShakeBundle):
    class BitsMMIOResp(Bundle):
        cmd, rdata = Signals(2)

    bits = BitsMMIOResp.from_prefix("bits_")

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
