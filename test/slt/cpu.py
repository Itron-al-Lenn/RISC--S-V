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
    for _ in range(7):
        await RisingEdge(dut.clock)
    
    # Verify results
    check_reg(dut, 1, 0xFFFFFFFF)
    check_reg(dut, 2, 2000)
    check_reg(dut, 3, 1)
    check_reg(dut, 4, 0)
    check_reg(dut, 5, 1)
    check_reg(dut, 6, 0)
