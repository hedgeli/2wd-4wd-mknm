'''
输出轴1圈对应编码器线数: 450
编码器最高频率: 2000Hz
输出轴最高转速: 4.3rps  260rpm
52mm轮对应速度: 70cmps
控制频率25ms,编码器最小增量10,对应速度0.9rps,14.5cmps,编码器周期2.5ms
'''

from machine import Pin, PWM, ADC
import time

enc_pa = 32
enc_pb = 33


enc_cnt = 0
irq_us = 0
vrpm = 0
irq_timestamp = 0
irq_us = 0
enc_dir = 0

def init_enc():
    global enc_pa
    global enc_pb
    global enc_pin_a
    global enc_pin_b
    enc_pin_a = Pin(enc_pa, Pin.IN, Pin.PULL_UP)
    enc_pin_a.irq(trigger=Pin.IRQ_RISING,handler=enc_handle)
    enc_pin_b = Pin(enc_pb, Pin.IN,Pin.PULL_UP)


def enc_handle(pin):
    global irq_timestamp 
    global enc_cnt
    global irq_us
    global enc_pin_b
    global enc_dir
    enc_dir = enc_pin_b.value()
    if  enc_dir == 0:
        enc_cnt = enc_cnt-1
    elif enc_dir == 1:
        enc_cnt = enc_cnt+1
    us = time.ticks_us()
    irq_us = us - irq_timestamp
    irq_timestamp = us


def dcmot_test(pin_front,pin_back,duty=500):
    global enc_cnt
    global vrpm
    global enc_pin_a
    global enc_dir

    print('Start DC motor test...')
    pwmf = PWM(Pin(pin_front),duty=0,freq=1000)
    pwmb = PWM(Pin(pin_back),duty=0,freq=1000)
    print_cnt = 0
   
    test_duty = duty
    min_duty = 25
    max_duty = 1000
    for i in range(20):
        #print('Test cnt:',i)
        #test_duty = i*50 
        if test_duty < min_duty:
            test_duty = min_duty
        elif test_duty > max_duty: 
            test_duty = max_duty
            
        pwmf.duty(test_duty)
        for j in range(50):
            time.sleep_ms(25)
            if print_cnt != enc_cnt:
                print('pwm:', test_duty//10, 'cmps:',round(36284/irq_us,2), 'dcnt:',enc_cnt-print_cnt)
                print_cnt = enc_cnt
                
        pwmf.duty(0)
        pwmb.duty(0)
        time.sleep_ms(500)
        
        for j in range(50):
            time.sleep_ms(25)
            if print_cnt != enc_cnt:
                print('pwm:', test_duty//10,'cmps:',round(36284/irq_us,2), 'dcnt:',enc_cnt-print_cnt)
                print_cnt = enc_cnt
                
        pwmb.duty(test_duty)
        for j in range(50):
            time.sleep_ms(25)
            if print_cnt != enc_cnt:
                print('pwm:', test_duty//10, 'cmps:',round(36284/irq_us,2),'dcnt:',enc_cnt-print_cnt)
                print_cnt = enc_cnt 
                
        pwmb.duty(0)
        pwmf.duty(0)
        for j in range(30):
            time.sleep_ms(25)
            if print_cnt != enc_cnt:
                #print('enc_cnt:', enc_cnt, 'rps:', 1000000/irq_us)
                print('pwm:', test_duty//10, 'cmps:',round(36284/irq_us,2), 'dcnt:',enc_cnt-print_cnt)
                print_cnt = enc_cnt
        
        
    pwmf.duty(0)
    pwmb.duty(0)
    print('End DC motor test.')
    

if __name__ == '__main__':
    init_enc()
    dcmot_test(27,14,duty=100)
    for i in range(120):
        time.sleep_ms(500)
        print('enc_cnt:', enc_cnt)


