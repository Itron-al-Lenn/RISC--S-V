from test.util import check_reg

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def apu(dut):
    """Test CPU execution of ADD, ADDI and SUB instructions"""
    
    # Setup clock
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the CPU
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    dut.reset.value = 0
    
    # Run for 6 clock cycles (more than enough for our 4 instructions)
    for _ in range(6):
        await RisingEdge(dut.clock)
    
    check_reg(dut, 1, 10)
    check_reg(dut, 2, 15)
    check_reg(dut, 3, 25)
    check_reg(dut, 4, 15)
