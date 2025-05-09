typedef enum logic [6:0] {
} alu_funct7_e;

typedef enum logic [2:0] {
  // Will be added when implementing the operations
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
