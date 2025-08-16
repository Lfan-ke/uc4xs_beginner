from SyncFIFO import *

def assert_eq(a, b):
    if a == b:
        pass
    else:
        print(f"left: [{a}] is not eq right: [{b}]!")
        assert(a == b)

def test_reset_dut_default():
    dut = DUTSyncFIFO()
    dut.InitClock("clk")
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)
    dut.Finish()

    print("Finished!")

def test_reset_dut_imme():
    dut = DUTSyncFIFO()
    dut.InitClock("clk")

    dut.rst_n.AsImmWrite()

    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)
    dut.Finish()

    print("Finished!")

def test_reset_dut_output():
    dut = DUTSyncFIFO()
    dut.InitClock("clk")
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)

    # print(dut.GetInternalSignalList())

    assert(dut.data_o.value == 0)
    assert(dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.rptr").value == 0)
    assert(dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.rptr").value == 0)

    dut.Finish()

    print("Finished!")

def test_smoke_dut():
    dut = DUTSyncFIFO()
    dut.InitClock("clk")
    dut.rst_n.value = 0
    dut.Step(5)
    dut.rst_n.value = 1
    dut.Step(2)

    assert_eq(dut.empty_o.value, 1)
    assert_eq(dut.full_o.value, 0)

    dut.we_i.value = 1
    dut.data_i.value = 0x114
    dut.Step(2)

    assert_eq(dut.empty_o.value, 0)
    assert_eq(dut.full_o.value, 0)
    assert_eq(dut.GetInternalSignal("SyncFIFO_top.SyncFIFO.counter").value, 1)

    dut.we_i.value = 1
    dut.data_i.value = 0x514  # 114514 是吧？
    dut.Step(2)

    dut.we_i.value = 0
    dut.re_i.value = 1
    dut.Step(2)

    assert_eq(dut.data_o.value, 0x114)

    dut.we_i.value = 0
    dut.re_i.value = 1
    dut.Step(2)

    assert_eq(dut.data_o.value, 0x514)

    dut.Step()

    assert_eq(dut.empty_o.value, 1)

    dut.Finish()
    print("Finished!")

if __name__ == "__main__":
    # test_reset_dut_output()
    test_smoke_dut()
