import toffee
import toffee_test
from SyncFIFO import *

@toffee_test.fixture
async def dut(toffee_request: toffee_test.ToffeeRequest):
    my_dut = toffee_request.create_dut(DUTSyncFIFO, "clk")
    toffee.start_clock(my_dut)
    return my_dut

@toffee_test.testcase
async def test_with_ref(dut: DUTSyncFIFO):
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)

    assert dut.empty_o.value == 1
    assert dut.full_o.value == 0

    dut.we_i.value = 1
    dut.data_i.value = 0x114
    dut.Step(2)

    assert dut.empty_o.value == 0
    assert dut.full_o.value == 0
    assert dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.counter").value == 1

    dut.we_i.value = 1
    dut.data_i.value = 0x514
    dut.Step(2)

    dut.we_i.value = 0
    dut.re_i.value = 1
    dut.Step(2)

    assert dut.data_o.value == 0x114

    dut.we_i.value = 0
    dut.re_i.value = 1
    dut.Step(2)

    assert dut.data_o.value == 0x514

    dut.Step()

    assert dut.empty_o.value == 1
