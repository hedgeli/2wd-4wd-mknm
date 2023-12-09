
from machine import Pin, PWM, ADC
import time

test_duty = 700
test_time = 1000

def pwm_init():
    global pwm1, pwm2, pwm3,pwm4,pwm5,pwm6
    global pwm7, pwm8, pwm9,pwm10,pwm11,pwm12
    
    Pin(27, Pin.OUT, value=0)
    Pin(14, Pin.OUT, value=0)
    Pin(12, Pin.OUT, value=0)
    Pin(13, Pin.OUT, value=0)
    
    Pin(21, Pin.OUT, value=0)
    Pin(19, Pin.OUT, value=0)
    Pin(18, Pin.OUT, value=0)
    Pin(5, Pin.OUT, value=0)
    
    time.sleep_ms(100)
    
    pwm1 = PWM(Pin(27), freq=500, duty=0)
    pwm2 = PWM(Pin(14), freq=500, duty=0)
    
    pwm4 = PWM(Pin(12), freq=500, duty=0)
    pwm3 = PWM(Pin(13), freq=500, duty=0) 
    
    
    pwm6 = PWM(Pin(5), freq=500, duty=0)
    pwm5 = PWM(Pin(18), freq=500, duty=0)   
    
    pwm7 = PWM(Pin(19), freq=500, duty=0)
    pwm8 = PWM(Pin(21), freq=500, duty=0)
    
    pwm9 = PWM(Pin(26), freq=500, duty=0)   
    pwm10 = PWM(Pin(15), freq=500, duty=0)

    pwm11 = PWM(Pin(23), freq=500, duty=0)
    pwm12 = PWM(Pin(22), freq=500, duty=0)
    
    time.sleep_ms(100)
    


def motor_forward():
    global pwm1, pwm2, pwm3,pwm4,pwm5,pwm6
    global pwm7, pwm8, pwm9,pwm10,pwm11,pwm12
    
    pwm2.duty(0)
    pwm4.duty(0)
    
    pwm6.duty(0)
    pwm8.duty(0)
    
    pwm10.duty(0)
    pwm12.duty(0) 
    
    pwm1.duty(test_duty)
    pwm3.duty(test_duty)
    
    pwm5.duty(test_duty)
    pwm7.duty(test_duty)

    pwm9.duty(test_duty)
    pwm11.duty(test_duty)
    
    time.sleep_ms(test_time)
    

    pwm5.duty(0)
    pwm9.duty(0)
    
    pwm1.duty(0)
    pwm3.duty(0)
    
    pwm7.duty(0)
    pwm11.duty(0)
    
    time.sleep_ms(500)
    
    

def motor_back():
    global pwm1, pwm2, pwm3,pwm4,pwm5,pwm6
    global pwm7, pwm8, pwm9,pwm10,pwm11,pwm12
    
    pwm5.duty(0)
    pwm9.duty(0)
    
    pwm1.duty(0)
    pwm3.duty(0)
    
    pwm7.duty(0)
    pwm11.duty(0)
    
    pwm2.duty(test_duty)
    pwm4.duty(test_duty)
    
    pwm6.duty(test_duty)
    pwm8.duty(test_duty)

    pwm10.duty(test_duty)
    pwm12.duty(test_duty)
    
    time.sleep_ms(test_time)
    

    pwm2.duty(0)
    pwm4.duty(0)
    
    pwm6.duty(0)
    pwm8.duty(0)
    
    pwm10.duty(0)
    pwm12.duty(0) 
    
    time.sleep_ms(500)


def pwm_motor_test(n=3):
    pwm_init()
    for i in range(n):
        print('motor test NO:', i) 
        motor_forward()
        time.sleep_ms(200)
        motor_back()
        time.sleep_ms(200)



if __name__ == '__main__':
    pwm_motor_test()


