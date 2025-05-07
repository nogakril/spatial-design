try:
    import spidev
except ImportError:
    class MockSpiDev:
        def open(self, bus, device): pass

        def xfer2(self, data): return [0, 2, 128]  # simulate midrange ADC value

        def close(self): pass

        max_speed_hz = 1350000


    spidev = type('spidev', (), {'SpiDev': MockSpiDev})


class JoystickReader:
    def __init__(self, channel_x=0, channel_y=1):
        self.channel_x = channel_x
        self.channel_y = channel_y

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, CS 0
        self.spi.max_speed_hz = 1350000

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def get_direction(self, threshold=200):
        x = self.read_channel(self.channel_x)  # center ~512
        y = self.read_channel(self.channel_y)
        print(f"Joystick channel inputs X: {x}, Y: {y}")

        if x < 512 - threshold:
            return 'LEFT'
        elif x > 512 + threshold:
            return 'RIGHT'
        elif y < 512 - threshold:
            return 'UP'
        elif y > 512 + threshold:
            return 'DOWN'
        else:
            return 'RIGHT'  # Centered
