from toffee import Bundle, Signals

class HandShakeBundle(Bundle):
    ready, valid = Signals(2)

class BaseBundle(Bundle):
    clock, reset = Signals(2)

    class IO(Bundle):
        empty, flush = Signals(2)

    io = IO.from_prefix("io_")

class RequestBundle(HandShakeBundle):
    class BitsRequest(Bundle):
        addr, size, cmd, wmask, wdata, user = Signals(6)

    bits = BitsRequest.from_prefix("bits_")

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
