from test.util import PROJ_PATH, check_reg, run_till_end, runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'auipc.hex'

def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.test_auipc",
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
    
    check_reg(dut, 1, 0x0007b000)
    check_reg(dut, 2, 0x000ea004)
    check_reg(dut, 3, 0x00159008)
    check_reg(dut, 4, 0x001c800c)
