from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq

# A class for functions related to motors
class Motor_OpenLoop:

    pos = 0
    enc_period_us = 0 
    encoder_circle_pulse = 48   # 输出轴转动一圈对应的编码器脉冲数

    # Interrupt handler
    def handle_interrupt(self,pin):
        tick_us = ticks_us()
        self.enc_period_us = tick_us - self.stamp_us
        self.stamp_us = tick_us
        self.interrupt_stamp_ms = ticks_ms()
        a = self.px.value()
        if a > 0:
            self.pos = self.pos+1 
        else:
            self.pos = self.pos-1

    # Constroctor for initializing the motor pins
    def __init__(self, m1, m2, c1, c2, freq = 500, minPWM=200, maxPWM=1000):
        self.stamp_us = ticks_us()
        self.interrupt_stamp_ms = 0
        self.enc_period_us = 0
        self.minpwm = minPWM
        self.maxpwm = maxPWM
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN, Pin.PULL_UP)
        self.freq = freq
        self.p_in1 = PWM(Pin(m1,Pin.OUT), freq=freq, duty=0)
        self.p_in2 = PWM(Pin(m2,Pin.OUT), freq=freq, duty=0)
        # Interrupt initialization
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)

    # Arduino's map() function implementation in python 
    def convert(self, x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    # A function for speed control without feedback(Open loop speed control)
    def speed(self,M):
        pwm = self.convert(abs(M),0, 1000, 0, 1000) 
        #print('pwm:', pwm)
        if pwm < self.minpwm:
            self.p_in2.duty(0)
            self.p_in1.duty(0)
        elif M>0:
            self.p_in2.duty(0)
            self.p_in1.duty(pwm)
        else:
            self.p_in1.duty(0)
            self.p_in2.duty(pwm)



if __name__ == '__main__':
    print('Motor open loop test...')
    mot1 = Motor_OpenLoop(m1=12, m2=13, c1=22, c2=23)
    mot2 = Motor_OpenLoop(m1=14, m2=27, c1=16, c2=17)
    sleep_ms(100)        #初始化后必需加延时才能让电机正常运动！？
    mot1.speed(500)
    mot2.speed(500)
    sleep_ms(5000)
    mot1.speed(0)
    mot2.speed(0)
    sleep_ms(300)
    print('m1 pos:', mot1.pos, '  m2 pos:', mot2.pos)
    mot1.speed(-500)
    mot2.speed(-500)
    sleep_ms(5000)
    mot1.speed(0)
    mot2.speed(0)
    sleep_ms(300)
    print('m1 pos:', mot1.pos, '  m2 pos:', mot2.pos)
    
    mot1.speed(700)
    mot2.speed(700)
    sleep_ms(5000)
    mot1.speed(0)
    mot2.speed(0)
    sleep_ms(300)
    print('m1 pos:', mot1.pos, '  m2 pos:', mot2.pos)
    mot1.speed(-700)
    mot2.speed(-700)
    sleep_ms(5000)
    mot1.speed(0)
    mot2.speed(0)
    sleep_ms(300)
    print('m1 pos:', mot1.pos, '  m2 pos:', mot2.pos)
    
    print('End motor open loop test.')


