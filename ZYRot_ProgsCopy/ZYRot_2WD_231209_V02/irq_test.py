import time
from machine import Pin, ADC, PWM

irq_cnt = 0
irq_timestamp = 0
irq_us = 0

def irq_test():
    global irq_cnt
    global irq_us
    print('irq_test()')
    pwm5 = PWM(Pin(5),freq = 1000, duty=512)
    irq_pin = Pin(14, Pin.IN)
    irq_pin.irq(trigger=Pin.IRQ_RISING,handler=irq_handle)
    for i in range(100):
        time.sleep_ms(100)
        print('irq_cnt:',irq_cnt, '  us:', irq_us)
    
    
def irq_handle(pin):
    global irq_timestamp
    global irq_cnt
    global irq_us
    irq_cnt = irq_cnt+1
    us = time.ticks_us()
    irq_us = us - irq_timestamp
    irq_timestamp = us
    
    
    
    
    
if __name__ == '__main__':
    irq_test()




