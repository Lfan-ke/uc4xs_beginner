from toffee import Bundle, Signals

class WriteBundle(Bundle):

    we_i, data_i = Signals(2)

    async def enqueue(self, data):
        self.we_i.value = 1
        self.data_i.value = data
        await self.step(1)
        self.we_i.value = 0
        await self.step(1)

class ReadBundle(Bundle):

    re_i, data_o = Signals(2)

    async def dequeue(self):
        self.re_i.value = 1
        await self.step(1)
        self.re_i.value = 0
        await self.step(1)
        return self.data_o.value

class CommonBundle(Bundle):

    clk, rst_n, full_o, empty_o = Signals(4)

class InternalBundle(Bundle):

    wptr, rptr, counter = Signals(3)

class SyncFIFOBundle(Bundle):

    write = WriteBundle()
    read = ReadBundle()
    common = CommonBundle()
    internal = InternalBundle.from_regex(".*?_(.*)")

    async def enqueue(self, data):
        await self.write.enqueue(data)

    async def dequeue(self):
        return await self.read.dequeue()

    async def read_write(self, data):
        self.write.we_i.value = 1
        self.write.data_i.value = data
        self.read.re_i.value = 1
        await self.step(1)
        self.read.re_i.value = 0
        self.write.we_i.value = 0
        await self.step(1)
        return self.read.data_o.value

    async def is_empty(self):
        return self.common.empty_o.value == 1

    async def is_full(self):
        return self.common.full_o.value == 1
