import random
from test.util import runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

BYTE      = 0b000
HALF_WORD = 0b001
WORD      = 0b010

def test_ram():
    runner('ram')

@cocotb.test()
async def basic_write_read(dut):
    """Test writing and reading bytes, half-words, and words from RAM."""
    cocotb.start_soon(Clock(dut.clk_i, 10, units="ns").start())
    await RisingEdge(dut.clk_i)

    async def write(address, data, size):
        dut.address_i.value = address
        dut.size_i.value = size
        dut.data_i.value = data
        dut.wr_enable_i.value = 1
        await RisingEdge(dut.clk_i)
        dut.wr_enable_i.value = 0
        await RisingEdge(dut.clk_i)

    async def read(address, size):
        dut.address_i.value = address
        dut.size_i.value = size
        dut.wr_enable_i.value = 0
        await RisingEdge(dut.clk_i)
        return dut.output_o.value.integer

    word_addr = 0x10
    word_data = 0xAABBCCDD
    await write(word_addr, word_data, WORD)
    read_data = await read(word_addr, WORD)
    assert read_data == word_data, f"Word read {read_data:#X} != written {word_data:#X}"

    half_addr = 0x20
    half_data = 0xFACE
    await write(half_addr, half_data, HALF_WORD)
    read_data = await read(half_addr, HALF_WORD)
    assert (read_data & 0xFFFF) == half_data, f"Half-word read {read_data:#X} != written {half_data:#X}"

    byte_addr = 0x30
    byte_data = 0x5A
    await write(byte_addr, byte_data, BYTE)
    read_data = await read(byte_addr, BYTE)
    assert (read_data & 0xFF) == byte_data, f"Byte read {read_data:#X} != written {byte_data:#X}"

    for _ in range(100):
        addr = random.randint(2048, 4096) << 2  # word-aligned
        data = random.randint(0, 0xFFFFFFFF)
        await write(addr, data, WORD)
        read_back = await read(addr, WORD)
        assert read_back == data, f"Random word: {read_back:#X} != {data:#X}"
