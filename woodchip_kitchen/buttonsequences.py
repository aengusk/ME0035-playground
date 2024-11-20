from machine import Pin
import time

class ButtonSequenceManager:
    """Manages a sequence-based button game using GPIO pins."""

    # Define GPIO pins for buttons and LEDs as class-level constants
    BUTTON_CONFIG = {
        1: {"button_pin": "GPIO0", "led_pin": "GPIO4"},
        2: {"button_pin": "GPIO1", "led_pin": "GPIO5"},
        3: {"button_pin": "GPIO2", "led_pin": "GPIO6"},
        4: {"button_pin": "GPIO3", "led_pin": "GPIO7"},
    }
    DEBOUNCE_MS = 400  # Debounce time in milliseconds

    def __init__(self):
        self.buttons = {}  # Map of button IDs to their handlers
        self.current_sequence = []  # The current sequence to follow
        self.current_index = 0  # The index of the current step in the sequence
        self.last_time = 0  # For debouncing
        self.last_pressed = {}  # To track the last time each button was pressed
        self.sequence_complete = True
        
        # Initialize button handlers and their LEDs
        for button_id, config in self.BUTTON_CONFIG.items():
            self.buttons[button_id] = {
                "button": Pin(config["button_pin"], Pin.IN, Pin.PULL_UP),
                "led": Pin(config["led_pin"], Pin.OUT)
            }
            # Attach interrupt handlers
            self.buttons[button_id]["button"].irq(
                trigger=Pin.IRQ_RISING, 
                handler=lambda pin, b_id=button_id: self._button_callback(b_id)
            )

    def new_sequence(self, sequence):
        """
        Set up a new sequence of button presses. Each step in the sequence can
        be a single button ID (e.g., 1) or a tuple of button IDs (e.g., (2, 3)).
        """
        self.sequence_complete = False
        self.current_sequence = sequence
        self.current_index = 0
        self._reset_leds()
        self._activate_current_step()

    def _activate_current_step(self):
        """Activate LEDs for the current step in the sequence."""
        if self.current_index < len(self.current_sequence):
            current_step = self.current_sequence[self.current_index]
            if isinstance(current_step, int):
                # Single button
                self.buttons[current_step]["led"].on()
            elif isinstance(current_step, tuple):
                # Multiple buttons
                for button_id in current_step:
                    self.buttons[button_id]["led"].on()

    def _deactivate_leds(self, button_ids):
        """Deactivate LEDs for given button IDs."""
        if isinstance(button_ids, int):
            # Single button
            self.buttons[button_ids]["led"].off()
        elif isinstance(button_ids, tuple):
            # Multiple buttons
            for button_id in button_ids:
                self.buttons[button_id]["led"].off()

    def _reset_leds(self):
        """Turn off all LEDs."""
        for config in self.BUTTON_CONFIG.values():
            Pin(config["led_pin"], Pin.OUT).off()

    def _button_callback(self, button_id):
        """
        Handle button presses. Verify if the pressed button matches
        the current step in the sequence.
        """
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_time) < self.DEBOUNCE_MS:
            return  # Ignore if within debounce time
        self.last_time = current_time

        if self.current_index >= len(self.current_sequence):
            return  # No sequence currently running

        current_step = self.current_sequence[self.current_index]

        if isinstance(current_step, int) and button_id == current_step:
            # Correct single button press
            print(f"Button {button_id} pressed correctly!")
            self._deactivate_leds(current_step)
            self._advance_sequence()
        elif isinstance(current_step, tuple) and button_id in current_step:
            # Handle multi-button step
            if self._all_buttons_pressed(current_step):
                print(f"Buttons {current_step} pressed correctly!")
                self._deactivate_leds(current_step)
                self._advance_sequence()

    def _all_buttons_pressed(self, button_ids):
        """
        Check if all buttons in a tuple were pressed simultaneously.
        This function checks the current state of all involved buttons.
        """
        return all(self.buttons[button_id]["button"].value() == 0 for button_id in button_ids)

    def _advance_sequence(self):
        """Move to the next step in the sequence or wrap up if done."""
        self.current_index += 1
        if self.current_index < len(self.current_sequence):
            self._activate_current_step()
        else:
            print("Sequence completed!")
            self.sequence_complete = True
