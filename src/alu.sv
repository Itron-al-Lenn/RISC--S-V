`timescale 1ns / 1ps
import types::*;

module alu (
    output logic [31:0] result_o,
    input logic [31:0] operand_1_i,
    input logic [31:0] operand_2_i,
    input alu_funct7_e funct7_i,
    input alu_funct3_e funct3_i
);
  logic [4:0] shift_amt;
  assign shift_amt = operand_2_i[4:0];

  always_comb begin
    case ({
      funct7_i, funct3_i
    })
      // Numerical Operations
      {NORMAL, ADD} : result_o = operand_1_i + operand_2_i;
      {ALT,    ADD} : result_o = operand_1_i - operand_2_i;

      // Bit Operations
      {NORMAL, AND} : result_o = operand_1_i & operand_2_i;
      {NORMAL, OR} :  result_o = operand_1_i | operand_2_i;
      {NORMAL, XOR} : result_o = operand_1_i ^ operand_2_i;

      // SLT
      {NORMAL, SLT} :  result_o = ($signed(operand_1_i) < $signed(operand_2_i)) ? 1 : 0;
      {NORMAL, SLTU} : result_o = (operand_1_i < operand_2_i) ? 1 : 0;

      // Bit Shifts
      {NORMAL, SLL} : result_o = operand_1_i << shift_amt;
      {NORMAL, SRL} : result_o = operand_1_i >> shift_amt;
      {ALT, SRL} : result_o = $signed(operand_1_i) >>> shift_amt;

      default: result_o = 32'b0;
    endcase
  end
endmodule
