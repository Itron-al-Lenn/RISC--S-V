import types::alu_operation_e;

module alu (
    output logic [31:0] result_o,
    input logic [31:0] operand_1_i,
    input logic [31:0] operand_2_i,
    input alu_operation_e operation_i
);
  always_comb begin
    unique case (operation_i)
      // Will be added when implementing the operations
    endcase
  end
endmodule
