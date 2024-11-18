from machine import Pin, PWM
import asyncio
from BLE_CEEO import Listen
from networking import Networking

class AprilTagMusicController:

    RESET_PIN = 17 # D7
    ADD_PIN   = 19 # D8
    PLAY_PIN  = 20 # D9
    PWM_PIN   = 18 # D10
    BLUETOOTH_DEVICE_NAME = 'Camera' # OpenMV Peripheral name

    # All possible note frequencies
    Notes = [262, # Index 0: C4
             294, # Index 1: D
             330, # Index 2: E
             349, # Index 3: F
             392, # Index 4: G
             440, # Index 5: A
             494, # Index 6: B
             523, # Index 7: C5
            ]

    def __init__(self):

        self.resetButton = Pin(self.RESET_PIN, Pin.IN, Pin.PULL_UP)
        self.addButton   = Pin(self.ADD_PIN, Pin.IN, Pin.PULL_UP)
        self.playButton  = Pin(self.PLAY_PIN, Pin.IN, Pin.PULL_UP)

        self.prev_reset_state = False
        self.prev_add_state   = False
        self.prev_play_state  = False

        self.speaker = PWM(self.PWM_PIN, Pin.OUT)
        self.speaker.duty_u16(int(0))
        self.activeNoteIndex = 0 # Received over bluetooth from OpenMV cam
        self.activeFoodIndex = None
        self.NotesQueue = [] # Contains the current notes

        self.networking = Networking()

    async def checkButtons(self):
        while True:
            current_reset_state = self.resetButton.value()
            if self.prev_reset_state and not current_reset_state:
                print('Reset button pressed!')
                await self.resetNotes()

            current_add_state = self.addButton.value()
            if self.prev_add_state and not current_add_state:
                print('Add button pressed!')
                await self.addNote()

            current_play_state = self.playButton.value()
            if self.prev_play_state and not current_play_state:
                print('Play button pressed!')
                await self.playNotes()

            # Update previous button states
            self.prev_reset_state = current_reset_state
            self.prev_add_state = current_add_state
            self.prev_play_state = current_play_state

            await asyncio.sleep(0.1) # Small delay to debounce
    
    async def addNote(self):
        print("Added: ", self.Notes[self.activeNoteIndex])
        self.NotesQueue.append(self.Notes[self.activeNoteIndex])
    
    async def resetNotes(self):
        self.NotesQueue.clear()

    async def playNotes(self):
        for Note in self.NotesQueue:
            print(Note)
            self.speaker.duty_u16(int(65535/8))
            self.speaker.freq(Note)
            await asyncio.sleep(0.5) # Play note for half a second
            self.speaker.duty_u16(int(0))
            await asyncio.sleep(0.5) # Wait for half a second
    
    async def getActiveNoteBluetooth(self):
        listen_device = Listen(name=self.BLUETOOTH_DEVICE_NAME, verbose=True)
        while True:
            try:
                if listen_device.connect_up(timeout=5000):
                    print(f"Connected to {self.BLUETOOTH_DEVICE_NAME}")
                    while True:
                        if listen_device.is_any:
                            # Read and update self.activeNoteIndex with the received data
                            received_message = listen_device.read()
                            print(f"Received message: {received_message}")
                            try:
                                indexes = received_message.split(',')
                                if len(indexes) >= 2:
                                    self.activeNoteIndex = int(indexes[0].strip())
                                    print(f"Updated activeNoteIndex: {self.activeNoteIndex}")

                                    if self.activeFoodIndex != indexes[1]:
                                        self.activeFoodIndex = indexes[1]
                                        print(f"Updated activeFoodIndex: {self.activeFoodIndex}")
                                        await self.sendFoodIndex()

                                else:
                                    print("Received message does not contain a valid pair of numbers")
                            except ValueError:
                                print(f"Invalid data received: {received_message}")
                            
                        await asyncio.sleep(0) # Must be 0 so that received message buffer is always immediately
                else:
                    print(f"Failed to connect to {self.BLUETOOTH_DEVICE_NAME}")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")
                # listen_device.disconnect()
                print("Attempting to reconnect...")
                await asyncio.sleep(1)
    
    async def sendFoodIndex(self):
        recipient_mac = b'\xff\xff\xff\xff\xff\xff'
        self.networking.aen.send(recipient_mac, self.activeFoodIndex)
     
    async def main(self):
        await asyncio.gather(
            self.getActiveNoteBluetooth(),
            self.checkButtons()
        )

# Create instance of controller class and run code
controller = AprilTagMusicController()
asyncio.run(controller.main())