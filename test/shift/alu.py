import random
from test.alu import alu_test
from test.util import to_signed32

import cocotb


@cocotb.test()
async def alu(dut):
    for _ in range(500):
        op1 = random.randint(0, 0xFFFFFFFF)
        op2 = random.randint(0, 0xFFFFFFFF)

        shamt = op2 & 0x1F

        await alu_test(dut, op1, op2, "SLL", op1 << shamt)
        await alu_test(dut, op1, op2, "SRL", op1 >> shamt)
        await alu_test(dut, op1, op2, "SRA", to_signed32(op1) >> shamt)
