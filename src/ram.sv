`timescale 1ns / 1ps
import types::*;

module ram #(
    parameter int MEM_SIZE = 4096
) (
    input  logic             clk_i,
    input  logic      [31:0] address_i,
    input  logic             unsigned_i,
    input  ram_size_e        size_i,
    input  logic      [31:0] data_i,
    input  logic             wr_enable_i,
    output logic      [31:0] output_o
);
  logic [7:0] mem[4*MEM_SIZE];

  wire [7:0] by;
  wire by_sign;
  assign by = mem[address_i];
  assign by_sign = by[7];
  wire [15:0] hw;
  wire hw_sign;
  assign hw = {mem[address_i+1], mem[address_i]};
  assign hw_sign = hw[15];
  wire [31:0] wd;
  assign wd = {mem[address_i+3], mem[address_i+2], mem[address_i+1], mem[address_i]};

  initial begin
    for (int i = 0; i < 4 * MEM_SIZE; i++) mem[i] = 8'b0;
    output_o = 32'b0;
  end

  // Read
  always_comb begin
    case (size_i)
      BYTE: begin
        output_o = (unsigned_i) ? {24'b0, by} : {{24{by_sign}}, by};
      end
      HALF_WORD: begin
        output_o = (unsigned_i) ? {16'b0, hw} : {{16{hw_sign}}, hw};
      end
      WORD: begin
        output_o = wd;
      end
      default: output_o = 32'b0;
    endcase
  end

  // Write
  always_ff @(posedge clk_i) begin
    if (wr_enable_i) begin
      case (size_i)
        BYTE: mem[address_i] <= data_i[7:0];
        HALF_WORD: begin
          mem[address_i]   <= data_i[7:0];
          mem[address_i+1] <= data_i[15:8];
        end
        WORD: begin
          mem[address_i]   <= data_i[7:0];
          mem[address_i+1] <= data_i[15:8];
          mem[address_i+2] <= data_i[23:16];
          mem[address_i+3] <= data_i[31:24];
        end
        default: ;
      endcase
    end
  end
endmodule
