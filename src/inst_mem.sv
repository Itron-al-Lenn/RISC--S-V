`timescale 1ns / 1ps
module inst_mem #(
    parameter int MEM_SIZE = 1024,
    parameter string INSTRUCTION_FILE = ""
) (
    input  logic [31:0] address_i,
    output logic [31:0] instruction_o
);
  logic [31:0] mem[MEM_SIZE];


  initial begin
    for (int i = 0; i < MEM_SIZE; i++) mem[i] = 32'h0;

    $display("Reading instructions from file: %s", INSTRUCTION_FILE);
    if (INSTRUCTION_FILE != "") $readmemh(INSTRUCTION_FILE, mem);
  end

  assign instruction_o = mem[address_i];
endmodule
