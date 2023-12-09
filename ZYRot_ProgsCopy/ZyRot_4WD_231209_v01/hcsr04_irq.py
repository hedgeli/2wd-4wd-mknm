from machine import Pin, time_pulse_us
from utime import sleep_us
import time

__version__ = '0.0.1'
__author__ = 'ZyRot'

class Hcsr04Irq:
    # 17cm/ms max meament distence 150cm(9ms)
    def __init__(self,trigger_pin, echo_pin, timeout_us=9000):
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
        self.echo.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,handler=self.irq_handle)  #IRQ_RISING IRQ_FALLING
        
        self.trig_us_stamp = 0
        self.pulse_us = 0
        self.distance_mm = 0
        self.mea_ms_stamp = 0
        self.echo_timeout_us = timeout_us
        self.echo_cnt = 0
        
    def trig_start(self):
        self.trigger.value(0) # Stabilize the sensor
        sleep_us(1)
        self.trigger.value(1)
        # Send a 10us pulse.
        sleep_us(10)
        self.trigger.value(0)
        self.trig_us_stamp = time.ticks_us()
        
    def get_dist_mm(self):
        return self.distance_mm
        
    def irq_handle(self,pin):
        edge = pin.value()
        if edge == 1:
            self.trig_us_stamp = time.ticks_us()
        else:
            self.pulse_us = time.ticks_us() - self.trig_us_stamp
            self.mea_ms_stamp = time.ticks_ms()
            self.echo_cnt+=1
            # 0.34320 mm/us that is 1mm each 2.91us
            # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
            if self.pulse_us <= self.echo_timeout_us:
                self.distance_mm = self.pulse_us * 100 // 582
            else:
                self.distance_mm = 0
                self.pulse_us = 0
        
if __name__ == '__main__':
    print('Start hcsr04irq test...')
    sr04 = Hcsr04Irq(trigger_pin = 2, echo_pin=4)
    for i in range(200):
        sr04.trig_start()
        time.sleep_ms(200)
        distance = sr04.get_dist_mm()
        print('Dis_mm:',distance)

    print('sr04irq test over.')
