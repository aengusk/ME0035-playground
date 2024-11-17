# Peripheral - By: annehu - Sun Nov 17 2024
from BLE_CEEO import Yell
import uasyncio as asyncio

class Peripheral():
    def _init_(self, name):
        self.p = Yell(name, interval_us=100000, verbose = True)
        self.nextMessage
        self.toSend = False

    # To connect the peripheral to central
    async def connect(self):
        while not self.p.is_connected:
            try:
                self.p.connect_up()
                print('P connected')
            except Exception as e:
                print(e + " --- not connecting...")
            await asyncio.sleep(0.1)

    # To add a note to the send queue
    async def send(self, note):
        self.nextMessage = note
        self.toSend = True

    # To continuously send messages
    async def messageHandler(self):
        while True:
            if self.toSend:
                try:
                    self.p.sendMessage(self.nextMessage)
                    self.toSend = False
                except Exception as e:
                    print("couldn't send message, reconnecting")
                    self.connect()
            await asyncio.sleep(0.01)



