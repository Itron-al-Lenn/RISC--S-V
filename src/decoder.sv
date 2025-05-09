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

  // field extraction
  wire [ 6:0] opcode = inst_i[6:0];
  wire [ 4:0] rd = inst_i[11:7];
  wire [ 2:0] funct3 = inst_i[14:12];
  wire [ 4:0] rs1 = inst_i[19:15];
  wire [ 4:0] rs2 = inst_i[24:20];
  wire [ 6:0] funct7 = inst_i[31:25];

  // immediate field subcomponents
  wire [11:0] imm_i = inst_i[31:20];
  wire        imm_i_sign = imm_i[11];
  wire [ 6:0] imm_s_hi = inst_i[31:25];
  wire [ 4:0] imm_s_lo = inst_i[11:7];
  wire        imm_s_sign = imm_s_hi[6];
  wire        imm_b_11 = inst_i[7];
  wire [ 5:0] imm_b_10_5 = inst_i[30:25];
  wire [ 3:0] imm_b_4_1 = inst_i[11:8];
  wire        imm_b_12 = inst_i[31];
  wire [19:0] imm_u = inst_i[31:12];
  wire [ 7:0] imm_j_19_12 = inst_i[19:12];
  wire        imm_j_11 = inst_i[20];
  wire [ 9:0] imm_j_10_1 = inst_i[30:21];
  wire        imm_j_20 = inst_i[31];

  assign opcode_o = opcode;
  assign rd_o     = rd;
  assign funct3_o = funct3;
  assign rs1_o    = rs1;
  assign rs2_o    = rs2;
  assign funct7_o = funct7;

  always_comb begin
    case (opcode)
      7'b0110011: format_o = R_TYPE;
      7'b1100111, 7'b0000011, 7'b0010011: format_o = I_TYPE;
      7'b0100011: format_o = S_TYPE;
      7'b1100011: format_o = B_TYPE;
      7'b0010111, 7'b0110111: format_o = U_TYPE;
      7'b1101111: format_o = J_TYPE;
      default: format_o = INVALID_TYPE;
    endcase
  end

  always_comb begin
    case (format_o)
      I_TYPE:  imm_o = {{20{imm_i_sign}}, imm_i};
      S_TYPE:  imm_o = {{20{imm_s_sign}}, imm_s_hi, imm_s_lo};
      B_TYPE:  imm_o = {{19{imm_b_12}}, imm_b_12, imm_b_11, imm_b_10_5, imm_b_4_1, 1'b0};
      U_TYPE:  imm_o = {imm_u, 12'b0};
      J_TYPE:  imm_o = {{11{imm_j_20}}, imm_j_20, imm_j_19_12, imm_j_11, imm_j_10_1, 1'b0};
      default: imm_o = 32'b0;
    endcase
  end

endmodule
