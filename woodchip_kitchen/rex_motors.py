from machine import Pin
from time import sleep

# Define the input pins connected to the ULN2003 driver
IN1 = Pin(16, Pin.OUT)
IN2 = Pin(17, Pin.OUT)
IN3 = Pin(18, Pin.OUT)
IN4 = Pin(19, Pin.OUT)

# Step sequence for the 28BYJ-48 motor
step_sequence = [
    [1, 0, 0, 0],  # Step 1
    [1, 1, 0, 0],  # Step 2
    [0, 1, 0, 0],  # Step 3
    [0, 1, 1, 0],  # Step 4
    [0, 0, 1, 0],  # Step 5
    [0, 0, 1, 1],  # Step 6
    [0, 0, 0, 1],  # Step 7
    [1, 0, 0, 1],  # Step 8
]

# Function to set the pins based on the step
def set_pins(step):
    IN1.value(step[0])
    IN2.value(step[1])
    IN3.value(step[2])
    IN4.value(step[3])

# Rotate the stepper motor
def test_motor(delay=0.001, steps=128):
    print("Testing stepper motor...")
    for _ in range(steps):
        for step in step_sequence:
            set_pins(step)
            sleep(delay)
    print("Test complete.")

# Run the test
test_motor()