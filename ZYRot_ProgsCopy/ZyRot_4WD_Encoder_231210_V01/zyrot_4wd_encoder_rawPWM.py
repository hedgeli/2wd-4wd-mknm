from machine import Pin,ADC,PWM
import time
from sys import platform
import time
import gc


class rawPWM_4WD_encoder():

    def __init__(self):
        self.pwm_freq = 500
        self.pwm_duty_r = 0
        self.pwm_duty_l = 0
        self.pin_lff = 12   # 左前轮前进
        self.pin_lfb = 13   # 左前轮后退
        self.pin_rbf = 5   # 左后轮前进
        self.pin_rbb = 18   # 左后轮后退
        
        self.pin_rfb = 27
        self.pin_rff = 14
        self.pin_lbb = 19
        self.pin_lbf = 21
        
        Pin(27, Pin.OUT, value=0)
        Pin(14, Pin.OUT, value=0)
        Pin(12, Pin.OUT, value=0)
        Pin(13, Pin.OUT, value=0)
        
        Pin(21, Pin.OUT, value=0)
        Pin(19, Pin.OUT, value=0)
        Pin(18, Pin.OUT, value=0)
        Pin(5, Pin.OUT, value=0)
    
        time.sleep_ms(100)
        
        
        self.pwm_lff = PWM(Pin(self.pin_lff),duty=0,freq=self.pwm_freq)
        self.pwm_lfb = PWM(Pin(self.pin_lfb),duty=0,freq=self.pwm_freq)
        self.pwm_rff = PWM(Pin(self.pin_rff),duty=0,freq=self.pwm_freq)
        self.pwm_rfb = PWM(Pin(self.pin_rfb),duty=0,freq=self.pwm_freq)
        
        self.pwm_lbf = PWM(Pin(self.pin_lbf),duty=0,freq=self.pwm_freq)
        self.pwm_lbb = PWM(Pin(self.pin_lbb),duty=0,freq=self.pwm_freq)
        self.pwm_rbf = PWM(Pin(self.pin_rbf),duty=0,freq=self.pwm_freq)
        self.pwm_rbb = PWM(Pin(self.pin_rbb),duty=0,freq=self.pwm_freq)

       
    def move_yxw_duty(self, vx=0, vy=0, vw=0):
        if vx > 0:
            self.pwm_lff.duty(0)
            self.pwm_lfb.duty(vx)
            self.pwm_lbf.duty(vx)
            self.pwm_lbb.duty(0)
            
            self.pwm_rff.duty(vx)
            self.pwm_rfb.duty(0)
            self.pwm_rbf.duty(0)
            self.pwm_rbb.duty(vx)
        elif vx < 0:
            self.pwm_lff.duty(-vx)
            self.pwm_lfb.duty(0)
            self.pwm_lbf.duty(0)
            self.pwm_lbb.duty(-vx)
            
            self.pwm_rff.duty(0)
            self.pwm_rfb.duty(-vx)
            self.pwm_rbf.duty(-vx)
            self.pwm_rbb.duty(0)
        else:
            self.stop()
        
        
    def move_lr(self, duty_l=0, duty_r=0):
        if duty_l < 0:
            self.pwm_lff.duty(0)
            self.pwm_lfb.duty(-duty_l)
            self.pwm_lbf.duty(0)
            self.pwm_lbb.duty(-duty_l)
        else:
            self.pwm_lfb.duty(0)
            self.pwm_lff.duty(duty_l)
            self.pwm_lbb.duty(0)
            self.pwm_lbf.duty(duty_l)
            
        if duty_r < 0:
            self.pwm_rff.duty(0)
            self.pwm_rfb.duty(-duty_r)
            self.pwm_rbf.duty(0)
            self.pwm_rbb.duty(-duty_r)
        else:
            self.pwm_rfb.duty(0)
            self.pwm_rff.duty(duty_r)
            self.pwm_rbb.duty(0)
            self.pwm_rbf.duty(duty_r)
            
            
    def stop(self):
        self.pwm_lfb.duty(0)
        self.pwm_rfb.duty(0)
        self.pwm_lff.duty(0)
        self.pwm_rff.duty(0)
        
        self.pwm_lbb.duty(0)
        self.pwm_rbb.duty(0)
        self.pwm_lbf.duty(0)
        self.pwm_rbf.duty(0)



if __name__ == '__main__':
    zy_miniMKNM = rawPWM_4WD_encoder()
    t_duty = 500
    for i in range(20):
        print("zyrot_mknm_IR_rawPWM test...", i)
        zy_miniMKNM.move_lr(t_duty, t_duty)
        time.sleep_ms(1000)
        zy_miniMKNM.move_lr(0, 0)
        time.sleep_ms(200)
        zy_miniMKNM.move_lr(-t_duty, -t_duty)
        time.sleep_ms(1000)
        zy_miniMKNM.move_lr(0, 0)
        time.sleep_ms(200)
        zy_miniMKNM.move_lr(0, -t_duty)
        time.sleep_ms(1000)
        zy_miniMKNM.move_lr(0, 0)
        time.sleep_ms(200)
        zy_miniMKNM.move_lr(-t_duty, 0)
        time.sleep_ms(1000)
        zy_miniMKNM.move_lr(0, 0)
        time.sleep_ms(200)
        
    zy_miniMKNM.stop()

