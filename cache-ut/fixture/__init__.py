import toffee
import toffee_test

from Cache import *

@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest) -> DUTCache:
    dut = toffee_request.create_dut(DUTCache, "clock")
    toffee.start_clock(dut)
    return dut

from testbench.bundle import CacheBundle

@toffee_test.fixture
async def pure_bundle(dut: DUTCache, debug=False) -> CacheBundle:
    # debug = True
    bundle = CacheBundle()
    bundle.bind(dut)
    bundle.hook(dut, [])
    return bundle

@toffee_test.fixture
async def bundle(dut: DUTCache, mmio: 'MMIODevice', mem: 'MemDevice', debug=False) -> CacheBundle:
    bundle = CacheBundle()
    bundle.bind(dut)

    # debug = True
    max_cycles = 100000

    state_dict = {
        "mem": {
            "queue": [],
            "burst": 0,
        },
        "mmio": {
            "queue": [],
        },
    }

    from testbench.device import DeviceRtn, SimpleBusCmd

    async def wait_empty(self):
        while state_dict["mem"]["queue"] or state_dict["mmio"]["queue"] or state_dict["mem"]["burst"]:
            await self.step(1)
        return

    setattr(bundle, "wait_empty", wait_empty.__get__(bundle))

    def mmio_func(cycle):
        curr_len = len(state_dict["mmio"]["queue"])
        if bundle.mmio_req.curr_is_valid():
            if bundle.mmio_req.curr_is_ready():
                bundle.mmio_req.ready.value = 0
            else:
                bundle.mmio_req.ready.value = 1
                req = bundle.recv_mmio_req()
                if debug: print(f"mmio req: 0x{req.addr:08X}, {req.size}, {SimpleBusCmd(req.cmd).name}, 0x{req.wmask:08X}, 0x{req.wdata:08X}")
                res = mmio.apply(
                    req.addr, req.size, SimpleBusCmd(req.cmd), req.wmask, req.wdata
                )
                state_dict["mmio"]["queue"].append(res)
        if bundle.mmio_resp.curr_is_ready():
            if bundle.mmio_resp.curr_is_valid():
                bundle.mmio_resp.valid.value = 0
            else:
                if curr_len == 0: return
                if state_dict["mmio"]["queue"]:
                    resp = state_dict["mmio"]["queue"].pop(0)
                    bundle.mmio_resp.valid.value = resp.valid
                    bundle.mmio_resp.bits.rdata.value = resp.rdata
                    bundle.mmio_resp.bits.cmd.value = resp.cmd
                    if debug: print(f"mmio resp: 0x{resp.rdata:08X}, {SimpleBusCmd(resp.cmd).name}, {resp.valid}")

    def mem_func(cycle):
        curr_len = len(state_dict["mem"]["queue"])
        if bundle.mem_req.curr_is_valid():
            if bundle.mem_req.curr_is_ready():
                bundle.mem_req.ready.value = 0
            else:
                bundle.mem_req.ready.value = 1
                req = bundle.recv_mem_req()
                if debug: print(f"mem req: 0x{req.addr:08X}, {req.size}, {SimpleBusCmd(req.cmd).name}, 0x{req.wmask:08X}, 0x{req.wdata:08X}")
                res = mem.apply(
                    req.addr, req.size, SimpleBusCmd(req.cmd), req.wmask, req.wdata
                )
                if debug:# or 1:
                    if req.cmd == SimpleBusCmd.WRITE_LAST:
                        print(f"  ---  mem write last: addr: {req.addr:08X}, wdata: {req.wdata:08X}, wmask: {req.wmask:08X}")
                    if req.cmd == SimpleBusCmd.WRITE_BURST:
                        print(f"  ---  mem write burst: addr: {req.addr:08X}, wdata: {req.wdata:08X}, wmask: {req.wmask:08X}")
                    if req.cmd == SimpleBusCmd.WRITE:
                        print(f"  ---  mem write: addr: {req.addr:08X}, wdata: {req.wdata:08X}, wmask: {req.wmask:08X}")
                    if req.cmd == SimpleBusCmd.READ:
                        print(f"  ---  mem read: addr: {req.addr:08X}")
                    if req.cmd == SimpleBusCmd.READ_BURST:
                        print(f"  ---  mem read burst: addr: {req.addr:08X}")
                if res.valid:
                    state_dict["mem"]["queue"].append(res)
                else:
                    assert req.cmd in (SimpleBusCmd.READ_BURST, SimpleBusCmd.WRITE_BURST, SimpleBusCmd.WRITE_LAST)
                    if req.cmd == SimpleBusCmd.READ_BURST:
                        for i in range(8):
                            raddr = req.addr + i * (1 << req.size)
                            rres = mem.apply(raddr, req.size, SimpleBusCmd.READ, 0, 0)
                            assert rres.valid
                            rres.cmd = SimpleBusCmd.READ_LAST # READ_BURST if i < 7 else SimpleBusCmd.READ_LAST
                            state_dict["mem"]["queue"].append(rres)
                    else:
                        # wb 等待写完即可
                        if req.cmd == SimpleBusCmd.WRITE_BURST:
                            req.cmd = SimpleBusCmd.WRITE
                            res = mem.apply(req.addr + state_dict["mem"]["burst"] * (1 << req.size), req.size, req.cmd, req.wmask, req.wdata)
                            state_dict["mem"]["burst"] += 1
                            assert res.valid
                        else:
                            assert req.cmd == SimpleBusCmd.WRITE_LAST
                            req.cmd = SimpleBusCmd.WRITE
                            res = mem.apply(req.addr + state_dict["mem"]["burst"] * (1 << req.size), req.size, req.cmd, req.wmask, req.wdata)
                            state_dict["mem"]["burst"] = 0
                            if res.valid: state_dict["mem"]["queue"].append(res)
        if bundle.mem_resp.curr_is_ready():
            if bundle.mem_resp.curr_is_valid():
                bundle.mem_resp.valid.value = 0
            else:
                if curr_len == 0: return   # 新加入的至少等待一个时钟周期
                if state_dict["mem"]["queue"]:
                    resp = state_dict["mem"]["queue"].pop(0)
                    bundle.mem_resp.valid.value = resp.valid
                    bundle.mem_resp.bits.rdata.value = resp.rdata
                    bundle.mem_resp.bits.cmd.value = resp.cmd
                    if debug: print(f"mem resp: 0x{resp.rdata:08X}, {SimpleBusCmd(resp.cmd).name}, {resp.valid}")

    resp_queue = bundle.get_queue()

    def collect_return(cycle):
        # debug = True
        if debug: print(f"--------------------{cycle}----------------------")
        if debug and cycle > max_cycles:
            import sys
            sys.exit(0)
        if bundle.resp.curr_is_ready():
            bundle.resp.ready.value = 0
        else:
            bundle.resp.ready.value = 1
            if bundle.resp.curr_is_valid():
                resp = bundle.recv_resp()
                if resp.valid: resp_queue.append(resp)
                if debug: print(f"  - cache resp: 0x{resp.rdata:08X}, {SimpleBusCmd(resp.cmd).name}, {resp.valid}")

    def log_pin_state(cycle):
        # debug = True
        if not debug: return
        # cache
        if bundle.req.curr_is_ready():
            print(f"req ready: addr: [{bundle.req.bits.addr.value:08X}] size: [{bundle.req.bits.size.value:08X}] cmd: [{SimpleBusCmd(bundle.req.bits.cmd.value).name}] wmask: [{bundle.req.bits.wmask.value:08X}] wdata: [{bundle.req.bits.wdata.value:08X}] user: [{bundle.req.bits.user.value:08X}] valid: [{bool(bundle.req.valid.value)}]")
        if bundle.req.curr_is_valid():
            if bundle.req.curr_is_ready():
                print(f"req handshake")
            else:
                print("req valid curr")
        if bundle.resp.curr_is_valid():
            print(f"resp valid: rdata: [{bundle.resp.bits.rdata.value:08X}] cmd: [{SimpleBusCmd(bundle.resp.bits.cmd.value).name}]")
        if bundle.resp.curr_is_ready():
            if bundle.resp.curr_is_valid():
                print(f"resp handshake")
            else:
                print("resp ready curr")
        # mem
        if bundle.mem_req.curr_is_ready():
            print(f"mem req ready: addr: [{bundle.mem_req.bits.addr.value:08X}] size: [{bundle.mem_req.bits.size.value:08X}] cmd: [{SimpleBusCmd(bundle.mem_req.bits.cmd.value).name}] wmask: [{bundle.mem_req.bits.wmask.value:08X}] wdata: [{bundle.mem_req.bits.wdata.value:08X}]")
        if bundle.mem_req.curr_is_valid():
            if bundle.mem_req.curr_is_ready():
                print(f"mem req handshake")
            else:
                print("mem req valid curr")
        if bundle.mem_resp.curr_is_valid():
            print(f"mem resp valid: rdata: [{bundle.mem_resp.bits.rdata.value:08X}] cmd: [{SimpleBusCmd(bundle.mem_resp.bits.cmd.value).name}]")
        if bundle.mem_resp.curr_is_ready():
            if bundle.mem_resp.curr_is_valid():
                print(f"mem resp handshake")
            else:
                print("mem resp ready curr")
        # mmio
        if bundle.mmio_req.curr_is_ready():
            print(f"mmio req ready: addr: [{bundle.mmio_req.bits.addr.value:08X}] size: [{bundle.mmio_req.bits.size.value:08X}] cmd: [{SimpleBusCmd(bundle.mmio_req.bits.cmd.value).name}] wmask: [{bundle.mmio_req.bits.wmask.value:08X}] wdata: [{bundle.mmio_req.bits.wdata.value:08X}]")
        if bundle.mmio_req.curr_is_valid():
            if bundle.mmio_req.curr_is_ready():
                print(f"mmio req handshake")
            else:
                print("mmio req valid curr")
        if bundle.mmio_resp.curr_is_valid():
            print(f"mmio resp valid: rdata: [{bundle.mmio_resp.bits.rdata.value:08X}] cmd: [{SimpleBusCmd(bundle.mmio_resp.bits.cmd.value).name}]")
        if bundle.mmio_resp.curr_is_ready():
            if bundle.mmio_resp.curr_is_valid():
                print(f"mmio resp handshake")
            else:
                print("mmio resp ready curr")

    bundle.hook(dut, [log_pin_state, mmio_func, mem_func, collect_return])
    return bundle

