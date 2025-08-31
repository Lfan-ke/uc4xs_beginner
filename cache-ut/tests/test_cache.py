import toffee_test

from Cache import *
from fixture import *
from testbench import *

CACHELINE_SIZE = 8
CLEN = CACHELINE_SIZE
MEM_BASE = 0x0000_0000
MEM_END = 0x0000_8400
MMIO_BASE = 0x3000_0000
MMIO_END = 0x3000_1000

# @toffee_test.testcase
# async def test_basic_cache_seq_rw_mmio(agent, debug=False):
#     await agent.reset()
#     for i in range(MMIO_BASE, MMIO_END):
#         await agent.call_write(i, 0, 0xff, (0xe5 & i))
#         resp = await agent.recv_resp()
#         if debug: print(f"mmio last [{MMIO_END-i}] resp = {resp}")
#         await agent.call_read(i, 0)
#         resp = await agent.recv_resp()
#         while resp.cmd != SimpleBusCmd.READ_LAST:
#             resp = await agent.recv_resp()
#         if debug: print(f"mmio last [{MMIO_END-i}] resp = {resp}")
#         assert resp.rdata == (0xe5 & (0XFF & i))

#     await agent.wait_queue_empty()

# @toffee_test.testcase
# async def test_mmio_no_burst(pure_bundle, agent, debug=False):
#     await pure_bundle.reset()
#     bundle = pure_bundle
#     req, mmio_req, resp, mmio_resp = bundle.req, bundle.mmio_req, bundle.resp, bundle.mmio_resp

#     for addr in range(MMIO_BASE, MMIO_BASE+5):
#         await req.wait_ready()
#         req.bits.addr.value = addr
#         req.bits.cmd.value = SimpleBusCmd.WRITE
#         req.valid.value = 1
#         req.bits.wmask.value = 0xff
#         req.bits.wdata.value = 0x14
#         await req.wait_handshake()
#         await req.step(1)
#         req.valid.value = 0
#         await req.step(1)

#         mmio_req.ready.value = 1
#         await mmio_req.step(1)
#         await mmio_req.wait_valid()
#         cmd = SimpleBusCmd(mmio_req.bits.cmd.value)
#         await mmio_req.step()
#         mmio_req.ready.value = 0
#         await mmio_req.step()

#         assert cmd != SimpleBusCmd.WRITE_BURST
#         assert cmd != SimpleBusCmd.WRITE_LAST

#         await mmio_resp.wait_ready()
#         mmio_resp.bits.rdata.value = 0x14
#         mmio_resp.valid.value = 1
#         await mmio_resp.step(1)
#         mmio_resp.valid.value = 0
#         await resp.step(1)

#         resp.ready.value = 1
#         await resp.wait_valid()
#         cmd = resp.bits.cmd.value
#         rdata = resp.bits.rdata.value
#         assert cmd == SimpleBusCmd.WRITE_RESP
#         resp.ready.value = 0
#         await resp.step(1)

#     for i in range(MMIO_BASE, MMIO_BASE+5):
#         await req.wait_ready()
#         req.bits.addr.value = addr
#         req.bits.cmd.value = SimpleBusCmd.READ
#         req.valid.value = 1
#         await req.wait_handshake()
#         await req.step(1)
#         req.valid.value = 0
#         await req.step(1)

#         mmio_req.ready.value = 1
#         await mmio_req.step(1)
#         await mmio_req.wait_valid()
#         cmd = SimpleBusCmd(mmio_req.bits.cmd.value)
#         await mmio_req.step()
#         mmio_req.ready.value = 0
#         await mmio_req.step()

#         assert cmd != SimpleBusCmd.READ_BURST

#         await mmio_resp.wait_ready()
#         mmio_resp.bits.rdata.value = 0x14
#         mmio_resp.valid.value = 1
#         await mmio_resp.step(1)
#         mmio_resp.valid.value = 0
#         await resp.step(1)

