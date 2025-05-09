import random
from test.util import PROJ_PATH, runner

import cocotb
from cocotb.triggers import Timer

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'basic.hex'

def test_inst_mem():
    runner('inst_mem', ['inst_mem.sv'],
           instruction_file=INSTRUCTION_FILE
           )

def read_hex_file(file_path):
    instructions = {}
    address = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            try:
                instr = int(line, 16)
                instructions[address] = instr
                address += 1
            except ValueError:
                continue
    
    return instructions

@cocotb.test()
async def inst_mem_basic(dut):
    instructions = read_hex_file(INSTRUCTION_FILE)
    
    num_test_addresses = 10
    random_addresses = [random.randint(0, 1024) for _ in range(num_test_addresses)]
    file_addresses = list(instructions.keys()) # Also test addresses that for sure are != 0
    if file_addresses:
        test_addresses = random_addresses + random.sample(file_addresses, min(10, len(file_addresses)))
    else:
        test_addresses = random_addresses
    
    dut._log.info(f"Testing addresses: {test_addresses}")
    
    for addr in test_addresses:
        dut.address_i.value = addr
        await Timer(1, units='ns')
        
        actual_value = int(dut.instruction_o.value)
        expected_value = instructions.get(addr, 0)
        
        print(f"Debug: At address {addr}, got {hex(actual_value)}, expected {hex(expected_value)}")
        
        assert dut.instruction_o.value == expected_value, \
            f"At address {addr}, expected {hex(expected_value)}, got {hex(actual_value)}"
        
        dut._log.info(f"Address {addr}: Instruction {hex(actual_value)} - PASS")
    
    dut._log.info("All instruction memory tests passed!")
