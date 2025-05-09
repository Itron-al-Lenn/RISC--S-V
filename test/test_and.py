from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'and.hex'

def test_alu_and():
    runner('alu', ['types.sv','alu.sv'], test_module="test.and.alu")
    
def test_cpu_and():
    runner('cpu', ['types.sv', 'alu.sv', 'decoder.sv', 'inst_mem.sv', 'reg_file.sv', 'cpu.sv'],
           instruction_file=INSTRUCTION_FILE,
           test_module="test.and.cpu",
)

