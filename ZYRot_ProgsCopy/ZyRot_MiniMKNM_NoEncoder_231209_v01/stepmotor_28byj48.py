from machine import Pin
from time import sleep_us,ticks_us

'''
http://www.taichi-maker.com/homepage/reference-index/motor-reference-index/28byj-48-stepper-motor-intro/
28byj48-5V 参数
步距角：5.625度   64step/circle
实测的减速比为(32/9)(22/11)(26/9)(31/10)≈63.684
64*63.684 = 4075.776 ~ 4076
起动转矩：300g*cm (100pps)
定位转矩：300g*cm
实测最高空载转速：0.25rps (15rpm,1Kpps)
'''


def stepmotor_28byj48_test():
    
    step_us = 200

    IN1 = Pin(26,Pin.OUT)
    IN2 = Pin(25,Pin.OUT)
    IN3 = Pin(33,Pin.OUT)
    IN4 = Pin(32,Pin.OUT)

    pins = [IN1, IN2, IN3, IN4]

    #sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    sequence_forward = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
    sequence_back =    [[1,0,0,0],[1,0,0,1],[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0]]

    start = ticks_us()
    for k in range(509):
        for step in sequence_forward:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep_us(step_us)
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)
    stop = ticks_us()
    print('rms:', 1_000_000/(stop-start))
    
    sleep_us(1_000_000)
    
    start = ticks_us()
    for k in range(509):
        for step in sequence_back:
            for i in range(len(pins)):
                pins[i].value(step[i])
                sleep_us(step_us)
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)
    stop = ticks_us()
    print('rms:', 1_000_000/(stop-start))
                
                
if __name__ == '__main__':
    stepmotor_28byj48_test()
            
            