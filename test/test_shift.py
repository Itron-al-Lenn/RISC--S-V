from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'shift.hex'

def test_alu_shift():
    runner('alu', test_module="test.shift.alu")
    
def test_cpu_shift():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.shift.cpu",
)

