# Open a file in binary mode to write raw ESC/POS commands
with open("print_receipt.bin", "wb") as f:
    f.write(b'\x1B\x40')  # Initialize printer
    f.write(b'\x1B\x21\x10')  # Double height text
    f.write(b'Hello, ESC/POS Printer!\n')  # Print text
    f.write(b'\x1B\x64\x02')  # Feed 2 lines
    f.write(b'\x1D\x56\x00')  # Cut paper

print("ESC/POS file created: print_receipt.bin")