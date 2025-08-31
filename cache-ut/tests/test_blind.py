"""
此文件用于确认端口行为，属于盲测并记录……
"""

import toffee_test

from Cache import *
from fixture import *
from testbench import *

# @toffee_test.testcase
# async def test_mmio_rw(agent, debug=False):
#     # debug = True
#     await agent.reset()
#     await agent.call_read(0x3000_0000, 0)
#     resp = await agent.recv_resp()
#     if debug: print(f"mmio [0x3000_0000] resp = {resp.rdata:08x}, {SimpleBusCmd(resp.cmd).name}")
#     await agent.monitor_step(3)
#     await agent.call_write(0x3000_0000, 0, 0xFF, 0x2333)
#     resp = await agent.recv_resp()
#     if debug: print(f"mmio [0x3000_0000] resp = {resp.rdata:08x}, {SimpleBusCmd(resp.cmd).name}")
#     await agent.monitor_step(3)
#     await agent.call_read(0x3000_0000, 0)
#     resp = await agent.recv_resp()
#     if debug: print(f"mmio [0x3000_0000] resp = {resp.rdata:08x}, {SimpleBusCmd(resp.cmd).name}")
#     resp = await agent.recv_resp()
#     if debug: print(f"mmio [0x3000_0000] resp = {resp.rdata:08x}, {SimpleBusCmd(resp.cmd).name}")
#     assert resp.rdata == (0x2333 & 0xFF)

# @toffee_test.testcase
# async def test_blind_bundle_req_mmio_resp(pure_bundle: CacheBundle, debug=False):
#     bundle = pure_bundle
#     await bundle.reset()
#     assert await bundle.is_empty()

#     bundle.req.bits.addr.value = 0x3000_0000
#     bundle.req.bits.size.value = 7
#     bundle.req.bits.cmd.value = SimpleBusCmd.WRITE
#     bundle.req.bits.wmask.value = 0XFF
#     bundle.req.bits.wdata.value = 0x2333
#     bundle.req.valid.value = 1

#     if debug: print(f"clock after req: {await bundle.req.wait_handshake()}")
#     else: await bundle.req.wait_handshake()

#     await bundle.step()
#     bundle.resp.ready.value = 1
#     bundle.req.valid.value = 0
#     bundle.mmio_req.ready.value = 1
#     await bundle.step(3)

#     assert bundle.mmio_req.valid.value == 1  # clock step 2 为 false，3 为 true
#     assert bundle.mmio_req.bits.addr.value == 0x3000_0000
#     assert bundle.mmio_req.bits.size.value == 7
#     assert bundle.mmio_req.bits.cmd.value == SimpleBusCmd.WRITE
#     assert bundle.mmio_req.bits.wmask.value == 0XFF
#     assert bundle.mmio_req.bits.wdata.value == 0x2333

#     if debug: print(f"""
#         cpu_req addr: 0x{bundle.req.bits.addr.value:08x}
#         cpu_req size: {bundle.req.bits.size.value}
#         cpu_req cmd: {SimpleBusCmd(bundle.req.bits.cmd.value).name}
#         cpu_req wmask: 0x{bundle.req.bits.wmask.value:08x}
#         cpu_req wdata: 0x{bundle.req.bits.wdata.value:08x}
#         cpu_req valid: {bundle.req.valid.value}
#         cpu_req ready: {bundle.req.ready.value}

#         cpu_resp rdata: 0x{bundle.resp.bits.rdata.value:08x}
#         cpu_resp cmd: {SimpleBusCmd(bundle.resp.bits.cmd.value).name}
#         cpu_resp valid: {bundle.resp.valid.value}
#         cpu_resp ready: {bundle.resp.ready.value}

#         mem_req addr: 0x{bundle.mem_req.bits.addr.value:08x}
#         mem_req size: {bundle.mem_req.bits.size.value}
#         mem_req cmd: {SimpleBusCmd(bundle.mem_req.bits.cmd.value).name}
#         mem_req wmask: 0x{bundle.mem_req.bits.wmask.value:08x}
#         mem_req wdata: 0x{bundle.mem_req.bits.wdata.value:08x}
#         mem_req valid: {bundle.mem_req.valid.value}
#         mem_req ready: {bundle.mem_req.ready.value}

#         mem_resp rdata: 0x{bundle.mem_resp.bits.rdata.value:08x}
#         mem_resp cmd: {SimpleBusCmd(bundle.mem_resp.bits.cmd.value).name}
#         mem_resp valid: {bundle.mem_resp.valid.value}
#         mem_resp ready: {bundle.mem_resp.ready.value}

#         mmio_req addr: 0x{bundle.mmio_req.bits.addr.value:08x}
#         mmio_req size: {bundle.mmio_req.bits.size.value}
#         mmio_req cmd: {SimpleBusCmd(bundle.mmio_req.bits.cmd.value).name}
#         mmio_req wmask: 0x{bundle.mmio_req.bits.wmask.value:08x}
#         mmio_req wdata: 0x{bundle.mmio_req.bits.wdata.value:08x}
#         mmio_req valid: {bundle.mmio_req.valid.value}
#         mmio_req ready: {bundle.mmio_req.ready.value}

