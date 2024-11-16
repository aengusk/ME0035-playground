# simpleRotation.py
# Reads April Tag ID and orientation, sends info over BLE to ESP32 for processing
# By: Anne Hu, 11/16/24

import time
import sensor
import math
from BLE_CEEO import Yell

# --------- CAMERA SET UP -----------
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # changing to QVGA (320x240) from QQVGA, makes it slower
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# --------- HELPER FUNCTIONS AND DEFINITIONS ----------
def degrees(radians):
    return (180 * radians) / math.pi

last_tag_seen = 0
no_tag_timeout = 1  # time in seconds before car stops after not detecting apriltag


f_x = (2.8 / 3.984) * 160  # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120  # find_apriltags defaults to this if not set
c_x = 160 * 0.5  # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5  # find_apriltags defaults to this if not set (the image.h * 0.5)


# ------------- BLE CODE ---------------

# to connect the camera peripheral to the ESP central
def connectBLE(p):
    try:
        if p.connect_up():
            print('P connected')
            time.sleep(2)
            p.send("test")
            if p.is_any:
                print(p.read())
            if not p.is_connected:
                print('lost connection')
            time.sleep(1)
    except Exception as e:
        print("except 1")
        print(e)
    finally:
        p.disconnect()
        print('closing up')

# to send messages over BLE
def sendMessage(p, message):
    while not p.is_connected:
        try:
            connectBLE(p)
        except Exception as e:
            print("trying to connect before sending message... "+e)
    p.send(message)


p = Yell('camera', interval_us=100000, verbose = True)
connectBLE(p)

# ---------------- MAIN CODE ----------------

while True:
    clock.tick()
    img = sensor.snapshot()
    tags_we_see = img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y)

    if tags_we_see:
        for tag in tags_we_see:  # defaults to TAG36H11
            img.draw_rectangle(tag.rect, color=(255, 0, 0))
            img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))
            angle = degrees(tag.z_rotation)
            print(angle)

            # TODO: Will need to revisit how to deal with out of bounds angles
            if angle > 270:
                angle = 270

            note = int(angle/34) -1
            print("index: "+str(note))
