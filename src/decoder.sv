import types::*;

module decoder (
    input  logic [31:0] inst_i,
    output logic [ 6:0] opcode_o,
    output logic [ 2:0] funct3_o,
    output logic [ 6:0] funct7_o,
    output logic [ 4:0] rs1_o,
    output logic [ 4:0] rs2_o,
    output logic [ 4:0] rd_o,
    output logic [31:0] imm_o
);
  inst_format_e format;
  wire [31:0] imm_i = {{20{inst_i[31]}}, inst_i[31:20]};
  wire [31:0] imm_s = {{20{inst_i[31]}}, inst_i[31:25], inst_i[11:7]};
  wire [31:0] imm_b = {{19{inst_i[31]}}, inst_i[31], inst_i[7], inst_i[30:25], inst_i[11:8], 1'b0};
  wire [31:0] imm_u = {inst_i[31:12], 12'b0};
  wire [31:0] imm_j = {
    {11{inst_i[31]}}, inst_i[31], inst_i[19:12], inst_i[20], inst_i[30:21], 1'b0
  };

  assign opcode_o = inst_i[6:0];
  assign rd_o = inst_i[11:7];
  assign funct3_o = inst_i[14:12];
  assign rs1_o = inst_i[19:15];
  assign rs2_o = inst_i[24:20];
  assign funct7_o = (format == R_TYPE || (opcode_o == 7'b0010011 && funct3_o == 3'b101))
    ? inst_i[31:25]
    : 7'b0000000;

  always_comb begin
    case (opcode_o)
      7'b0110011:                         format = R_TYPE;
      7'b1100111, 7'b0000011, 7'b0010011: format = I_TYPE;
      7'b0100011:                         format = S_TYPE;
      7'b1100011:                         format = B_TYPE;
      7'b0010111, 7'b0110111:             format = U_TYPE;
      7'b1101111:                         format = J_TYPE;
      default:                            format = INVALID_TYPE;
    endcase

    case (format)
      I_TYPE:  imm_o = imm_i;
      S_TYPE:  imm_o = imm_s;
      B_TYPE:  imm_o = imm_b;
      U_TYPE:  imm_o = imm_u;
      J_TYPE:  imm_o = imm_j;
      default: imm_o = 32'b0;
    endcase
  end

endmodule
