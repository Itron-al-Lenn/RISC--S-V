from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'slt.hex'

def test_alu_slt():
    runner('alu', test_module="test.slt.alu")
    
def test_cpu_slt():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.slt.cpu")

