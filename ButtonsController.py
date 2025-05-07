class ButtonsController:
    def __init__(self):
        self.joystick_state = ''
        self.button_state = 'SAVE'

    def get_joystick_state(self):
        return self.joystick_state

    def get_button_state(self):
        return self.button_state

    def get_input(self):
        """Return the buttons state"""
        return {
            'joystick': self.get_joystick_state(),
            'button': self.get_button_state()
        }