#         mmio_resp rdata: 0x{bundle.mmio_resp.bits.rdata.value:08x}
#         mmio_resp cmd: {SimpleBusCmd(bundle.mmio_resp.bits.cmd.value).name}
#         mmio_resp valid: {bundle.mmio_resp.valid.value}
#         mmio_resp ready: {bundle.mmio_resp.ready.value}
#     """)


# @toffee_test.testcase
# async def test_blind_bundle_req_mem_resp(pure_bundle: CacheBundle, debug=False):
#     bundle = pure_bundle
#     await bundle.reset()
#     assert await bundle.is_empty()

#     bundle.req.bits.addr.value = 0x0000_1000
#     bundle.req.bits.size.value = 0
#     bundle.req.bits.cmd.value = SimpleBusCmd.READ
#     bundle.req.bits.wmask.value = 0XFF
#     bundle.req.bits.wdata.value = 0x2333
#     bundle.req.valid.value = 1

#     if debug: print(f"clock after req: {await bundle.req.wait_handshake()}")

#     await bundle.step()
#     bundle.resp.ready.value = 1
#     bundle.req.valid.value = 0
#     bundle.mem_req.ready.value = 1
#     await bundle.step(3)

#     # 此时获取到的是：READ_BURST 0x00001000 0x000000ff

#     bundle.mem_resp.bits.rdata.value = 0x666
#     bundle.mem_resp.bits.cmd.value = SimpleBusCmd.READ_BURST
#     await bundle.step()

#     bundle.mem_resp.valid.value = 1
#     await bundle.step()
#     await bundle.mem_resp.wait_handshake()
#     bundle.mem_resp.valid.value = 0
#     await bundle.step(2)

#     if debug: print(f"""
#         cpu_req addr: 0x{bundle.req.bits.addr.value:08x}
#         cpu_req size: {bundle.req.bits.size.value}
#         cpu_req cmd: {SimpleBusCmd(bundle.req.bits.cmd.value).name}
#         cpu_req wmask: 0x{bundle.req.bits.wmask.value:08x}
#         cpu_req wdata: 0x{bundle.req.bits.wdata.value:08x}
#         cpu_req valid: {bundle.req.valid.value}
#         cpu_req ready: {bundle.req.ready.value}

#         cpu_resp rdata: 0x{bundle.resp.bits.rdata.value:08x}
#         cpu_resp cmd: {SimpleBusCmd(bundle.resp.bits.cmd.value).name}
#         cpu_resp valid: {bundle.resp.valid.value}
#         cpu_resp ready: {bundle.resp.ready.value}

#         mem_req addr: 0x{bundle.mem_req.bits.addr.value:08x}
#         mem_req size: {bundle.mem_req.bits.size.value}
#         mem_req cmd: {SimpleBusCmd(bundle.mem_req.bits.cmd.value).name}
#         mem_req wmask: 0x{bundle.mem_req.bits.wmask.value:08x}
#         mem_req wdata: 0x{bundle.mem_req.bits.wdata.value:08x}
#         mem_req valid: {bundle.mem_req.valid.value}
#         mem_req ready: {bundle.mem_req.ready.value}

#         mem_resp rdata: 0x{bundle.mem_resp.bits.rdata.value:08x}
#         mem_resp cmd: {SimpleBusCmd(bundle.mem_resp.bits.cmd.value).name}
#         mem_resp valid: {bundle.mem_resp.valid.value}
#         mem_resp ready: {bundle.mem_resp.ready.value}
#     """)

# @toffee_test.testcase
# async def test_blind_agent_rw_device(agent: CacheAgent, debug=False):
#     await agent.reset()
#     debug = True
#     await agent.call_read(0x0000_0000, 0)
#     resp = await agent.recv_resp()
#     await agent.monitor_step(5)
#     if debug: print(f"read resp: cmd={SimpleBusCmd(resp.cmd).name}, rdata=0x{resp.rdata:08x}")
#     if debug: print(f"agent resp queue: {agent.resp_queue}")
#     xx = agent.resp_queue.pop(0)
#     if debug: print(f"agent resp queue: {xx.rdata:08x}, {SimpleBusCmd(xx.cmd).name}")

#     await agent.call_write(0x0000_1000, 1, 0xFF, 0xEE)
#     resp = await agent.recv_resp()

#     await agent.call_read(0x0000_1000, 1)
#     resp = await agent.recv_resp()
#     resp = await agent.recv_resp()

#     for i in range(0, 0x8400, 8):
#         await agent.call_write(0x0000_1000 + i, 3, 0xFF, 0x2333)
#         await agent.call_read(0x0000_0000+i, 0)
#     resp = await agent.recv_resp()
#     await agent.monitor_step()
#     if debug: print(f"write resp: cmd={SimpleBusCmd(resp.cmd).name}, rdata=0x{resp.rdata:08x}")
#     if debug: print(f"agent resp queue: {agent.resp_queue}")
#     if debug: print(f"agent resp queue: {agent.resp_queue[0].rdata:08x}, {SimpleBusCmd(agent.resp_queue[0].cmd).name}")
