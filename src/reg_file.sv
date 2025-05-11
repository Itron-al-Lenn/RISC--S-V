`timescale 1ns / 1ps
module reg_file (
    input         clock,
    input         write_enable,
    input  [ 4:0] rd_address,
    input  [ 4:0] rs1_address,
    input  [ 4:0] rs2_address,
    input  [31:0] rd_data,
    output [31:0] rs1_data,
    output [31:0] rs2_data
);
  logic [31:0] register[32];

  // Read ports for rs1 and rs2
  assign rs1_data = register[rs1_address];
  assign rs2_data = register[rs2_address];

  // Initialize all registers to 0
  initial begin
    for (int i = 0; i < 32; i = i + 1) begin
      register[i] = 32'b0;
    end
  end

  // Write port for rd
  always_ff @(posedge clock) begin
    if (write_enable) begin
      // Only write if we are not on register x0
      if (rd_address != 5'b0) begin
        register[rd_address] <= rd_data;
      end
    end
  end
endmodule
