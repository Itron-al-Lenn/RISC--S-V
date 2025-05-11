`timescale 1ns / 1ps
import types::*;

module ram #(
    parameter int MEM_SIZE = 4096
) (
    input  logic              clk_i,
    input  logic       [31:0] address_i,
    input  logic              sign_extend_i,
    input  load_size_e        size_i,
    input  logic       [31:0] data_i,
    input  logic              wr_enable_i,
    output logic       [31:0] output_o
);
  logic [31:0] mem[MEM_SIZE];

  initial begin
    for (int i = 0; i < MEM_SIZE; i++) mem[i] = 32'b0;
  end

  localparam int ADDRWIDTH = $clog2(MEM_SIZE);
  logic [ADDRWIDTH-1:0] addr;
  assign addr = address_i[ADDRWIDTH+1:2];

  logic [31:0] read_data;
  always_ff @(posedge clk_i) begin
    case (size_i)
      BYTE: begin
        if (sign_extend_i) read_data <= {{24{mem[addr][7]}}, mem[addr][7:0]};
        else read_data <= {24'b0, mem[addr][7:0]};
      end
      HALF_WORD: begin
        if (sign_extend_i) read_data <= {{16{mem[addr][15]}}, mem[addr][15:0]};
        else read_data <= {16'b0, mem[addr][15:0]};
      end
      WORD:    read_data <= mem[addr];
      default: read_data <= 32'b0;
    endcase
  end
  assign output_o = read_data;

  always_ff @(posedge clk_i) begin
    if (wr_enable_i) begin
      case (size_i)
        BYTE:      mem[addr][7:0] <= data_i[7:0];
        HALF_WORD: mem[addr][15:0] <= data_i[15:0];
        WORD:      mem[addr] <= data_i;
        default:   ;
      endcase
    end
  end
endmodule
