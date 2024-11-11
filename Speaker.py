# speaker.py - By: annehu - Sat Nov 9 2024
from machine import Pin, PWM
import time

class Speaker:
    def __init__(self, pwm):
        self.pin = PWM(pwm)
        self.pin.freq(262)
        self.pin.duty_u16(0)

    def playNote(self,note):
        print("playing note!")
        self.pin.freq(note)
        self.pin.duty_u16(50000)
        time.sleep(1)
        self.pin.duty_u16(0)



# Test code
test = Speaker(Pin('P4',Pin.OUT))
test.playNote(50)

led = PWM(Pin('P7', Pin.OUT))

led.freq(2)
for i in range(0,63553):
    led.duty_u16(i)
    time.sleep(0.01)
