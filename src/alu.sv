`timescale 1ns / 1ps
import types::*;

module alu (
    output logic [31:0] result_o,
    input logic [31:0] operand_1_i,
    input logic [31:0] operand_2_i,
    input alu_funct7_e funct7_i,
    input alu_funct3_e funct3_i
);
  logic [31:0] op2;

  always_comb begin
    case (funct7_i)
      NEG: op2 = -operand_2_i;
      default: op2 = operand_2_i;
    endcase

    case (funct3_i)
      ADD: result_o = operand_1_i + op2;
      AND: result_o = operand_1_i & op2;
      OR: result_o = operand_1_i | op2;
      XOR: result_o = operand_1_i ^ op2;
      default: result_o = 32'b0;
    endcase
  end
endmodule
