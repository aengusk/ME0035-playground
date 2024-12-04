import time
from now import Now # type: ignore
from BLE_Minimal import Yell # type: ignore

yeller = Yell()

def my_callback(msg, mac):
    if isinstance(mac, str):
        if mac == 'spillover':
            print('spillover')
    print(mac)
    msg = msg.decode()
    print(msg)

    if msg == '0':
        print('0, burger')
        yelltext = 'k' + msg
        print('about to yell {}'.format(yelltext))
        yeller.advertise(yelltext)
    elif msg == '1':
        print('1, smoothie')
        yelltext = 'k' + msg
        print('about to yell {}'.format(yelltext))
        yeller.advertise(yelltext)
    elif msg == '2':
        print('2, ramen')
        yelltext = 'k' + msg
        print('about to yell {}'.format(yelltext))
        yeller.advertise(yelltext)
    else:
        print('msg received was not interpreted: {}'.format(msg))




n = Now(my_callback)
n.connect()
print(n.wifi.config('mac'))

try:
    while True:
        for _ in range(10):
            time.sleep(1)
        my_callback('0'.encode(), 'spillover')

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()