from testbench.agent import CacheAgent
from testbench.coverage import all_coverage_func, single_coverage_func

@toffee_test.fixture
async def agent(toffee_request: toffee_test.ToffeeRequest, bundle: CacheBundle) -> CacheAgent:
    agent = CacheAgent(bundle)
    toffee_request.add_cov_groups(list(map(lambda f: f(agent), all_coverage_func)))
    single_cov_points = {
        k: f(agent) for k, f in single_coverage_func.items()
    }
    setattr(agent, "single_cov_points", single_cov_points)
    yield agent
    toffee_request.cov_groups.extend(single_cov_points.values())

@toffee_test.fixture
async def pure_agent(toffee_request: toffee_test.ToffeeRequest, pure_bundle: CacheBundle) -> CacheAgent:
    agent = CacheAgent(pure_bundle)
    toffee_request.add_cov_groups(list(map(lambda f: f(agent), all_coverage_func)))
    single_cov_points = {
        k: f(agent) for k, f in single_coverage_func.items()
    }
    setattr(agent, "single_cov_points", single_cov_points)
    yield agent
    toffee_request.cov_groups.extend(single_cov_points.values())

from testbench.ref import CacheRef

@toffee_test.fixture
async def ref() -> CacheRef:
    ref = CacheRef()
    return ref

from testbench.env import CacheEnv

@toffee_test.fixture
async def env(agent: CacheAgent, ref: CacheRef) -> CacheEnv:
    env = CacheEnv(agent)
    env.attach(ref)
    return env

from testbench.device import MMIODevice, MemDevice

@toffee_test.fixture
async def mmio() -> MMIODevice:
    mmio = MMIODevice()
    return mmio

@toffee_test.fixture
async def mem() -> MemDevice:
    mem = MemDevice()
    return mem
