"""
官方示例：
 - 基本操作：成功写入、成功读取、无操作。
 - 边界状态：FIFO 空时尝试读取、FIFO 满时尝试写入、FIFO 空时写入、FIFO 满时读取。
 - 指针行为：写指针追上读指针（写满）、读指针追上写指针（读空）、指针回绕。
 - 数据完整性：写入的数据与后续读出的数据一致。
 - 复位行为：复位后 FIFO 应为空，指针复位。

功能描述：
    写入操作：
        当we_i为 1 时，FIFO 可以接收数据并存储到内部缓冲区ram中。
        写指针wptr指示下一个写入位置，随着每次写入操作递增。
        当 FIFO 已满时，full_o为 1，写入无效。

    读取操作：
        当re_i为 1 时，FIFO 将根据读取指针rptr从ram中输出数据。
        读取指针rptr指示下一个读取位置，随着每次读取操作递增。
        当 FIFO 为空时，empty_o为 1，读取无效。

    指针更新：
        wptr（写指针）和rptr（读指针）在时钟上升沿更新。rptr仅在re_i有效并且 FIFO 非空时更新，wptr仅在we_i有效并且 FIFO 非满时更新。
        FIFO 操作时，通过比较wptr和rptr的位置，FIFO 会自动调整数据的读写位置。

    计数器：
        counter用于跟踪 FIFO 中的数据量（从 0 到 16）。每次写入数据时，counter加 1，每次读取数据时，counter减 1。
        当counter值为 0 时，empty_o信号为 1，表示 FIFO 为空；当counter值为 16 时，full_o信号为 1，表示 FIFO 已满。

时序与复位
    同步时序： 所有的操作（写入、读取、指针更新、计数器更新）都在时钟信号的上升沿同步。
    复位： 在rst_n为低时，FIFO 内部所有指针（wptr、rptr）和数据输出（data_o）都将被清零，并且计数器counter会被复位为 0。

功能块说明
    指针更新：
        负责同步更新写入和读取指针。
        在每个时钟周期内，如果we_i为 1 并且 FIFO 不满，则数据会被写入 FIFO，且wptr自增。
        如果re_i为 1 并且 FIFO 不空，则会读取数据并将其输出，rptr自增。

    计数器更新：
        计数器counter用于追踪 FIFO 的当前数据量。
        每次写入时，counter自增；每次读取时，counter自减。
        FIFO 满时，counter达到 16，full_o为 1；FIFO 空时，counter为 0，empty_o为 1。

设计约束与假设
    数据宽度与深度： 本设计采用 32 位宽度，16 深度的 FIFO，适用于较小规模的数据缓存需求。
    时钟域： FIFO 模块假设在单一时钟域内工作，且时钟信号与复位信号是同步的。
    数据保持： FIFO 的数据存储在一个 16 个元素的 RAM 数组中，每个元素为 32 位。
    读写并行：FIFO 未满且不为空时，允许同时进行读、写操作。

边界条件
    当 FIFO 已满且we_i信号为高时，写入操作将被阻塞。
    当 FIFO 为空且re_i信号为高时，读取操作将被阻塞。
"""
# 归纳后的测试点：
"""
基本操作：
    测试读 测试写 测试无操作 测试同时读写-满空正常 测试读后写 测试满 测试空
边界状态：
    空读取被阻 满写入被阻 空写入 满读取
指针行为：
    写满 读空 指针回绕 计数器测试
数据完整性：
    使用循环进行多次读写
复位行为：
    复位后为空且指针与计数器为0
"""

from toffee.funcov import *
from agent import SyncFIFOAgent as FIFOAgent

def get_cover_base_operations(agent: FIFOAgent) -> CovGroup:
    group = CovGroup("base operations")
    group.add_watch_point(agent.bundle.internal.counter, {
        "empty": CovEq(0),
        "full": CovEq(16),
        "middle": CovIsInRange(1, 15),
    }, name="counter")
    group.add_watch_point(agent.bundle, {
        "write": lambda bundle: bundle.write.we_i.value and not bundle.read.re_i.value,
        "read": lambda bundle: bundle.read.re_i.value and not bundle.write.we_i.value,
        "noop": lambda bundle: not bundle.write.we_i.value and not bundle.read.re_i.value,
        "read_write": lambda bundle: bundle.write.we_i.value and bundle.read.re_i.value,
    }, name="rw")
    return group

def get_cover_boundary_operations(agent: FIFOAgent) -> CovGroup:
    group = CovGroup("boundary operations")
    group.add_watch_point(agent.bundle, {
        "empty_read": lambda bundle: bundle.common.empty_o.value and bundle.read.re_i.value,
        "full_write": lambda bundle: bundle.common.full_o.value and bundle.write.we_i.value,
        "empty_write": lambda bundle: bundle.common.empty_o.value and bundle.write.we_i.value,
        "full_read": lambda bundle: bundle.common.full_o.value and bundle.read.re_i.value,
    }, name="rwc")
    return group

def get_cover_point_behavior(agent: FIFOAgent) -> CovGroup:
    group = CovGroup("point behavior")
    group.add_watch_point(agent.bundle.internal.counter, {
        "empty": CovEq(0),
        "full": CovEq(16),
        "middle": CovIsInRange(1, 15),
    }, name="counter")
    group.add_watch_point(agent.bundle, {
        "write_full": lambda bundle: bundle.common.full_o.value and bundle.write.we_i.value,
        "read_empty": lambda bundle: bundle.common.empty_o.value and bundle.read.re_i.value,
        "ptr_cross": lambda bundle: bundle.internal.wptr.value == bundle.internal.rptr.value,
    }, name="ptr")
    return group

def get_cover_data_integrity(agent: FIFOAgent) -> CovGroup:
    group = CovGroup("data integrity")
    group.add_watch_point(agent.bundle.internal.counter, {
        "empty": CovEq(0),
        "full": CovEq(16),
        "middle": CovIsInRange(1, 15),
    }, name="counter")
    return group

def get_cover_reset_behavior(agent: FIFOAgent) -> CovGroup:
    group = CovGroup("reset behavior")
    group.add_watch_point(agent.bundle, {
        "reset": lambda bundle: not bundle.common.rst_n.value and bundle.common.empty_o.value and not bundle.common.full_o.value and bundle.internal.counter.value == 0,
        "normal": lambda bundle: bundle.common.rst_n.value,
    }, name="rst_n")
    return group
