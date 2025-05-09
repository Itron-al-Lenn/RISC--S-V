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
    
    # Check register values via the register file
    reg = dut.registers.register
    x1 = reg.value[1]
    x2 = reg.value[2]
    x3 = reg.value[3]
    x4 = reg.value[4]
    
    # Verify results
    assert x1 == 10, f"Register x1 should be 10, got {x1}"
    assert x2 == 15, f"Register x2 should be 15, got {x2}"
    assert x3 == 25, f"Register x3 should be 25, got {x3}"
    assert x4 == 15, f"Register x4 should be 15, got {x4}"
