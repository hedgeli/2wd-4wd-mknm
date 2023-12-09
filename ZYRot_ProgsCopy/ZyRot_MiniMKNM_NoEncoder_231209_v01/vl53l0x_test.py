# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time
from machine import SoftI2C, Pin
import vl53l0x 


if __name__ == '__main__':
    # Initialize I2C bus and sensor.
    #i2c = machine.I2C(1, freq = 400000)
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
    vl53 = vl53l0x.VL53L0X(i2c)

    # Optionally adjust the measurement timing budget to change speed and accuracy.
    # See the example here for more details:
    #   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
    # For example a higher speed but less accurate timing budget of 20ms:
    # vl53.measurement_timing_budget = 20000
    # Or a slower but more accurate timing budget of 200ms:
    # vl53.measurement_timing_budget = 200000
    # The default timing budget is 33ms, a good compromise of speed and accuracy.

    # Main loop will read the range and print it every second.
    # while True:
    for i in range(500):
        print("Range: {0} mm".format(vl53.range))
        time.sleep(0.1)

