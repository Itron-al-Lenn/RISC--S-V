package types;
  typedef enum logic [6:0] {
    NORMAL = 7'b0000000,
    ALT    = 7'b0100000
  } alu_funct7_e;

  typedef enum logic [2:0] {
    ADD  = 3'b000,
    AND  = 3'b111,
    OR   = 3'b110,
    XOR  = 3'b100,
    SLT  = 3'b010,
    SLTU = 3'b011,
    SLL  = 3'b001,
    SRL  = 3'b101
  } alu_funct3_e;

  typedef enum {
    R_TYPE,
    I_TYPE,
    S_TYPE,
    B_TYPE,
    U_TYPE,
    J_TYPE,
    INVALID_TYPE
  } inst_format_e;

  typedef enum {
    WB_ALU,
    WB_IMM,
    WB_PC_IMM,
    WB_RAM,
    WB_JAL,
    WB_JALR
  } wb_sel_e;

  typedef enum logic {
    REG = 1'b0,
    IMM = 1'b1
  } alu_src_e;

  typedef enum logic [1:0] {
    BYTE = 2'b00,
    HALF_WORD = 2'b01,
    WORD = 2'b10
  } ram_size_e;
endpackage
