`timescale 1ns / 1ps

import types::*;

module cpu #(
    parameter int MEM_SIZE = 1024
) (
    input logic clock,
    input logic reset
);
  // Program Counter
  logic         [31:0] pc;
  logic         [31:0] next_pc;

  // Instruction Fetch
  logic         [31:0] instruction;

  // Decode Signals
  inst_format_e        inst_format;
  logic         [ 4:0] rs1_addr;
  logic         [ 4:0] rs2_addr;
  logic         [ 4:0] rd_addr;
  logic         [31:0] imm;
  logic         [ 6:0] opcode;
  logic         [ 2:0] funct3;
  logic         [ 6:0] funct7;

  // Register File Signals
  logic                reg_wr_enable;
  logic         [31:0] rs1_data;
  logic         [31:0] rs2_data;
  logic         [31:0] rd_data;

  // ALU Signals
  logic         [31:0] alu_result;
  logic         [31:0] alu_operand1;
  logic         [31:0] alu_operand2;
  alu_funct7_e         alu_funct7;
  alu_funct3_e         alu_funct3;

  // RAM Signals
  logic         [31:0] ram_out;
  logic         [31:0] ram_addr;
  logic                ram_wr_enable;
  logic                ram_unsigned;
  ram_size_e           ram_size;
  logic         [31:0] ram_data;

  // Control signals
  alu_src_e            alu_src;
  wb_sel_e             wb_sel;

  assign next_pc = pc + 4;

  wire funct3_2 = funct3[2];
  wire [1:0] funct3_10 = funct3[1:0];

  // Control Flow
  always_comb begin
    reg_wr_enable = 1'b0;
    ram_wr_enable = 1'b0;
    alu_src = REG;

    case (opcode)
      7'b0110111: begin  // LUI
        reg_wr_enable = 1'b1;
        wb_sel        = WB_IMM;
      end

      7'b0010111: begin  // AUIPC
        reg_wr_enable = 1'b1;
        wb_sel        = WB_PC_IMM;
      end

      7'b0110011: begin  // R-Type ALU
        reg_wr_enable = 1'b1;
        alu_src       = REG;
        wb_sel        = WB_ALU;
      end

      7'b0010011: begin  // I-Type ALU
        reg_wr_enable = 1'b1;
        alu_src       = IMM;
        wb_sel        = WB_ALU;
      end

      7'b0000011: begin  // Load
        reg_wr_enable = 1'b1;
        ram_unsigned  = funct3_2;
        ram_addr      = rs1_data + imm;
        ram_size      = ram_size_e'(funct3_10);
        wb_sel        = WB_RAM;
      end

      7'b0100011: begin  // Store
        ram_wr_enable = 1'b1;
        ram_addr = rs1_data + imm;
        ram_size = ram_size_e'(funct3_10);
      end

      7'b1101111: begin  // JAL
        reg_wr_enable = 1'b1;
        alu_src = IMM;
        wb_sel = WB_JAL;
      end

      7'b1100111: begin  // JALR
        reg_wr_enable = 1'b1;
        wb_sel = WB_JALR;
      end

      default: begin
        wb_sel = WB_ALU;
      end
    endcase
  end

  // RAM definitions
  assign ram_data = rs2_data;

  // ALU definitions
  assign alu_operand1 = rs1_data;
  assign alu_operand2 = alu_src ? imm : rs2_data;
  assign alu_funct3 = alu_funct3_e'(funct3);
  assign alu_funct7 = alu_funct7_e'(funct7);

  always_comb begin
    case (wb_sel)
      WB_ALU:          rd_data = alu_result;
      WB_IMM:          rd_data = imm;
      WB_PC_IMM:       rd_data = pc + imm;
      WB_RAM:          rd_data = ram_out;
      WB_JAL, WB_JALR: rd_data = next_pc;
      default:         rd_data = 32'b0;
    endcase
  end

  // Program Counter Logic
  always_ff @(posedge clock or posedge reset) begin
    if (reset) begin
      pc <= 32'h0;
    end else begin
      case (wb_sel)
        WB_JAL:  pc <= pc + imm;
        WB_JALR: pc <= (rs1_data + imm) & ~32'b00000000000000000000000000000001;
        default: pc <= next_pc;
      endcase
    end
  end

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
      .wr_enable(reg_wr_enable),
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

  ram random_access_memory (
      .clk_i(clock),
      .address_i(ram_addr),
      .unsigned_i(ram_unsigned),
      .size_i(ram_size),
      .data_i(ram_data),
      .wr_enable_i(ram_wr_enable),
      .output_o(ram_out)
  );
endmodule
