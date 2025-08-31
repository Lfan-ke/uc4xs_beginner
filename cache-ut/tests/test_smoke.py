import toffee_test

from Cache import *
from fixture import *
from testbench import *

@toffee_test.testcase
async def test_smoke_dut(dut: DUTCache):
    assert dut is not None

@toffee_test.testcase
async def test_smoke_bundle(bundle: CacheBundle):
    assert bundle is not None

@toffee_test.testcase
async def test_smoke_agent(agent: CacheAgent):
    assert agent is not None

@toffee_test.testcase
async def test_smoke_ref(ref: CacheRef):
    assert ref is not None

@toffee_test.testcase
async def test_smoke_env(env: CacheEnv):
    assert env is not None

from toffee_test.reporter import __report_info__

global __report_info__

__report_info__["user"] = {"name": "Leo Cheng", "email": "chengkelfan@qq.com"}
__report_info__["title"] = "NutShell Cache Report"
