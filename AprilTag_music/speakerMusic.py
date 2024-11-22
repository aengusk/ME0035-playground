from machine import Pin, PWM
from time import sleep

# Define the notes (frequencies in Hz)
Notes = [262, # Index 0: C4
         294, # Index 1: D
         330, # Index 2: E
         349, # Index 3: F
         392, # Index 4: G
         440, # Index 5: A
         494, # Index 6: B
         523  # Index 7: C5
        ]

# Define pins
shutdown_pin = Pin(18, Pin.OUT)  # Connected to SD pin of PAM8302A
audio_pin = Pin(20, Pin.OUT)     # Connected to IN+ of PAM8302A

# Enable the amplifier
shutdown_pin.value(1)

# Set up PWM on the audio pin
pwm = PWM(audio_pin)

# Function to play a single note
def play_note(frequency, duration):
    pwm.freq(frequency)  # Set frequency
    pwm.duty(512)        # Set duty cycle (50% volume)
    sleep(duration)      # Play note for the specified duration
    pwm.duty(0)          # Turn off sound

# Play through all the notes
for note in Notes:
    play_note(note, 0.5)  # Play each note for 0.5 seconds

# Clean up
pwm.deinit()
