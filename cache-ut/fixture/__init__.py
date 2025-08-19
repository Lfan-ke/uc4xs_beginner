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
async def bundle(toffee_request: toffee_test.ToffeeRequest, dut: DUTCache) -> CacheBundle:
    bundle = CacheBundle()
    bundle.bind(dut)
    return bundle

from testbench.agent import CacheAgent
from testbench.coverage import all_coverage_func

@toffee_test.fixture
async def agent(toffee_request: toffee_test.ToffeeRequest, bundle: CacheBundle) -> CacheAgent:
    agent = CacheAgent(bundle)
    toffee_request.add_cov_groups(list(map(lambda f: f(agent), all_coverage_func)))
    return agent

from testbench.ref import CacheRef

@toffee_test.fixture
async def ref(toffee_request: toffee_test.ToffeeRequest) -> CacheRef:
    ref = CacheRef()
    return ref

from testbench.env import CacheEnv

@toffee_test.fixture
async def env(toffee_request: toffee_test.ToffeeRequest, agent: CacheAgent, ref: CacheRef) -> CacheEnv:
    env = CacheEnv(agent)
    env.attach(ref)
    return env
