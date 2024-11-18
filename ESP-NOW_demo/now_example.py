import time
from now import Now # type: ignore (suppresses Pylance lint warning)


n = Now()
n.connect()
print(n.wifi.config('mac'))

try:
    while True:
        message = input('message to send to richard: ')
        n.publish(message.encode())
        print('just published {}'.format(message))
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted! Cleaning up...")

finally:
    # Ensure interfaces are deactivated on exit
    n.close()