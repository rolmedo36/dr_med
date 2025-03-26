from escpos.printer import File

p = File("/dev/usb/lp0")
p.text("Hello, Thermal Printer!\n")
p.cut()