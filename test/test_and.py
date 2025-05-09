from test.util import PROJ_PATH, runner

INSTRUCTION_FILE = PROJ_PATH / 'test' / 'instructions' / 'and.hex'

def test_alu_and():
    runner('alu', test_module="test.and.alu")
    
def test_cpu_and():
    runner('cpu',
           instruction_file=INSTRUCTION_FILE,
           test_module="test.and.cpu",
)

