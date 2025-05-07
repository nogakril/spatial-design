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
UP_LED = 5
DOWN_LED = 6
LEFT_LED = 13
RIGHT_LED = 19


class LEDController:
    def __init__(self):
        self.led_pins = {
            'UP': UP_LED,
            'DOWN': DOWN_LED,
            'LEFT': LEFT_LED,
            'RIGHT': RIGHT_LED
        }

        for pin in self.led_pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def turn_on_led(self, direction):
        pin = self.led_pins.get(direction)
        if pin is not None:
            GPIO.output(pin, GPIO.HIGH)

    def turn_off_led(self, direction):
        pin = self.led_pins.get(direction)
        if pin is not None:
            GPIO.output(pin, GPIO.LOW)

    def turn_off_all(self):
        for pin in self.led_pins.values():
            GPIO.output(pin, GPIO.LOW)