#         resp.ready.value = 1
#         await resp.wait_valid()
#         cmd = resp.bits.cmd.value
#         rdata = resp.bits.rdata.value
#         assert cmd == SimpleBusCmd.READ_LAST
#         assert rdata & 0xFF == 0x14
#         resp.ready.value = 0
#         await resp.step(1)

#     agent.single_cov_points["mmio not burst"].sample()

# @toffee_test.testcase
# async def test_mmio_block_pipeline(agent, debug=False):
#     await agent.reset()
#     await agent.call_write(MMIO_BASE, 2, 0xFFFFFFFF, 0x00114514)
#     agent.bundle.resp.ready.value = 1
#     mmio_block_clock_write = await agent.bundle.resp.wait_valid()

#     await agent.call_read(MMIO_BASE, 2)
#     mmio_block_clock_read = await agent.bundle.resp.wait_valid()
#     assert agent.bundle.resp.bits.rdata.value == 0x00114514

#     await agent.call_write(MMIO_BASE, 2, 0xFFFFFFFF, 0x00114514)
#     agent.bundle.resp.ready.value = 1
#     assert mmio_block_clock_write == await agent.bundle.resp.wait_valid()

#     await agent.call_read(MMIO_BASE, 2)
#     assert mmio_block_clock_read == await agent.bundle.resp.wait_valid()

#     # 获取缓存内的进行比较
#     await agent.call_read(MEM_BASE, 2)
#     await agent.monitor_step(100) # 确保下面的不干扰
#     await agent.call_write(MEM_BASE, 2, 0xFFFFFFFF, 0x00114514)
#     agent.bundle.resp.ready.value = 1
#     mem_block_clock_write = await agent.bundle.resp.wait_valid()
#     await agent.monitor_step(100)
#     await agent.call_read(MEM_BASE, 2)
#     agent.bundle.resp.ready.value = 1
#     mem_block_clock_read = await agent.bundle.resp.wait_valid()

#     assert mem_block_clock_write < mmio_block_clock_write
#     assert mem_block_clock_read < mmio_block_clock_read

#     agent.single_cov_points["mmio block pipeline"].sample()

# @toffee_test.testcase
# async def test_cache_write_back(agent, debug=False):
#     await agent.reset()

#     await agent.call_write(0b0000, 0, 0xff, 0x66)

#     for i in range(300):
#         # 直接写入不会触发MEM写
#         if agent.bundle.mem_req.valid.value:
#             assert agent.bundle.mem_req.bits.cmd.value != SimpleBusCmd.WRITE_BURST
#         await agent.monitor_step(1)

#     point = [False]
#     readed_addr = {0x0000}

#     async def check_write_back():
#         await agent.bundle.dut.ACondition(
#             lambda: agent.bundle.mem_req.valid.value == 1 and
#             agent.bundle.mem_req.bits.wdata.value == 0x66 and
#             agent.bundle.mem_req.bits.cmd.value == SimpleBusCmd.WRITE_BURST
#         )
#         assert agent.bundle.mem_req.bits.addr.value in readed_addr
#         point[0] = True

#     toffee.create_task(check_write_back())

#     for i in range(MEM_BASE, MEM_END, CLEN):
#         await agent.call_write(i, 0, 0xff, 0x66)
#         # 不断写入新的地址，直到触发MEM写
#         readed_addr.add(i)
#         if point[0]:
#             break
#         if debug: print(f"mem last [{(MEM_END-i)//CLEN}]")

#     assert point[0]

#     agent.single_cov_points["cache write back"].sample()

# @toffee_test.testcase
# async def test_cache_miss_and_hit(agent, debug=False):
#     await agent.reset()
#     await agent.monitor_step(200)

#     # miss的时钟周期比hit大，且，miss会触发read_burst
#     await agent.call_read(MEM_BASE+512, 0)
#     mem_block_clock_read_miss = await agent.bundle.resp.wait_valid()

#     await agent.monitor_step(200)

