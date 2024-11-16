from machine import Pin, PWM
import time
import math

from speaker import simpleSpeaker

notes = [262, # Index 0: C4
        294, # Index 1: D
        330, # Index 2: E
        349, # Index 3: F
        392, # Index 4: G
        440, # Index 5: A
        494, # Index 6: B
        523] # Index 7: C5


# ---------- MAIN CODE ----------
speaker = simpleSpeaker(PWM('GPIO6', Pin.OUT))
speaker.playNote(262)

redButton = Pin('GPIO17', Pin.IN, Pin.PULL_UP)
blueButton = Pin('GPIO16', Pin.IN, Pin.PULL_UP)
purpButton = Pin('GPIO18', Pin.IN, Pin.PULL_UP)

while True:
    print("in loop, red button value: "+str(redButton.value()))
    if not redButton.value():
        print("Red button is down!")
    if not blueButton.value():
        print("Blue button is down!")
    time.sleep(0.1)

