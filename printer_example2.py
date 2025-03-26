import usb.core
import usb.util

devices = usb.core.find(find_all=True)
for dev in devices:
    print(f"Device: {hex(dev.idVendor)}:{hex(dev.idProduct)}")