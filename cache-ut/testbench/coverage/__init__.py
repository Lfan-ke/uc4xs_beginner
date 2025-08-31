__all__ = [
    "all_coverage_func", "single_coverage_func",
]

from toffee.funcov import CovGroup, CovIsInRange

# Cache的基本读写
from testbench.device import SimpleBusCmd

def get_cov_group_basic_cache_rw(agent: "CacheAgent"):
    group = CovGroup("Basic Cache Read/Write")
    group.add_watch_point(agent.bundle.req, {
        "READ": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ,
        "WRITE": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE,
        "READ_BURST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ_BURST,
        "WRITE_BURST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_BURST,
        "WRITE_LAST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_LAST,
    }, name="cache req")
    group.add_watch_point(agent.bundle.resp, {
        "READ_LAST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ_LAST,
        "WRITE_RESP": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_RESP,
    }, name="cache resp")
    return group

def get_cov_group_basic_mem_rw(agent: "CacheAgent"):
    group = CovGroup("Basic Mem Read/Write")
    group.add_watch_point(agent.bundle.mem_req, {
        "READ": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ,
        "WRITE": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE,
        "READ_BURST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ_BURST,
        "WRITE_BURST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_BURST,
        "WRITE_LAST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_LAST,
    }, name="mem req")
    group.add_watch_point(agent.bundle.mem_resp, {
        "READ_LAST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ_LAST,
        "WRITE_RESP": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_RESP,
    }, name="mem resp")
    return group

def get_cov_group_basic_mmio_rw(agent: "CacheAgent"):
    group = CovGroup("Basic MMIO Read/Write")
    group.add_watch_point(agent.bundle.mmio_req, {
        "READ": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ,
        "WRITE": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE,
        "NO BURST": lambda bundle: bundle.bits.cmd.value != SimpleBusCmd.READ_BURST and bundle.bits.cmd.value != SimpleBusCmd.WRITE_BURST and bundle.bits.cmd.value != SimpleBusCmd.WRITE_LAST,
    }, name="mmio req")
    group.add_watch_point(agent.bundle.mmio_resp, {
        "READ_LAST": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.READ_LAST,
        "WRITE_RESP": lambda bundle: bundle.bits.cmd.value == SimpleBusCmd.WRITE_RESP,
    }, name="mmio resp")
    return group

# 请求被正确转发
def get_cov_group_req_forward(agent: "CacheAgent"):
    group = CovGroup("Request Forwarding")
    group.add_watch_point(agent.bundle.req, {
        "to mem": lambda bundle: bundle.bits.addr.value < 0x3000_0000,
        "to mmio": lambda bundle: bundle.bits.addr.value >= 0x3000_0000,
    }, name="cache req forward")
    group.add_watch_point(agent.bundle, {
        "mem recv": lambda bundle: bundle.mem_req.bits.addr.value < 0x3000_0000 and bundle.mem_req.curr_is_valid() and bundle.mem_req.curr_is_ready(),
        "mmio recv": lambda bundle: bundle.mmio_req.bits.addr.value >= 0x3000_0000 and bundle.mmio_req.curr_is_valid() and bundle.mmio_req.curr_is_ready(),
    }, name="cache recv forward")
    return group

def get_cov_group_mem_mmio_rw_block_range(agent: "CacheAgent"):
    group = CovGroup("Mem/MMIO RW Block CL Range")

    CACHELINE_SIZE = 8
    MEM_BASE = 0x0000_0000
    MEM_END = 0x0000_8400
    MMIO_BASE = 0x3000_0000
    MMIO_END = 0x3000_1000

    mem_bins_dict = {}
    mmio_bins_dict = {}

    for i in range((MEM_END - MEM_BASE) // (CACHELINE_SIZE ** 2)):   # CL_LEN * XLEN -》 64
        start = MEM_BASE + i * (CACHELINE_SIZE ** 2)
        end = start + CACHELINE_SIZE - 1
        mem_bins_dict[f"mem_cl_{i:03d}: [0x{start:08x}, 0x{end:08x}]"] = CovIsInRange(start, end)

    for i in range((MMIO_END - MMIO_BASE) // CACHELINE_SIZE):
        start = MMIO_BASE + i * CACHELINE_SIZE
        end = start + CACHELINE_SIZE - 1
        mmio_bins_dict[f"mmio_cl_{i:03d}: [0x{start:08x}, 0x{end:08x}]"] = CovIsInRange(start, end)

    group.add_watch_point(agent.bundle.mem_req.bits.addr, mem_bins_dict, name="mem cacheline access")
    group.add_watch_point(agent.bundle.mmio_req.bits.addr, mmio_bins_dict, name="mmio cacheline access")

    return group

all_coverage_func = [
    get_cov_group_basic_cache_rw,
    get_cov_group_basic_mem_rw,
    get_cov_group_basic_mmio_rw,
    get_cov_group_req_forward,
    get_cov_group_mem_mmio_rw_block_range,
]

def cov_func_gen(name, point_name, point_hit_name):
    """ 生成一个只要 sample 就被记录的覆盖点函数 """
    def func(agent):
        group = CovGroup(name)
        group.add_watch_point(agent.bundle, {
            point_hit_name: lambda bundle: True,
        }, name=point_name)
        return group
    return func

# 需要单测的功能点
single_coverage_func = {
    "mmio block pipeline": cov_func_gen("mmio block pipeline".title(), "mmio block pipeline", "mmio block pipeline"),
    "mmio not burst": cov_func_gen("mmio not burst".title(), "mmio not burst", "mmio not burst"),
    "cache write back": cov_func_gen("cache write back".title(), "cache write back", "cache write back"),
    "cache read miss time more than read hit": cov_func_gen("cache read miss time more than read hit".title(), "cache read miss time more than read hit", "cache read miss time more than read hit"),
    "cache miss block pipeline": cov_func_gen("cache miss block pipeline".title(), "cache miss block pipeline", "cache miss block pipeline"),
    "cache key priority": cov_func_gen("cache key priority".title(), "cache key priority", "cache key priority"),
    "cache dirty block write back": cov_func_gen("cache dirty block write back".title(), "cache dirty block write back", "cache dirty block write back"),
    "clean blocks not write back": cov_func_gen("clean blocks not write back".title(), "clean blocks not write back", "clean blocks not write back"),
}
