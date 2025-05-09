from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'add.hex'

def test_alu_add():
    runner('alu', test_module="test.add.alu")
    
def test_cpu_add():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.add.cpu")

