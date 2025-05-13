from test.util import PROJ_PATH, check_reg, run_till_end, runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'branch.hex'

def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.test_branch",
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
    
    check_reg(dut, 10, 0)
    check_reg(dut, 11, 1)
    check_reg(dut, 12, 0)
    check_reg(dut, 13, 0)
    check_reg(dut, 14, 1)
    check_reg(dut, 15, 1)
    check_reg(dut, 16, 0)