#     await agent.call_write(MEM_BASE+255, 0, 0xff, 0x45)
#     mem_block_clock_write_miss = await agent.bundle.resp.wait_valid()

#     if debug: print(f"mem_block_clock_read_miss: {mem_block_clock_read_miss}, mem_block_clock_write_miss: {mem_block_clock_write_miss}")

#     await agent.call_read(MEM_BASE+512, 0)
#     mem_block_clock_read_hit = await agent.bundle.resp.wait_valid()

#     await agent.monitor_step(200)

#     await agent.call_write(MEM_BASE+255, 0, 0xff, 0x45)
#     mem_block_clock_write_hit = await agent.bundle.resp.wait_valid()

#     if debug: print(f"mem_block_clock_read_hit: {mem_block_clock_read_hit}, mem_block_clock_write_hit: {mem_block_clock_write_hit}")

#     assert mem_block_clock_read_miss > mem_block_clock_read_hit
#     assert mem_block_clock_write_miss > mem_block_clock_write_hit

#     agent.single_cov_points["cache read miss time more than read hit"].sample()

# @toffee_test.testcase
# async def test_cache_keyword_priority(pure_agent):
#     agent = pure_agent
#     await agent.reset()

#     await agent.call_read(MEM_BASE+4, 0)
#     agent.bundle.resp.ready.value = 1
#     req = await agent.bundle.recv_mem_req_block()

#     assert req.addr == MEM_BASE
#     assert req.cmd == SimpleBusCmd.READ_BURST

#     agent.single_cov_points["cache key priority"].sample()

# @toffee_test.testcase
# async def test_cache_dirty_wb(agent, debug=False):
#     await agent.reset()

#     await agent.call_write(0o0000, 0, 0xff, 0x66)

#     for i in range(300):
#         if agent.bundle.mem_req.valid.value:
#             assert agent.bundle.mem_req.bits.cmd.value != SimpleBusCmd.WRITE_BURST
#         await agent.monitor_step(1)

#     point = [False]

#     async def check_write_back():
#         await agent.bundle.dut.ACondition(
#             lambda: agent.bundle.mem_req.valid.value == 1 and
#             agent.bundle.mem_req.bits.wdata.value == 0x66 and
#             agent.bundle.mem_req.bits.cmd.value == SimpleBusCmd.WRITE_BURST
#         )
#         assert agent.bundle.mem_req.bits.addr.value == 0  # 只检测唯一脏块写回
#         point[0] = True

#     toffee.create_task(check_write_back())

#     for i in range(MEM_BASE, MEM_END, CLEN):
#         await agent.call_read(i, 0)
#         # 不写入新的地址，直到触发MEM写
#         if point[0]:
#             break
#         if debug: print(f"mem last [{(MEM_END-i)//CLEN}]")

#     assert point[0]

#     agent.single_cov_points["cache dirty block write back"].sample()

# @toffee_test.testcase
# async def test_cache_clean_non_wb(agent, debug=False):
#     await agent.reset()

#     point = [1]

#     async def check_write_back():
#         await agent.bundle.dut.ACondition(
#             lambda: agent.bundle.mem_req.valid.value == 1 and
#             (agent.bundle.mem_req.bits.cmd.value == SimpleBusCmd.WRITE_BURST or
#              agent.bundle.mem_req.bits.cmd.value == SimpleBusCmd.WRITE or
#              agent.bundle.mem_req.bits.cmd.value == SimpleBusCmd.WRITE_LAST)
#         )
#         point[0] = False   # 如果检测到写回就报错

#     toffee.create_task(check_write_back())

#     for i in range(MEM_BASE, MEM_END, CLEN):
#         await agent.call_read(i, 0)
#         assert point[0]
#         if debug: print(f"mem last [{(MEM_END-i)//CLEN}]")

#     await agent.monitor_step(500)
#     assert point[0]

#     agent.single_cov_points["clean blocks not write back"].sample()
