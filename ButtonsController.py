# Refactor later
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    # Fake GPIO for development/testing
    class MockGPIO:
        BCM = BOARD = IN = OUT = HIGH = LOW = PUD_UP = FALLING = None
        def setmode(self, *args): pass
        def setup(self, *args, **kwargs): pass
        def output(self, *args): pass
        def input(self, *args): return 0
        def add_event_detect(self, *args, **kwargs): pass
        def remove_event_detect(self, *args): pass
        def cleanup(self): pass

    GPIO = MockGPIO()
from JoystickReader import JoystickReader

# Joystick directions: UP, DOWN, LEFT, RIGHT
# Button state: SAVE, CONNECT

CONNECT_GPIO = 17
SAVE_GPIO = 27

class ButtonsController:
    def __init__(self):
        self.joystick_reader = JoystickReader()
        self.button_state = None

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CONNECT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SAVE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(CONNECT_GPIO, GPIO.FALLING, callback=self.connect_callback, bouncetime=200)
        GPIO.add_event_detect(SAVE_GPIO, GPIO.FALLING, callback=self.save_callback, bouncetime=200)

    def connect_callback(self, channel):
        self.button_state = "CONNECT"
        print("Connect button pressed")

    def save_callback(self, channel):
        self.button_state = "SAVE"
        print("Save button pressed")

    def get_joystick_state(self):
        direction = self.joystick_reader.get_direction()
        print(f"Joystick direction: {direction}")
        return direction

    def get_button_state(self):
        return self.button_state

    def get_input(self):
        """Return the buttons state"""
        return {
            'joystick': self.get_joystick_state(),
            'button': self.get_button_state()
        }

    def cleanup(self):
        GPIO.cleanup()
