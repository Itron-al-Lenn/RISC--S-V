
from cocotb.triggers import Timer


async def alu_test(dut, operand_1, operand_2, operator, expected_result):
    """Helper function to help test the ALU"""
    match operator:
        case "ADD" | "ADDI":
            dut.funct3_i.value = 0
            dut.funct7_i.value = 0
        case "SUB":
            dut.funct3_i.value = 0
            dut.funct7_i.value = 0b0100000
        
    dut.operand_1_i.value = operand_1
    dut.operand_2_i.value = operand_2
    await Timer(1, units="ns")
    result = int(dut.result_o)
    # If result is negative in two's complement, convert to Python signed integer
    if result > 0x7FFFFFFF:  # Check if MSB is set (negative number)
        result = result - (1 << 32)  # Convert to Python negative number
    assert result == expected_result, f"Run {operator} for {operand_1} and {operand_2}: Expected {expected_result}. got {result}"
