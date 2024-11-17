# Peripheral - By: annehu - Sun Nov 17 2024
from BLE_CEEO import Yell
import uasyncio as asyncio
import time

class Peripheral():
    def __init__(self, name):
        self.p = Yell(name, interval_us=100000, verbose = True)
        self.nextMessage = None
        self.queue = False

    # To connect the peripheral to central
    def connect(self):
        while not self.p.is_connected:
            print("---------Still not connected--------")
            try:
                self.p.connect_up()
                print('P connected')
            except Exception as e:
                print(e + " --- not connecting...")
            time.sleep(0.1)

    # To add a note to the send queue
    def send(self, note):
        print("In peripheral.send() function")
        self.nextMessage = note
        self.queue = True


    # To continuously send messages
    async def messageHandler(self):
        while True:
            if self.queue:
                try:
                    print("Trying to send message")
                    self.p.send(self.nextMessage)
                    self.queue = False
                except Exception as e:
                    print("couldn't send message")
                    if not self.p.is_connected:
                        print("Reconnecting")
                        self.p.self.connect_up()
            await asyncio.sleep(0.01)

# async def tester(p):
#     while True:
#         p.send("testing testing testing")
#         print("sent a thing")
#         await asyncio.sleep(0.01)

# test = Peripheral('Camera')
# test.connect()
# loop = asyncio.get_event_loop()
# loop.create_task(test.messageHandler())
# loop.create_task(tester(test))
# loop.run_forever()






