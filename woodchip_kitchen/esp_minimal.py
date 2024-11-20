import time
from networking import Networking # type: ignore
a = Networking()

from BLE_Minimal import Yell
yeller = Yell()
while True:
    messages = list(a.aen.return_messages())
    print(messages)
    messagetext = messages[0][1]
    if messagetext is not None:
        yelltext = 'k' + messagetext[0]
        print('about to yell {}'.format(yelltext))
        yeller.advertise(yelltext)
    print()
    time.sleep(1)