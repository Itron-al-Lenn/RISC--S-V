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
    """Test writing and reading bytes, half-words, and words from RAM, including misaligned accesses."""
    cocotb.start_soon(Clock(dut.clk_i, 10, units="ns").start())
    dut.unsigned_i.value = 1  # Use unsigned for simplicity

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

    # Test aligned word
    word_addr = 0x10
    word_data = 0xAABBCCDD
    await write(word_addr, word_data, WORD)
    read_data = await read(word_addr, WORD)
    assert read_data == word_data, f"Word read {read_data:#X} != written {word_data:#X}"

    # Test misaligned word (address + 1)
    word_addr_mis = 0x11
    word_data_mis = 0x12345678
    await write(word_addr_mis, word_data_mis, WORD)
    read_data = await read(word_addr_mis, WORD)
    assert read_data == word_data_mis, f"Misaligned word read {read_data:#X} != written {word_data_mis:#X}"

    # Test aligned halfword
    half_addr = 0x20
    half_data = 0xFACE
    await write(half_addr, half_data, HALF_WORD)
    read_data = await read(half_addr, HALF_WORD)
    assert (read_data & 0xFFFF) == half_data, f"Half-word read {read_data:#X} != written {half_data:#X}"

    # Test misaligned halfword (address + 1)
    half_addr_mis = 0x21
    half_data_mis = 0xBEEF
    await write(half_addr_mis, half_data_mis, HALF_WORD)
    read_data = await read(half_addr_mis, HALF_WORD)
    assert (read_data & 0xFFFF) == half_data_mis, f"Misaligned half-word read {read_data:#X} != written {half_data_mis:#X}"

    # Test aligned byte
    byte_addr = 0x30
    byte_data = 0x5A
    await write(byte_addr, byte_data, BYTE)
    read_data = await read(byte_addr, BYTE)
    assert (read_data & 0xFF) == byte_data, f"Byte read {read_data:#X} != written {byte_data:#X}"

    # Test misaligned byte (address + 1)
    byte_addr_mis = 0x31
    byte_data_mis = 0x77
    await write(byte_addr_mis, byte_data_mis, BYTE)
    read_data = await read(byte_addr_mis, BYTE)
    assert (read_data & 0xFF) == byte_data_mis, f"Misaligned byte read {read_data:#X} != written {byte_data_mis:#X}"

    # Randomized accesses, including misaligned
    for _ in range(100):
        # Random misaligned address
        addr = random.randint(0, 4*4095)
        size = random.choice([BYTE, HALF_WORD, WORD])
        if size == BYTE:
            data = random.randint(0, 0xFF)
            await write(addr, data, BYTE)
            read_back = await read(addr, BYTE)
            assert (read_back & 0xFF) == data, f"Random byte: {read_back:#X} != {data:#X} @ {addr:#X}"
        elif size == HALF_WORD:
            data = random.randint(0, 0xFFFF)
            await write(addr, data, HALF_WORD)
            read_back = await read(addr, HALF_WORD)
            assert (read_back & 0xFFFF) == data, f"Random halfword: {read_back:#X} != {data:#X} @ {addr:#X}"
        elif size == WORD:
            data = random.randint(0, 0xFFFFFFFF)
            await write(addr, data, WORD)
            read_back = await read(addr, WORD)
            assert read_back == data, f"Random word: {read_back:#X} != {data:#X} @ {addr:#X}"
