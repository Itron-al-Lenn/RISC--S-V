from cocotb.triggers import Timer


async def alu_test(dut, operand_1, operand_2, operator, expected_result):
    """Helper function to help test the ALU"""
    match operator:
        case "SLL" | "SLLI":
            dut.funct3_i.value = 0b001
            dut.funct7_i.value = 0
        case "SRL" | "SRLI":
            dut.funct3_i.value = 0b101
            dut.funct7_i.value = 0
        case "SRA":
            dut.funct3_i.value = 0b101
            dut.funct7_i.value = 0b0100000
        case "SLT" | "SLTI":
            dut.funct3_i.value = 0b010
            dut.funct7_i.value = 0
        case "SLTU" | "SLTIU":
            dut.funct3_i.value = 0b011
            dut.funct7_i.value = 0
        case "OR" | "ORI":
            dut.funct3_i.value = 0b110
            dut.funct7_i.value = 0
        case "XOR" | "XORI":
            dut.funct3_i.value = 0b100
            dut.funct7_i.value = 0
        case "AND" | "ANDI":
            dut.funct3_i.value = 0b111
            dut.funct7_i.value = 0
        case "ADD" | "ADDI":
            dut.funct3_i.value = 0
            dut.funct7_i.value = 0
        case "SUB":
            dut.funct3_i.value = 0
            dut.funct7_i.value = 0b0100000
        case a:
            assert False, f"{a} does not match any operation"
        
    dut.operand_1_i.value = operand_1
    dut.operand_2_i.value = operand_2
    await Timer(1, units="ns")
    result = int(dut.result_o)
    # Use only the lowest 32 bits of the expected result. Python may support integer operations higher than 2^32, out microprocessor does not and doesn't have to
    expected_result &= 0xFFFFFFFF
    assert result == expected_result, f"Run {operator} for {operand_1} and {operand_2}: Expected {expected_result:08X}. got {result:08X}"
