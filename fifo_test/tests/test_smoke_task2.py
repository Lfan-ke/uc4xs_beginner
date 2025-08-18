import toffee
import toffee_test

from bundle import *
from SyncFIFO import *

from toffee_test.reporter import __report_info__

global __report_info__

__report_info__["user"] = {"name": "Leo Cheng", "email": "chengkelfanke@gmail.com"}
__report_info__["title"] = "SyncFIFO Report"

@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest):
    my_dut = toffee_request.create_dut(DUTSyncFIFO, "clk")
    toffee.start_clock(my_dut)
    return my_dut

def reset_dut(dut: DUTSyncFIFO):
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)

    assert dut.empty_o.value == 1
    assert dut.full_o.value == 0

@toffee_test.testcase
async def test_bundle(dut: DUTSyncFIFO):
    reset_dut(dut)
    dut_bundle = SyncFIFOBundle()
    dut_bundle.bind(dut)

    await dut_bundle.enqueue(0x114)
    await dut_bundle.step(1)
    assert dut_bundle.common.empty_o.value == 0
    assert dut_bundle.common.full_o.value == 0
    assert dut_bundle.internal.counter.value == 1

    await dut_bundle.enqueue(0x514)
    await dut_bundle.step(1)
    assert dut_bundle.internal.counter.value == 2

    data = await dut_bundle.dequeue()
    assert data == 0x114
    data = await dut_bundle.dequeue()
    assert data == 0x514

    await dut_bundle.step(1)
    assert dut_bundle.common.empty_o.value == 1
    assert dut_bundle.common.full_o.value == 0
    assert dut_bundle.internal.counter.value == 0


@toffee_test.testcase
async def test_full_empty(dut: DUTSyncFIFO):
    reset_dut(dut)
    dut_bundle = SyncFIFOBundle()
    dut_bundle.bind(dut)

    queue_size = 16
    for i in range(queue_size):
        await dut_bundle.enqueue(i)
        assert dut_bundle.internal.counter.value == i + 1
        assert dut_bundle.common.empty_o.value == 0
        if i < queue_size - 1:
            assert dut_bundle.common.full_o.value == 0
        else:
            assert dut_bundle.common.full_o.value == 1

    for i in range(queue_size):
        data = await dut_bundle.dequeue()
        assert data == i
        assert dut_bundle.internal.counter.value == queue_size - i - 1
        if i < queue_size - 1:
            assert dut_bundle.common.empty_o.value == 0
        else:
            assert dut_bundle.common.empty_o.value == 1

    assert dut_bundle.common.empty_o.value == 1
    assert dut_bundle.common.full_o.value == 0
    assert dut_bundle.internal.counter.value == 0

@toffee_test.testcase
async def test_agent(dut: DUTSyncFIFO):
    from agent import SyncFIFOAgent

    dut_bundle = SyncFIFOBundle()
    dut_bundle.bind(dut)
    agent = SyncFIFOAgent(dut_bundle)

    await agent.reset()

    await agent.enqueue(0x114)
    await agent.enqueue(0x514)

    data = await agent.dequeue()
    assert data == 0x114
    data = await agent.dequeue()
    assert data == 0x514

""" --- | --- """
from agent import SyncFIFOAgent


@toffee_test.fixture
async def agent(toffee_request: toffee_test.ToffeeRequest):
    fifo_dut: DUTSyncFIFO = toffee_request.create_dut(DUTSyncFIFO, "clk")
    toffee.start_clock(fifo_dut)

    from coverage.fifo_coverage import (
        get_cover_base_operations,
        get_cover_boundary_operations,
        get_cover_point_behavior,
        get_cover_data_integrity,
        get_cover_reset_behavior,
    )

    dut_bundle = SyncFIFOBundle()
    dut_bundle.bind(fifo_dut)
    fifo_agent = SyncFIFOAgent(dut_bundle)

    toffee_request.add_cov_groups([
        get_cover_base_operations(fifo_agent),
        get_cover_boundary_operations(fifo_agent),
        get_cover_point_behavior(fifo_agent),
        get_cover_data_integrity(fifo_agent),
        get_cover_reset_behavior(fifo_agent),
    ])

    yield fifo_agent

@toffee_test.testcase
async def test_agent_with_coverage(agent: SyncFIFOAgent):

    await agent.reset()

    await agent.enqueue(0x114)
    await agent.enqueue(0x514)

    data = await agent.dequeue()
    assert data == 0x114
    data = await agent.dequeue()
    assert data == 0x514

    for i in range(17):
        await agent.enqueue(i)
    else:
        assert await agent.is_full()

    last = -1

    for i in range(17):
        if i < 16:
            assert await agent.dequeue() == i
            last = i
        else:
            assert await agent.is_empty()
            assert agent.bundle.internal.counter.value == 0
            assert await agent.dequeue() == last
            assert await agent.is_empty()
            assert agent.bundle.internal.counter.value == 0

    await agent.reset()
    assert await agent.is_empty()

    assert await agent.read_write(0x233) == 0
    assert await agent.read_write(0x666) == 0x233
    assert await agent.read_write(0xaaa) == 0x666

""" --- | --- """
from ref import SyncFIFORef
from env import SyncFIFOEnv

@toffee_test.fixture
async def env(toffee_request: toffee_test.ToffeeRequest):
    fifo_dut: DUTSyncFIFO = toffee_request.create_dut(DUTSyncFIFO, "clk")
    toffee.start_clock(fifo_dut)

    from coverage.fifo_coverage import (
        get_cover_base_operations,
        get_cover_boundary_operations,
        get_cover_point_behavior,
        get_cover_data_integrity,
        get_cover_reset_behavior,
    )

    dut_bundle = SyncFIFOBundle()
    dut_bundle.bind(fifo_dut)
    fifo_agent = SyncFIFOAgent(dut_bundle)

    toffee_request.add_cov_groups([
        get_cover_base_operations(fifo_agent),
        get_cover_boundary_operations(fifo_agent),
        get_cover_point_behavior(fifo_agent),
        get_cover_data_integrity(fifo_agent),
        get_cover_reset_behavior(fifo_agent),
    ])

    fifo_env = SyncFIFOEnv(fifo_agent)
    fifo_env.attach(SyncFIFORef())

    yield fifo_env


@toffee_test.testcase
async def test_env_with_ref(env: SyncFIFOEnv):

    await env.agent.reset()

    await env.agent.enqueue(0x114)
    await env.agent.enqueue(0x514)

    data = await env.agent.dequeue()
    data = await env.agent.dequeue()

    for i in range(17):
        await env.agent.enqueue(i)

    last = -1

    for i in range(17):
        if i < 16:
            await env.agent.dequeue()
            last = i
        else:
            await env.agent.dequeue()

    await env.agent.reset()

    await env.agent.read_write(0x233)
    await env.agent.read_write(0x666)
    await env.agent.read_write(0xaaa)
