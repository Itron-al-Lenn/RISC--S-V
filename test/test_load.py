from test.util import PROJ_PATH, check_ram, check_reg, run_till_end, runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'load.hex'

def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.test_load",
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

    await run_till_end(dut, INSTRUCTION_FILE)
    
    check_ram(dut, 0x00000200, 0xFF345678)
    check_reg(dut, 2, 0xFF345678)
    check_reg(dut, 3, 0x00003456)
    check_reg(dut, 4, 0xFFFFFFFF)
    check_reg(dut, 5, 0x00003456)
    check_reg(dut, 6, 0x000000FF)
