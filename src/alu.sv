import types::alu_operation_e;

module alu (
    output logic [31:0] result_o,
    input logic [31:0] operand_1_i,
    input logic [31:0] operand_2_i,
    input alu_funct7_e funct7_i,
    input alu_funct3_e funct3_i
);
  always_comb begin
    case (funct7_i)
    endcase

    case (funct3_i)
    endcase
  end
endmodule
