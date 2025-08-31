"""
一定注意：初始化的size，mem是kb，mmio是byte，read/write的是SimpleBus的size，即：2^size，读写1字节就传入0
"""

__all__ = [
    "MMIODevice",
    "MemDevice",
    "SimpleBusCmd",
    "DeviceRtn",
]

from enum import IntEnum

class SimpleBusCmd(IntEnum):
    # req
    READ        = 0b0000
    WRITE       = 0b0001
    READ_BURST  = 0b0010
    WRITE_BURST = 0b0011
    WRITE_LAST  = 0b0111
    PROBE       = 0b1000
    PREFETCH    = 0b0100
    # resp
    READ_LAST   = 0b0110
    WRITE_RESP  = 0b0101
    PROBE_HIT   = 0b1100
    PROBE_MISS  = 0b1000

def size_to_bytes(size: int) -> int:
    return 2**size

class DeviceRtn:
    def __init__(self, valid: bool, rdata: int, cmd: int):
        self.cmd = cmd
        self.rdata = rdata
        self.valid = valid

class MMIODevice:
    def __init__(self, base: int = 0x3000_0000, size: int = 0x1000):
        """ size: byte """
        self.base_address = base
        self.size = size
        self.end_address = base + size - 1
        self.buffer = bytearray(self.size)

        for i in range(32):
            self.buffer[i] = i+1 & 0xFF

    def validate_address_(self, address: int, size: int = 1) -> bool:
        return not (
            address < self.base_address or address + size - 1 > self.end_address
        )

    def validate_address(self, address: int, size: int = 1):
        assert self.validate_address_(address, size), f"address [${address}] with size [${size}] out of mmio"

    def read_data(self, addr: int, size: int) -> int:
        bytes_size = size_to_bytes(size)
        self.validate_address(addr, bytes_size)

        index = addr - self.base_address
        data = 0

        for i in range(bytes_size):
            data |= (self.buffer[index + i] << (8 * i))

        return data

    def write_data(self, addr: int, size: int, wdata: int, wmask: int):
        bytes_size = size_to_bytes(size)
        self.validate_address(addr, bytes_size)

        index = addr - self.base_address

        # print(f"\n\t  + mmio write data: {wdata:08X} to {addr:08X} with mask {wmask:08X} size: {size} bsize: {bytes_size}")

        for i in range(bytes_size):
            if wmask & (1 << i):
                byte = (wdata >> (8 * i)) & 0xFF
                self.buffer[index + i] = byte
                # print(f"\n\t  - mmio write data: {byte:02X} to {addr + i:08X}")
            # print(f"\n\t  - mmio write mask: {wmask:08X}  cond: {wmask & (1 << i)}")

    def apply(self, addr: int, size: int, cmd: SimpleBusCmd, wmask: int, wdata: int) -> DeviceRtn:
        self.validate_address(addr, size_to_bytes(size))
        offset = addr - self.base_address
        match cmd:
            case SimpleBusCmd.READ:
                return DeviceRtn(True, self.read_data(addr, size), SimpleBusCmd.READ_LAST)
            case SimpleBusCmd.WRITE:
                self.write_data(addr, size, wdata, wmask)
                return DeviceRtn(True, 0, SimpleBusCmd.WRITE_RESP)
            case SimpleBusCmd.PROBE:
                return DeviceRtn(True, 0, SimpleBusCmd.PROBE_HIT)
            case SimpleBusCmd.READ_BURST | SimpleBusCmd.WRITE_BURST | SimpleBusCmd.WRITE_LAST:
                assert False, "mmio shout not support burst"
            case _:
                return DeviceRtn(False, 0, SimpleBusCmd.PROBE_MISS)

class MemDevice:
    def __init__(self, size=33):
        """ 默认 32k 就是 0x0000 - 0x8000，这里比 Cache 大一点：0x8400 """
        self.size = size * 1024
        self.buffer = bytearray(self.size)

        self.base_address = 0x0000
        self.end_address  = self.base_address + self.size -1

        for i in range(256):
            self.buffer[i] = i & 0xFF

    def validate_address_(self, address: int, size: int = 1) -> bool:
        return not (
            address < self.base_address or address + size - 1 > self.end_address
        )

    def validate_address(self, address: int, size: int = 1):
        assert self.validate_address_(address, size), f"address [${address:08X}] with size [${size:02x}] out of mem [0x{self.base_address:08X}, 0x{self.end_address:08X}]"

    def read_bytes(self, addr: int, size: int) -> bytearray:
        self.validate_address(addr, size)
        return self.buffer[addr - self.base_address: addr - self.base_address + size]

    def write_bytes(self, addr: int, data: bytes):
        self.validate_address(addr, len(data))
        index = addr - self.base_address
        for i, byte in enumerate(data):
            self.buffer[index + i] = byte

    def read_data(self, addr: int, size: int) -> int:
        bytes_size = size_to_bytes(size)
        self.validate_address(addr, bytes_size)

        index = addr - self.base_address
        data = 0

        for i in range(bytes_size):
            data |= (self.buffer[index + i] << (8 * i))

        return data

    def write_data(self, addr: int, size: int, wdata: int, wmask: int):
        bytes_size = size_to_bytes(size)
        self.validate_address(addr, bytes_size)

        index = addr - self.base_address

        for i in range(bytes_size):
            if wmask & (1 << i):
                byte = (wdata >> (8 * i)) & 0xFF
                self.buffer[index + i] = byte

    def apply(self, addr: int, size: int, cmd: SimpleBusCmd, wmask: int, wdata: int) -> DeviceRtn:
        match cmd:
            case SimpleBusCmd.READ:
                rdata = self.read_data(addr, size)
                return DeviceRtn(True, rdata, SimpleBusCmd.READ_LAST)
            case SimpleBusCmd.WRITE:
                self.write_data(addr, size, wdata, wmask)
                return DeviceRtn(True, 0, SimpleBusCmd.WRITE_RESP)
            case SimpleBusCmd.READ_BURST:
                return DeviceRtn(False, 0, SimpleBusCmd.READ_BURST)
            case SimpleBusCmd.WRITE_BURST:
                return DeviceRtn(False, 0, SimpleBusCmd.WRITE_BURST)
            case SimpleBusCmd.WRITE_LAST:
                return DeviceRtn(False, 0, SimpleBusCmd.WRITE_RESP)
            case SimpleBusCmd.PROBE:
                return DeviceRtn(True, 0, SimpleBusCmd.PROBE_HIT if self.validate_address_(addr, size_to_bytes(size)) else SimpleBusCmd.PROBE_MISS)
            case SimpleBusCmd.PREFETCH:
                return DeviceRtn(True, 0, SimpleBusCmd.READ_LAST)
            case _:
                return DeviceRtn(False, 0, SimpleBusCmd.PROBE_MISS)

