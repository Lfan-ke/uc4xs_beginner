from Cache import *

def test_reset_dut_default():
    dut = DUTCache()

    dut.Step(1)

    dut.Finish()

    print("Finished!")
