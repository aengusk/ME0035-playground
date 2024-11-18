# THIS MODULE CURRENTLY DOES NOT WORK
# This module is a low-versatility UART class that will be run on both the Pico and the ESP 
# to facilitate serial communication

# Python
import sys
# MicroPython
from machine import Pin, UART   # type: ignore (suppresses Pylance lint warning)


class KitchenUART():
    def __init__(self):
        if sys.platform == 'rp2': 
            # if the code is running on a Raspberry Pi Pico
            # tx=16, rx=17
            self.uart = UART(0, baudrate=115200, tx=16, rx=17)
        elif sys.platform == 'esp32': 
            # if the code is running on an ESP on a Dahal board
            # tx is D6, rx is D7 according to pinout https://wiki.seeedstudio.com/xiao_esp32s3_pin_multiplexing/
            # tx is SDA, rx is SCL
            # Smart Motor code uses i2c = SoftI2C(scl = Pin(7), sda = Pin(6)) # ESP
            self.uart = UART(0, baudrate=115200, tx=6, rx=7) # pico
        else:
            raise RuntimeError('unrecognized board: {}'.format(sys.platform))
        
    def send(self, message):
        message = message.encode()
        self.uart.write(message)

    def receive(self):
        if self.uart.any():
            message_received = self.uart.read()
            if isinstance(message_received, bytes):
                return message_received.decode()#.strip()
            else:
                print('message_received was of type {}'.format(type(message_received)))
                return None
        print('uart.any() was False')
        return None

uart = KitchenUART()
print('successfully established UART')

while True:
    message_to_send = input('message to send: ')
    uart.send(message_to_send)
    print(uart.receive())