from test.util import check_reg

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def apu(dut):
    """Test CPU execution of OR(I) and XOR(I) instructions"""
    
    # Setup clock
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the CPU
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    
    # Run for 6 clock cycles (more than enough for our 4 instructions)
    for _ in range(7):
        await RisingEdge(dut.clock)
    
    check_reg(dut, 1, 1000)
    check_reg(dut, 2, 2000)
    check_reg(dut, 3, 2040)
    check_reg(dut, 4, 1080)
    check_reg(dut, 5, 2036)
    check_reg(dut, 6, 1652)
