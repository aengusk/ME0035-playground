# Python
import time, machine                # type: ignore (suppresses Pylance lint warning)
# MicroPython
from machine import Pin, PWM, UART  # type: ignore
# custom
from BLE_CEEO import Yell, Listen   # type: ignore
from espnow_bluetooth_relay import check_bluetooth

class Woodchip_Kitchen:
    
    def __init__(self):
        
        # Need to add stuff for on/off switch, apriltag separation, arrow stepper motor setup, etc.
        
        # Button setup
        self.btn1 = Pin('GPIO', Pin.IN, Pin.PULL_UP) # pull up resistor; other btn rail is connected to ground, so btn.value becomes 0 when pressed
        self.btn2 = Pin('GPIO', Pin.IN, Pin.PULL_UP)
        self.btn3 = Pin('GPIO', Pin.IN, Pin.PULL_UP)
        self.btn4 = Pin('GPIO', Pin.IN, Pin.PULL_UP)
        
        # Button LED setup
        self.led1 = Pin('GPIO', Pin.OUT) 
        self.led2 = Pin('GPIO', Pin.OUT)
        self.led3 = Pin('GPIO', Pin.OUT)
        self.led4 = Pin('GPIO', Pin.OUT)
        
        # More LED setup
        # for status leds on station?
        
        # Stepper motor setup
        self.in1 = Pin(27, Pin.OUT)
        self.in2 = Pin(26, Pin.OUT)
        self.in3 = Pin(6, Pin.OUT)
        self.in4 = Pin(7, Pin.OUT)
        
        # Full-step sequence (forward)
        self.full_step_sequence = [
            [1, 0, 1, 0],  # Step 1
            [0, 1, 1, 0],  # Step 2
            [0, 1, 0, 1],  # Step 3
            [1, 0, 0, 1],  # Step 4
        ]

        # Full-step sequence (reverse)
        self.reverse_full_step_sequence = [
            [1, 0, 0, 1],  # Step 4
            [0, 1, 0, 1],  # Step 3
            [0, 1, 1, 0],  # Step 2
            [1, 0, 1, 0],  # Step 1
        ]
        
        # Food option setup
        self.food_functions = {
            "burger": self.burger,
            "smoothie": self.smoothie,
            "ramen": self.ramen
        }
        self.food_steps = {
            "burger": 10, # placeholder values
            "smoothie": 20,
            "ramen": 30
        }
        
        # # UART connection
        # self.uart_pico = UART(1, baudrate=9600, tx=17, rx=16)  # adjust TX/RX pins as needed
        
        # Bluetooth connection
        # if we decide to do pico to pico communication
        
        # Run game
        #main()
        
        
    # Function to set the stepper motor states
    def set_step(self, step):
        self.in1.value(step[0])
        self.in2.value(step[1])
        self.in3.value(step[2])
        self.in4.value(step[3])

    # Function to rotate the stepper motors (pass the step sequence)
    def rotate_motor(self, delay, steps, step_sequence):
        for _ in range(steps):
            for step in step_sequence:
                self.set_step(step)
                time.sleep(delay)
                
    # Functions for each food sequence
    # These will include all the logic that involves communicating with the other station
    def burger(self):
        # button logic
        raise NotImplementedError
        
    def smoothie(self):
        # button logic
        raise NotImplementedError
        
    def ramen(self):
        # button logic
        raise NotImplementedError
        
    # Main code
    def main(self):
        while True:
            message = check_bluetooth()
            if message:  # check if data is available to read
                if message in self.food_functions: # check if the received message matches one of the commands
                    #print(f"New Order: {message}")
                    self.rotate_motor(0.01, self.food_steps[message], self.full_step_sequence) # rotate motors to correct pictures
                    self.food_functions[message]()  # call the corresponding function
                    self.rotate_motor(0.01, self.food_steps[message], self.reverse_full_step_sequence) # rotate motors back to starting pictures when order is complete
                else:
                    print("Unknown command received.")
            
            time.sleep(0.1)



if __name__ == '__main__':
    kitchen = Woodchip_Kitchen()
    kitchen.main()