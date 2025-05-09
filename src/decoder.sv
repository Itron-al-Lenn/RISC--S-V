import types::inst_format_e;

module decoder (
    input logic [31:0] inst_i,
    output inst_format_e format_o,
    output logic [6:0] opcode_o,
    output logic [2:0] funct3_o,
    output logic [6:0] funct7_o,
    output logic [4:0] rs1_o,
    output logic [4:0] rs2_o,
    output logic [4:0] rd_o,
    output logic [31:0] imm_o
);

  assign opcode_o = instruction[6:0];
  assign rd_o     = instruction[11:7];
  assign funct3_o = instruction[14:12];
  assign rs1_o    = instruction[19:15];
  assign rs2_o    = instruction[24:20];
  assign funct7_o = instruction[31:25];

  always_comb begin
    case (opcode)
      7'b0110011: format_o = R_TYPE;
      7'b1100111, 7'b0000011, 7'b0010011: format_o = I_TYPE;
      7'b0100011: format_o = S_TYPE;
      7'b1100011: format_o = B_TYPE;
      7'b0010111, 7'b0110111: format_o = U_TYPE;
      7'b1101111, 7'b1100111: format_o = J_TYPE;
      default: format_o = INVALID_TYPE;
    endcase
  end

  always_comb begin
    case (format_o)
      I_TYPE:  imm_o = {{20{inst_i[31]}}, inst_i[31:20]};
      S_TYPE:  imm_o = {{20{inst_i[31]}}, inst_i[30:25], inst[11:7]};
      B_TYPE:  imm_o = {{19{inst_i[31]}}, inst_i[7], inst_i[30:25], inst[11:8], 1'b0};
      U_TYPE:  imm_o = {inst_i[31:12], 12'b0};
      J_TYPE:  imm_o = {{11{inst_i[31]}}, inst_i[19:12], inst_i[20], inst[30:21], 1'b0};
      default: imm_o = 32'b0;
    endcase
  end

endmodule
