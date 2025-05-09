from test.util import check_reg

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def cpu(dut):
    # Setup clock
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the CPU
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    dut.reset.value = 0

    # Run for sufficient clock cycles
    for _ in range(16):
        await RisingEdge(dut.clock)
    
    check_reg(dut, 1, 0xFFFFFFFF)
    check_reg(dut, 2, 0x00000004)
    check_reg(dut, 3, 0xFFFFFFF0)
    check_reg(dut, 4, 0x0FFFFFFF)
    check_reg(dut, 5, 0xFFFFFFFF)
    check_reg(dut, 6, 0xFFFFFFF8)
    check_reg(dut, 7, 0x1FFFFFFF)
    check_reg(dut, 8, 0xFFFFFFFF)
