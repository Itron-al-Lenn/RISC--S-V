import os
from pathlib import Path

from cocotb.runner import get_runner

PROJ_PATH = Path(os.path.dirname(__file__)).parent

def runner(feature: str, instruction_file: Path = Path(""), parameters: list[tuple[str, str]] = [], clean: bool = True, test_module: None | str = None):
    if test_module == None:
        test_module = f"test.test_{feature}"
        
    sources = [f for f in (PROJ_PATH / "src").iterdir() if f.is_file()]
    sources.sort(key=lambda f: 0 if f.name == "types.sv" else 1)
    for s in sources:
        print(s)
    build_args = [f'-DINSTRUCTION_FILE="{instruction_file}"']
    for parameter in parameters:
        build_args.append(f"-P{feature}.{parameter[0]}={parameter[1]}")
        
    
    runner = get_runner("icarus")
    runner.build(waves=True, sources=sources, hdl_toplevel=feature, clean=clean, build_args=build_args)

    runner.test(waves=True, hdl_toplevel=feature, test_module=test_module)

def check_reg(dut, reg_num: int, expected_value: int):
    value = int(dut.registers.register.value[reg_num])
    assert value == expected_value, f"Register x{reg_num} should be {expected_value}, got {value}"
    
def to_signed32(val):
    return val if val < 0x80000000 else val - 0x100000000
