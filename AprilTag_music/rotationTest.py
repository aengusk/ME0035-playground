from machine import Pin, PWM
import time
import sensor
import math

from speaker import Speaker


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

notes = [262, # Index 0: C
         277, # Index 1: C#
         294, # Index 2: D
         311, # Index 3: D#
         330, # Index 4: E
         349, # Index 5: F
         370, # Index 6: F#
         392, # Index 7: G
         415, # Index 8: G#
         440, # Index 9: A
         466, # Index 10: A#
         494] # Index 11: B


# ---------- MAIN CODE ----------
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

