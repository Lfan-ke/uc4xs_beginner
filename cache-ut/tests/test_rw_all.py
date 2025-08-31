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

@toffee_test.testcase
async def test_basic_cache_seq_rw_mmio(agent, debug=False):
    await agent.reset()
    for i in range(MMIO_BASE, MMIO_END):
        await agent.call_write(i, 0, 0xff, (0xe5 & i))
        resp = await agent.recv_resp()
        if debug: print(f"mmio last [{MMIO_END-i}] resp = {resp}")
        await agent.call_read(i, 0)
        resp = await agent.recv_resp()
        while resp.cmd != SimpleBusCmd.READ_LAST:
            resp = await agent.recv_resp()
        if debug: print(f"mmio last [{MMIO_END-i}] resp = {resp}")
        assert resp.rdata == (0xe5 & (0XFF & i))

    await agent.wait_queue_empty()

@toffee_test.testcase
async def test_basic_cache_rw_mem(agent, debug=False):
    await agent.reset()

    TEST_SIZE = 128

    for i in range(TEST_SIZE, TEST_SIZE+TEST_SIZE):
        await agent.call_write(i, 0, 0xff, 0x23)

    await agent.wait_queue_empty()
    await agent.monitor_step(100)

    for i in range(TEST_SIZE, TEST_SIZE+TEST_SIZE):
        await agent.call_read(i, 0)
        resp = await agent.recv_resp()
        assert resp.rdata == 0x23

@toffee_test.testcase
async def test_basic_cache_seq_rw_mem(agent, debug=False):
    # debug = True
    await agent.reset()

    for i in range(MEM_BASE, MEM_END):
        await agent.call_write(i, 0, 0xff, 0x66)
        if debug: print(f"mem last [{(MEM_END-i)//CLEN}]")

    await agent.wait_queue_empty()
    await agent.monitor_step(100)

    for i in range(MEM_BASE, MEM_END):
        await agent.call_read(i, 0)
        resp = await agent.recv_resp()
        if debug: print(f"mem last [{(MEM_END-i)//CLEN}] resp = {resp}")
        assert resp.rdata == 0x66
