from now import Now # type: ignore
from BLE_Minimal import Yell

yeller = Yell()

def my_callback(msg, mac):
    print(mac, msg)
    n.publish(msg, mac)

n = Now(my_callback)
n.connect()
print(n.wifi.config('mac'))

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()