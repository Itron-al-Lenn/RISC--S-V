import os
from pathlib import Path

from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge

PROJ_PATH = Path(os.path.dirname(__file__)).parent

def runner(feature: str, instruction_file: Path = Path(""), parameters: list[tuple[str, str]] = [], clean: bool = True, test_module: None | str = None):
    if test_module == None:
        test_module = f"test.test_{feature}"
        
    sources = [f for f in (PROJ_PATH / "src").iterdir() if f.is_file()]
    sources.sort(key=lambda f: 0 if f.name == "types.sv" else 1)
    build_args = [f'-DINSTRUCTION_FILE="{instruction_file}"']
    for parameter in parameters:
        build_args.append(f"-P{feature}.{parameter[0]}={parameter[1]}")
        
    
    runner = get_runner("icarus")
    runner.build(waves=True, sources=sources, hdl_toplevel=feature, clean=clean, build_args=build_args)

    runner.test(waves=True, hdl_toplevel=feature, test_module=test_module)

def check_reg(dut, reg_num: int, expected_value: int):
    value = int(dut.registers.register.value[reg_num])
    assert value == expected_value, f"Register x{reg_num} should be {expected_value:08X}, got {value:08X}"
    
def check_ram(dut, address: int, expected_value: int):
    ram = dut.random_access_memory.mem.value
    value = (
        int(ram[address]) |
        (int(ram[address+1]) << 8) |
        (int(ram[address+2]) << 16) |
        (int(ram[address+3]) << 24)
    )
    assert value == expected_value, f"RAM at {address:08X} should be {expected_value:08X}, got {value:08X}"
    
def to_signed32(val):
    return val if val < 0x80000000 else val - 0x100000000
    
def count_lines(filename):
    with open(filename, "r") as f:
        return sum(1 for _ in f)

async def run_till_end(dut, instruction_file, extra_cycles=2):
    num_instructions = count_lines(instruction_file)
    for _ in range(num_instructions + extra_cycles):
        await RisingEdge(dut.clock)
