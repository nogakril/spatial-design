import serial
import threading


class ArduinoInputController:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.last_button = None
        self.last_joystick = None
        self.running = True

        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def _listen(self):
        while self.running:
            line = self.ser.readline().decode().strip()
            if line in ['SAVE', 'CONNECT']:
                self.last_button = line
                print(f"Button: {line}")
            elif line in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                self.last_joystick = line
                print(f"Joystick: {line}")

    def get_input(self):
        # Return current state, then reset
        input_state = {
            'button': self.last_button,
            'joystick': self.last_joystick
        }
        self.last_button = None
        self.last_joystick = None
        return input_state

    def cleanup(self):
        self.running = False
        self.ser.close()
