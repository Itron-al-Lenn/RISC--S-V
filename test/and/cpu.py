from test.util import check_reg

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


@cocotb.test()
async def test_and_and_andi(dut):
    """Test CPU execution of AND and ANDI instructions"""

    # Setup clock
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the CPU
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    dut.reset.value = 0

    # Run for sufficient clock cycles
    for _ in range(8):
        await RisingEdge(dut.clock)
    
    # Verify results
    check_reg(dut, 1, 1000)
    check_reg(dut, 2, 2000)
    check_reg(dut, 3, 960)
    check_reg(dut, 4, 232)
