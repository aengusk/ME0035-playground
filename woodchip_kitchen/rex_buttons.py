from machine import Pin
import time

class ButtonHandler:
    def __init__(self, pin_name, button_id, led_pin, sequence_controller=None, debounce_ms=400):
        self.pin = Pin(pin_name, Pin.IN, Pin.PULL_UP)  # Button pin
        self.led = Pin(led_pin, Pin.OUT)              # LED pin
        self.button_id = button_id                   # Unique button ID
        self.sequence_controller = sequence_controller  # Sequence manager (can be None initially)
        self.last_time = 0                           # For debouncing
        self.debounce_ms = debounce_ms
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=self.callback)

    def activate_led(self):
        """Turn the LED on."""
        self.led.on()

    def deactivate_led(self):
        """Turn the LED off."""
        self.led.off()

    def callback(self, p):
        """Handle button press."""
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_time) > self.debounce_ms:
            if self.sequence_controller and self.sequence_controller.is_correct_button(self.button_id):
                print(f'Button {self.button_id} pressed correctly!')
                self.deactivate_led()  # Turn off the LED
                self.sequence_controller.advance_sequence()  # Move to the next button
            else:
                print(f'Button {self.button_id} pressed out of sequence.')
            self.last_time = current_time


class SequenceController:
    def __init__(self, buttons, sequence):
        self.buttons = buttons
        self.sequence = sequence  # User-defined sequence of button IDs
        self.current_index = 0    # Start with the first button in the sequence

    def activate_current_button(self):
        """Activate the LED for the current button in the sequence."""
        if self.buttons:
            current_button = self.get_button_by_id(self.sequence[self.current_index])
            current_button.activate_led()

    def is_correct_button(self, button_id):
        """Check if the pressed button matches the active button."""
        return self.sequence[self.current_index] == button_id

    def advance_sequence(self):
        """Move to the next button in the sequence."""
        if self.buttons:
            self.current_index = (self.current_index + 1) % len(self.sequence)  # Wrap around
            self.activate_current_button()

    def get_button_by_id(self, button_id):
        """Find the button handler by its ID."""
        for button in self.buttons:
            if button.button_id == button_id:
                return button
        raise ValueError(f"Button with ID {button_id} not found")


# Define button pins, unique IDs, and LED pins
button_definitions = [
    {"pin": "GPIO0", "id": 1, "led_pin": "GPIO5"},
    {"pin": "GPIO1", "id": 2, "led_pin": "GPIO6"},
    {"pin": "GPIO3", "id": 3, "led_pin": "GPIO7"},
    {"pin": "GPIO4", "id": 4, "led_pin": "GPIO8"},
]

# Create button handlers without sequence controller initially
button_handlers = [ButtonHandler(btn["pin"], btn["id"], btn["led_pin"]) for btn in button_definitions]

# Define a custom sequence of button IDs
custom_sequence = [3, 1, 4, 2]  # Example: Button 3 → Button 1 → Button 4 → Button 2

# Create the sequence controller with the custom sequence and assign it to button handlers
sequence_controller = SequenceController(button_handlers, custom_sequence)
for handler in button_handlers:
    handler.sequence_controller = sequence_controller

# Activate the first button in the custom sequence
sequence_controller.activate_current_button()
