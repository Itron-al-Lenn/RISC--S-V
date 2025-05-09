import random
from test.alu import alu_test

import cocotb


@cocotb.test()
async def alu(dut):
    for _ in range(500):
        op1 = random.randint(0, 0xFFFFFFFF)
        op2 = random.randint(0, 0xFFFFFFFF)
        await alu_test(dut, op1, op2, "OR", op1 | op2)
        await alu_test(dut, op1, op2, "XOR", op1 ^ op2)
