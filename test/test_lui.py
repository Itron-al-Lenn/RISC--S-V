from test.util import PROJ_PATH, check_reg, runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'lui.hex'

def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.test_lui",
)

    
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
    for _ in range(4):
        await RisingEdge(dut.clock)
    
    check_reg(dut, 1, 0x0007b000)
    check_reg(dut, 2, 0x000ea000)
    check_reg(dut, 3, 0x00159000)
