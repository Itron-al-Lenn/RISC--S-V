module branch_comp (
    input logic [31:0] op1_i,
    input logic [31:0] op2_i,
    input branch_op_e branch_op_i,
    input logic unsigned_i,
    output logic result_o
);
  always_comb begin
    case (branch_op_i)
      EQ: result_o = op1_i == op2_i;
      NE: result_o = op1_i != op2_i;
      LT: result_o = unsigned_i ? (op1_i < op2_i) : ($signed(op1_i) < $signed(op2_i));
      GE: result_o = unsigned_i ? (op1_i >= op2_i) : ($signed(op1_i) >= $signed(op2_i));
      default: result_o = 1'b0;
    endcase
  end
endmodule
