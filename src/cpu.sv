`timescale 1ns / 1ps

import types::*;

module cpu #(
    parameter int MEM_SIZE = 1024
) (
    input logic clock,
    input logic reset
);
  // Program Counter
  logic [31:0] pc;
  logic [31:0] next_pc;

  // Instruction Fetch
  logic [31:0] instruction;

  // Decode Signals
  inst_format_e inst_format;
  logic [4:0] rs1_addr;
  logic [4:0] rs2_addr;
  logic [4:0] rd_addr;
  logic [31:0] imm;
  logic [6:0] opcode;
  logic [2:0] funct3;
  logic [6:0] funct7;

  // Register File Signals
  logic reg_write_enable;
  logic [31:0] rs1_data;
  logic [31:0] rs2_data;
  logic [31:0] rd_data;

  // ALU Signals
  logic [31:0] alu_result;
  logic [31:0] alu_operand1;
  logic [31:0] alu_operand2;
  alu_funct7_e alu_funct7;
  alu_funct3_e alu_funct3;

  // Control signals
  alu_src_e alu_src;
  wb_sel_e wb_sel;

  // Program Counter Logic
  always_ff @(posedge clock or posedge reset) begin
    if (reset) begin
      pc <= 32'h0;
    end else begin
      pc <= next_pc;
    end
  end

  assign next_pc = pc + 4;

  always_comb begin
    reg_write_enable = 1'b0;
    alu_src = REG;

    case (opcode)
      7'b0110111: begin  // LUI
        reg_write_enable = 1'b1;
        wb_sel           = WB_IMM;
      end

      7'b0010111: begin  // AUIPC
        reg_write_enable = 1'b1;
        wb_sel           = WB_PC_IMM;
      end

      7'b0110011: begin  // R-Type ALU
        reg_write_enable = 1'b1;
        alu_src          = REG;
        wb_sel           = WB_ALU;
      end

      7'b0010011: begin  // I-Type ALU
        reg_write_enable = 1'b1;
        alu_src          = IMM;
        wb_sel           = WB_ALU;
      end

      default: begin
        reg_write_enable = 1'b0;
        wb_sel           = WB_ALU;
      end
    endcase
  end

  // ALU definitions
  assign alu_operand1 = rs1_data;
  assign alu_operand2 = alu_src ? imm : rs2_data;
  assign alu_funct3   = alu_funct3_e'(funct3);
  assign alu_funct7   = alu_funct7_e'(funct7);

  logic [31:0] wb_data;

  always_comb begin
    case (wb_sel)
      WB_ALU:    wb_data = alu_result;
      WB_IMM:    wb_data = imm;
      WB_PC_IMM: wb_data = pc + imm;
      default:   wb_data = 32'b0;
    endcase
  end

  assign rd_data = wb_data;

  // Module instantiations
  inst_mem #(
      .MEM_SIZE(MEM_SIZE)
  ) instruction_memory (
      .address_i(pc),
      .instruction_o(instruction)
  );

  decoder instruction_decoder (
      .inst_i(instruction),
      .format_o(inst_format),
      .opcode_o(opcode),
      .funct3_o(funct3),
      .funct7_o(funct7),
      .rs1_o(rs1_addr),
      .rs2_o(rs2_addr),
      .rd_o(rd_addr),
      .imm_o(imm)
  );

  reg_file registers (
      .clock(clock),
      .write_enable(reg_write_enable),
      .rd_address(rd_addr),
      .rs1_address(rs1_addr),
      .rs2_address(rs2_addr),
      .rd_data(rd_data),
      .rs1_data(rs1_data),
      .rs2_data(rs2_data)
  );

  alu arithmetic_logic_unit (
      .result_o(alu_result),
      .operand_1_i(alu_operand1),
      .operand_2_i(alu_operand2),
      .funct7_i(alu_funct7),
      .funct3_i(alu_funct3)
  );

endmodule
