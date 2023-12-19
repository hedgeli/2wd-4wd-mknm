'''
file: dc_mot_test.py
直流电机PWM开环控制
使用增量式AB相编码器测量电机转速，测量脉冲宽度（T法测量）
'''
from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq

class DC_Motor():
    def __init__(self,PinFor,PinBack,PinEncA=0,PinEncB=0,Freq=500, maxDuty=1000, Name='DCMot1'):
        self.pwmf = PWM(Pin(PinFor), freq=Freq, duty=0)
        self.pwmb = PWM(Pin(PinBack), freq=Freq, duty=0)
        self.max_duty = maxDuty
        self.name = Name
        self.stamp_us = 0
        self.enc_period_us = 0
        self.interrupt_stamp_ms = 0
        self.enc_n_per_cir = 450
        self.pos = 0
        if (PinEncA != 0) and (PinEncB != 0):
            self.pin_encA = Pin(PinEncA, Pin.IN, Pin.PULL_UP)
            self.pin_encB = Pin(PinEncB, Pin.IN, Pin.PULL_UP)
            # Interrupt initialization
            self.pin_encB.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
        
        # Interrupt handler
    def handle_interrupt(self,pin):
        tick_us = ticks_us()
        self.enc_period_us = tick_us - self.stamp_us
        self.stamp_us = tick_us
        self.interrupt_stamp_ms = ticks_ms()
        a = self.pin_encA.value()
        if a > 0:
            self.pos = self.pos+1 
        else:
            self.pos = self.pos-1
    
    def set_duty(self, Duty=0):
        if Duty > self.max_duty:
            Duty = self.max_duty
        if Duty < -self.max_duty:
            Duty = -self.max_duty
        if Duty == 0:
            self.pwmf.duty(0)
            self.pwmb.duty(0)
        if Duty > 0:
            self.pwmb.duty(0)
            self.pwmf.duty(Duty)
        if Duty < 0:
            self.pwmf.duty(0)
            self.pwmb.duty(-Duty)
            
    def merge_stop(self,Duty=1000):
        self.pwmf.duty(Duty)
        self.pwmb.duty(Duty)
    
        
        
if __name__ == '__main__':
    # 关闭另外3个电机
    p12 = Pin(12, mode=Pin.OUT, pull=None)
    p13 = Pin(13, mode=Pin.OUT, pull=None)
    p19 = Pin(19, mode=Pin.OUT, pull=None)
    p21 = Pin(21, mode=Pin.OUT, pull=None)
    
    p5 = Pin(5, mode=Pin.OUT, pull=None)    #后左电机
    p18 = Pin(18, mode=Pin.OUT, pull=None)
    
    # 测试前左电机
    m1 = DC_Motor(27,14,32,33,Name='m1')
    for i in range(10):
        duty = i * 100 + 100
#         duty = 100
        pre_pos = m1.pos
        #print('duty:', duty)
        m1.set_duty(duty)
        for j in range(60):
            
            #print('duty:',duty,'per_us:',m1.enc_period_us,'pos:', m1.pos)
            if m1.enc_period_us > 0:
                # rps = 1000000/450/m1.enc_period_us
                # cmps = rps*5.2*3.1416 = 36303/m1.enc_period_us
                print('duty,',duty//10,',cmps,',36303//m1.enc_period_us,",pos_inc,",m1.pos-pre_pos)
                pre_pos = m1.pos
            sleep_ms(8)
        m1.merge_stop()
        for j in range(40):
            
            #print('duty:',duty,'per_us:',m1.enc_period_us,'pos:', m1.pos)
            if m1.enc_period_us > 0:
                print('duty,',0,',cmps,',36303//m1.enc_period_us,",pos_inc,",m1.pos-pre_pos)
                pre_pos = m1.pos
            sleep_ms(8)
    m1.set_duty(0)
        


    
