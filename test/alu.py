
from cocotb.triggers import Timer

operator_name: dict[int, str] = {}

async def alu_test(dut, operand_1, operand_2, operator, expected_result):
    """Helper function to help test the ALU"""
    dut.operand_1_i = operand_1
    dut.operand_2_i = operand_2
    dut.operator_i = operator
    await Timer(1, units="ns")
    result = int(dut.result_o)
    assert result == expected_result, f"Run {operator_name[operator]} for {operand_1} and {operand_2}: Expected {expected_result}. got {result}"
