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
async def test_basic_cache_rw_mem(agent, debug=False):
    await agent.reset()

    TEST_SIZE = 128

    for i in range(TEST_SIZE):
        await agent.call_write(i, 0, 0xff, 0x23)

    await agent.wait_queue_empty()
    await agent.monitor_step(100)

    for i in range(TEST_SIZE):
        await agent.call_read(i, 0)
        resp = await agent.recv_resp()
        assert resp.rdata == 0x23

@toffee_test.testcase
async def test_basic_cache_seq_rw_mem(agent, debug=False):
    debug = True
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

@toffee_test.testcase
async def test_basic_cache_rdm_rw_all(agent):
    from random import randrange, choice

    def gen_rand_testcase(num = 10):
        tc = []
        for i in range(num):
            tc.append({
                "addr": randrange(MEM_BASE, MEM_END),
                "data": randrange(0, 0xFFFF_FFFFF),
                "mask": choice([0xFF, 0XFFFF, 0xFFFFFFFF]),
                "size": randrange(0, 8),
            })
        return tc

    testcase = gen_rand_testcase()

    for i in range(len(testcase)):
        await agent.call_write(testcase[i]["addr"], testcase[i]["size"], testcase[i]["mask"], testcase[i]["data"])

    await agent.wait_queue_empty()
    await agent.monitor_step(100)

    for i in range(len(testcase)):
        resp = await agent.recv_resp()
        await agent.call_read(testcase[i]["addr"], testcase[i]["size"])
        byte_size = 2 ** testcase[i]["size"]
        bit_mask = (1 << (byte_size * 8)) - 1
        expected = testcase[i]["data"] & bit_mask & testcase[i]["mask"]

        assert resp.rdata == expected
