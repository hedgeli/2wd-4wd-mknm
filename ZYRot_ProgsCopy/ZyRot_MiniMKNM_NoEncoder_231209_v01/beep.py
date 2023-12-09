
from machine import Pin, PWM
import time


def beep_test():
    
    p27 = Pin(27, Pin.OUT)
    p27.off()
    
    p14 = Pin(14, Pin.OUT)
    p14.off()
    
    p12 = Pin(12, Pin.OUT)
    p12.off()
    
    p13 = Pin(13, Pin.OUT)
    p13.off()
    

    beep = PWM(Pin(0),freq=1000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=2000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=3000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=4000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=5000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=6000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=7000)
    beep.duty(512)
    time.sleep(1)
    beep = PWM(Pin(0),freq=8000)
    beep.duty(512)
    time.sleep(1)
    beep.duty(0)


if __name__ == '__main__':
    beep_test()










