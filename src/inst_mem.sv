module inst_mem #(
    parameter int MEM_SIZE = 1024
) (
    input  logic [31:0] address_i,
    output logic [31:0] instruction_o
);
  logic [31:0] mem[MEM_SIZE];

  string file;

  initial begin
    if (!$value$plusargs("INSTRUCTION_FILE=%s", file)) begin
      $display("ERROR: INSTRUCTION_FILE plusarg not provided!");
      $finish;
    end
    for (int i = 0; i < MEM_SIZE; i++) mem[i] = 32'b0;
    $readmemh(file, mem);
  end

  assign instruction_o = mem[address_i[31:2]];
endmodule
