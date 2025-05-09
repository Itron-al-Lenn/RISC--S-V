import random
from test.alu import alu_test

import cocotb


@cocotb.test()
async def alu(dut):
    for _ in range(50):
        op1 = random.randint(0, 200)
        op2 = random.randint(0, 200)
        await alu_test(dut, op1, op2, "ADD", op1 + op2)
        await alu_test(dut, op1, op2, "SUB", op1 - op2)
