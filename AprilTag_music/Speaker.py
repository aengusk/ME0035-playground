# speaker.py - By: annehu - Sat Nov 9 2024
from machine import Pin, PWM
import uasyncio as asyncio
import time

class Speaker():

    def __init__(self, pwm):
        self.pin = pwm
        self.currNote = 200
        #self.pin.freq(262)
        #self.pin.duty_u16(0)

    def setNote(self, note):
        self.currNote  = note

    async def playNote(self):
        print("playing note!")
        self.pin.freq(self.currNote)
        self.pin.duty_u16(int(65535/8))
        await asyncio.sleep(0.5)
        self.pin.duty_u16(0)

    async def playNote(self, note):
        print("playing note!")
        self.pin.freq(note)
        self.pin.duty_u16(int(65535/8))
        await asyncio.sleep(0.5)


    async def noteHandler(self):
        while True:
            self.playNote()
            await asyncio.sleep(0.01)

# ------ simpleSpeaker: Base code that doens't use async -------
class simpleSpeaker:
    def __init__(self, pwm):
        self.pin = pwm

    def playNote(self,note):
        print("playing note!")
        self.pin.freq(note)
        self.pin.duty_u16(int(65535/8))
        time.sleep(0.1)


# Test code
# test = Speaker(PWM(Pin('P0', Pin.OUT)))
# test.playNote(200)



# test = PWM(Pin('P0', Pin.OUT))
# print("starting")
# test.freq(200)
# test.duty_u16(int(65535/2))
# time.sleep(2)
