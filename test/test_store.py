from test.util import PROJ_PATH, check_ram, run_till_end, runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'store.hex'

def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.test_store",
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
        
    check_ram(dut, 0x00000200, 0x12345678)
    check_ram(dut, 0x00000204, 0x00005678)
    check_ram(dut, 0x00000208, 0x00000078)
    check_ram(dut, 0x0000020c, 0x34567878)
    check_ram(dut, 0x00000210, 0x00000012)
