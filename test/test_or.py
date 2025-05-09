from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'or.hex'

def test_alu_or():
    runner('alu', test_module="test.or.alu")
    
def test_cpu_or():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.or.cpu")

