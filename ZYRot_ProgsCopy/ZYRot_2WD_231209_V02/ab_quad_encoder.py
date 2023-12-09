from machine import Pin, PWM, ADC
import time

enc_pa = 16
enc_pb = 17



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


def dcmot_test(pin_front,pin_back):
    global enc_cnt
    global vrpm
    global enc_pin_a
    global enc_dir

    print('Start DC motor test...')
    pwmf = PWM(Pin(pin_front),duty=0,freq=1000)
    pwmb = PWM(Pin(pin_back),duty=0,freq=1000)
    print_cnt = 0
   
    test_duty = 500
    min_duty = 25
    max_duty = 1000
    for i in range(20):
        #print('Test cnt:',i)
        test_duty = i*50 
        if test_duty < min_duty:
            test_duty = min_duty
        elif test_duty > max_duty:
            test_duty = max_duty
            
        pwmf.duty(test_duty)
        #time.sleep_ms(1500)
        for j in range(25):
            time.sleep_ms(100)
            if print_cnt != enc_cnt:
                #print('enc_cnt:', enc_cnt, 'rps:', 1000000/irq_us)
                print('pwm:', test_duty//10, 'rps:',1000000//irq_us)
                print_cnt = enc_cnt
                
        pwmf.duty(0)
        pwmb.duty(0)
        time.sleep_ms(500)
        
        for j in range(10):
            time.sleep_ms(100)
            if print_cnt != enc_cnt:
                #print('enc_cnt:', enc_cnt, 'rps:', 1000000/irq_us)
                print('pwm:', test_duty//10, 'rps:',1000000//irq_us)
                print_cnt = enc_cnt
                
        pwmb.duty(test_duty)
        for j in range(25):
            time.sleep_ms(100)
            if print_cnt != enc_cnt:
                #print('enc_cnt:', enc_cnt, 'rps:', 1000000/irq_us)
                print('pwm:', test_duty//10, 'rps:',1000000//irq_us)
                print_cnt = enc_cnt 
                
        pwmb.duty(0)
        pwmf.duty(0)
        for j in range(10):
            time.sleep_ms(100)
            if print_cnt != enc_cnt:
                #print('enc_cnt:', enc_cnt, 'rps:', 1000000/irq_us)
                print('pwm:', test_duty//10, 'rps:',1000000//irq_us)
                print_cnt = enc_cnt
        
        
    pwmf.duty(0)
    pwmb.duty(0)
    print('End DC motor test.')
    

if __name__ == '__main__':
    init_enc()
    #dcmot_test(27,14)
    dcmot_test(27,14)
    for i in range(120):
        time.sleep_ms(500)
        print('enc_cnt:', enc_cnt)


