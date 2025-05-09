import random
from test.alu import alu_test
from test.util import to_signed32

import cocotb


@cocotb.test()
async def alu(dut):
    for _ in range(500):
        op1 = random.randint(0, 0xFFFFFFFF)
        op2 = random.randint(0, 0xFFFFFFFF)
        await alu_test(dut, op1, op2, "SLT", 1 if to_signed32(op1) < to_signed32(op2) else 0)
        await alu_test(dut, op1, op2, "SLTU", 1 if op1 < op2 else 0)
