import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115:

    def __init__(self, poll_delay=0.01):
        # create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # create ADC object
        ads = ADS.ADS1015(i2c)

        POWER_CHANNEL_MOTOR = ADS.P3  # A3 on board
        POWER_CHANNEL_PI = ADS.P2  # A2 on board

        self.chan_motor = AnalogIn(ads, POWER_CHANNEL_MOTOR)
        self.chan_pi = AnalogIn(ads, POWER_CHANNEL_PI)

        self.poll_delay = poll_delay
        self.on = True
        self.vm = 0
        self.vp = 0

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def poll(self):
        self.vm = self.chan_motor.voltage
        self.vp = self.chan_pi.voltage

    def run_threaded(self):
        return self.vm, self.vp

    def run(self):
        self.poll()
        return self.vm, self.vp

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    iter = 0
    p = ADS1115()
    while iter < 100:
        data1, data2 = p.run()
        print(data1, " ", data2)
        time.sleep(0.01)
        iter += 1