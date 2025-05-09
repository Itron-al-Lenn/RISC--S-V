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

    # Check register values via the register file
    reg = dut.registers.register
    x1 = int(reg.value[1])
    x2 = int(reg.value[2])
    x3 = int(reg.value[3])
    x4 = int(reg.value[4])
    
    # Verify results
    assert x1 == 1000, f"Register x1 should be 1000, got {x1}"
    assert x2 == 2000, f"Register x2 should be 2000, got {x2}"
    assert x3 == 960,  f"Register x3 should be 960, got {x3}"
    assert x4 == 232,  f"Register x4 should be 232, got {x4}"
