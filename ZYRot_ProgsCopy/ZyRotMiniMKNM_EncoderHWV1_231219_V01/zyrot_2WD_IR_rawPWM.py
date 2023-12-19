from machine import Pin,ADC,PWM
import time
from sys import platform
import time
import gc


class rawPWM_2WD():

    def __init__(self):
        self.pwm_freq = 500
        self.pwm_duty_r = 0
        self.pwm_duty_l = 0
        self.pin_lf = 12
        self.pin_lb = 13
        self.pin_rf = 14
        self.pin_rb = 27
        self.pwm_lf = PWM(Pin(self.pin_lf),duty=0,freq=self.pwm_freq)
        self.pwm_lb = PWM(Pin(self.pin_lb),duty=0,freq=self.pwm_freq)
        self.pwm_rf = PWM(Pin(self.pin_rf),duty=0,freq=self.pwm_freq)
        self.pwm_rb = PWM(Pin(self.pin_rb),duty=0,freq=self.pwm_freq)

       
    def move(self, duty_l, duty_r):
        if duty_l < 0:
            self.pwm_lf.duty(0)
            self.pwm_lb.duty(-duty_l)
        else:
            self.pwm_lb.duty(0)
            self.pwm_lf.duty(duty_l)
            
        if duty_r < 0:
            self.pwm_rf.duty(0)
            self.pwm_rb.duty(-duty_r)
        else:
            self.pwm_rb.duty(0)
            self.pwm_rf.duty(duty_r)
            
    def stop(self):
        self.pwm_lb.duty(0)
        self.pwm_rb.duty(0)
        self.pwm_lf.duty(0)
        self.pwm_rf.duty(0)



if __name__ == '__main__':
    zy2wd = rawPWM_2WD()
    for i in range(10):
        print("zyrot_2WD_IR_rawPWM test...", i)
        zy2wd.move(200, 200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(200)
        zy2wd.move(-200, -200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(200)
        zy2wd.move(0, -200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(200)
        zy2wd.move(-200, 0)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(200)
        
        



