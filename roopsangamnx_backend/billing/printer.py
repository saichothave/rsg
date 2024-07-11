from escpos.printer import Usb

p = None

def initialize_printer():
    global p
    if p is None:
        try:
            p = Usb(0x0483, 0x5743)
            p.buzzer(2, 1)
            print('printer status:', p.buzzer)
            return p
        except Exception as e:
            print('exception-', e)