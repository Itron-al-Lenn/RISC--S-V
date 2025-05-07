from test.util import runner

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def test_reg_file():
    runner('reg_file', ['reg_file.sv'])

@cocotb.test()
async def reg_file_basic(dut):
    
    # Create a clock with 10ns period
    clock = Clock(dut.clock, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Initialize inputs
    dut.write_enable.value = 0
    dut.rd_address.value = 0
    dut.rs1_address.value = 0
    dut.rs2_address.value = 0
    dut.rd_data.value = 0
    
    # Reset - wait a few clock cycles
    for _ in range(2):
        await RisingEdge(dut.clock)
    
    # Test Case 1: Write to register 1 and read it back
    dut.write_enable.value = 1
    dut.rd_address.value = 1
    dut.rd_data.value = 0xABCD1234
    await RisingEdge(dut.clock)
    
    dut.write_enable.value = 0
    dut.rs1_address.value = 1
    await Timer(1, units="ns")  # Small delay for combinational read
    assert int(dut.rs1_data.value) == 0xABCD1234, f"TC1 Failed: rs1_data=0x{int(dut.rs1_data.value):x}, expected=0xABCD1234"
    
    # Test Case 2: Try writing to register 0 (should remain 0)
    dut.write_enable.value = 1
    dut.rd_address.value = 0
    dut.rd_data.value = 0x12345678
    await RisingEdge(dut.clock)
    
    dut.write_enable.value = 0
    dut.rs1_address.value = 0
    await Timer(1, units="ns")
    assert int(dut.rs1_data.value) == 0, f"TC2 Failed: rs1_data=0x{int(dut.rs1_data.value):x}, expected=0x0"
    
    # Test Case 3: Write multiple registers and read using both ports
    dut.write_enable.value = 1
    dut.rd_address.value = 2
    dut.rd_data.value = 0xAAAA5555
    await RisingEdge(dut.clock)
    
    dut.rd_address.value = 3
    dut.rd_data.value = 0x55551111
    await RisingEdge(dut.clock)
    
    dut.write_enable.value = 0
    dut.rs1_address.value = 2
    dut.rs2_address.value = 3
    await Timer(1, units="ns")
    assert int(dut.rs1_data.value) == 0xAAAA5555, f"TC3 Failed rs1: rs1_data=0x{int(dut.rs1_data.value):x}, expected=0xAAAA5555"
    assert int(dut.rs2_data.value) == 0x55551111, f"TC3 Failed rs2: rs2_data=0x{int(dut.rs2_data.value):x}, expected=0x55551111"
    
    # Test Case 4: Test write enable functionality
    dut.write_enable.value = 0  # Disabled
    dut.rd_address.value = 4
    dut.rd_data.value = 0xDEADBEEF
    await RisingEdge(dut.clock)
    
    dut.rs1_address.value = 4
    await Timer(1, units="ns")
    
    # Modified to handle undefined values in register 4
    # If the register hasn't been written to, it might be x (undefined)
    # We'll check if it's not equal to 0xDEADBEEF, which is what we attempted to write
    if dut.rs1_data.value.is_resolvable:
        assert int(dut.rs1_data.value) != 0xDEADBEEF, "TC4 Failed: Write occurred when write_enable=0"
    else:
        # If the value is 'x' (undefined), that's acceptable for an uninitialized register
        dut._log.info("Register 4 has undefined value, which is acceptable for an unwritten register")

@cocotb.test()
async def reg_file_random_access(dut):
    """Test random access patterns in register file"""
    
    for _ in range(50):
        import random

        # Setup clock
        clock = Clock(dut.clock, 10, units="ns")
        cocotb.start_soon(clock.start())
        
        # Initialize
        dut.write_enable.value = 0
        await RisingEdge(dut.clock)
        
        # Test random values to random registers (except x0)
        test_values = {}
        for i in range(10):
            reg = random.randint(1, 31)  # Skip reg 0
            value = random.randint(0, 0xFFFFFFFF)
            test_values[reg] = value
            
            # Write the value
            dut.write_enable.value = 1
            dut.rd_address.value = reg
            dut.rd_data.value = value
            await RisingEdge(dut.clock)
        
        # Disable writes
        dut.write_enable.value = 0
        await RisingEdge(dut.clock)
        
        # Read back and verify all values
        for reg, expected_value in test_values.items():
            dut.rs1_address.value = reg
            await Timer(1, units="ns")
            assert int(dut.rs1_data.value) == expected_value, f"Random test failed: reg[{reg}]=0x{int(dut.rs1_data.value):x}, expected=0x{expected_value:x}"