"""   ---   """

def test_mmio_device():
    mmio = MMIODevice(0x8000, 4)
    mmio.write_data(0x8000, 2, 0x12345678, 0xFFFFFFFF)
    assert mmio.read_data(0x8000, 2) == 0x12345678, f"[{mmio.read_data(0x8000, 2):08X}] [{0x12345678:08X}]"
    assert mmio.read_data(0x8000, 0) == 0x78, f"[{mmio.read_data(0x8000, 0):08X}] [{0x78:08X}]"
    assert mmio.read_data(0x8001, 0) == 0x56, f"[{mmio.read_data(0x8001, 0):08X}] [{0x56:08X}]"
    assert mmio.read_data(0x8002, 0) == 0x34, f"[{mmio.read_data(0x8002, 0):08X}] [{0x34:08X}]"
    assert mmio.read_data(0x8003, 0) == 0x12, f"[{mmio.read_data(0x8003, 0):08X}] [{0x12:08X}]"

def test_memo_device():
    mem = MemDevice(4)
    for i in range(256):
        resp = mem.write_data(i, 0, i, 0xFF)
    for i in range(256):
        assert mem.read_data(i, 0) == i

import pytest

@pytest.fixture
def mem():
    device = MemDevice(size=4)
    for i in range(min(256, device.size)):
        device.buffer[i] = i & 0xFF
    return device

@pytest.fixture
def mmio():
    return MMIODevice(0x8000, 4)

def test_memo_device_apply_write(mem):
    test_cases = [
        (0x100, 0, 0x55, 0b1, 1),
        (0x110, 1, 0xAABB, 0b11, 2),
        (0x120, 2, 0x11223344, 0b1111, 4),
        (0x130, 3, 0x1122334455667788, 0b11111111, 8),
    ]

    for addr, size_param, wdata, wmask, expected_bytes in test_cases:
        response = mem.apply(addr, size_param, SimpleBusCmd.WRITE, wmask, wdata)

        assert response.valid == True
        assert response.cmd == SimpleBusCmd.WRITE_RESP
        assert response.rdata == 0

        result = mem.read_data(addr, expected_bytes)
        expected_value = wdata & ((1 << (8 * expected_bytes)) - 1)
        assert result == expected_value

def test_memo_device_apply_probe(mem):
    test_cases = [
        (0x100, 0, True),
        (0x110, 1, True),
        (0x120, 2, True),
        (mem.end_address + 1, 0, False),
    ]

    for addr, size_param, should_hit in test_cases:
        if should_hit:
            response = mem.apply(addr, size_param, SimpleBusCmd.PROBE, 0, 0)
            assert response.valid == True
            assert response.cmd == SimpleBusCmd.PROBE_HIT
        else:
            hit = mem.validate_address_(addr, size_to_bytes(size_param))
            response = mem.apply(addr, size_param, SimpleBusCmd.PROBE, 0, 0)
            if not hit:
                assert response.cmd == SimpleBusCmd.PROBE_MISS

def test_memo_device_apply_prefetch(mem):
    test_cases = [0, 1, 2, 3]

    for size_param in test_cases:
        response = mem.apply(0x500, size_param, SimpleBusCmd.PREFETCH, 0, 0)

        assert response.valid == True
        assert response.cmd == SimpleBusCmd.READ_LAST
        expected_bytes = size_to_bytes(size_param)
        expected_data = mem.read_data(0x500, expected_bytes)
        assert response.rdata == expected_data

def test_mmio_device_apply(mmio):
    for i in range(4):
        resp = mmio.write_data(i + mmio.base_address, 0, i, 0xFF)
    for i in range(4):
        assert mmio.read_data(i + mmio.base_address, 0) == i

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-s", "-v"])
