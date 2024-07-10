from escpos.printer import Usb

p = None

def initialize_printer():
    global p
    if p is None:
        p = Usb(0x0483, 0x5743)
        print('printer status:', p)