import random
from test.util import PROJ_PATH, runner

import cocotb
from cocotb.triggers import Timer

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'basic.hex'

def test_inst_mem():
    runner('inst_mem',
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
    # Generate byte addresses that are multiples of 4 (word-aligned)
    random_addresses = [random.randint(0, 1023) * 4 for _ in range(num_test_addresses)]
    file_addresses = [addr * 4 for addr in instructions.keys()]  # Convert word indices to byte addresses

    if file_addresses:
        test_addresses = random_addresses + random.sample(file_addresses, min(10, len(file_addresses)))
    else:
        test_addresses = random_addresses
    
    dut._log.info(f"Testing addresses: {test_addresses}")
    
    for byte_addr in test_addresses:
        dut.address_i.value = byte_addr
        await Timer(1, units='ns')
        
        word_addr = byte_addr // 4
        actual_value = int(dut.instruction_o.value)
        expected_value = instructions.get(word_addr, 0)
        
        print(f"Debug: At byte address {byte_addr} (word {word_addr}), got {hex(actual_value)}, expected {hex(expected_value)}")
        
        assert actual_value == expected_value, \
            f"At address {byte_addr} (word {word_addr}), expected {hex(expected_value)}, got {hex(actual_value)}"
        
        dut._log.info(f"Address {byte_addr} (word {word_addr}): Instruction {hex(actual_value)} - PASS")
    
    dut._log.info("All instruction memory tests passed!")
