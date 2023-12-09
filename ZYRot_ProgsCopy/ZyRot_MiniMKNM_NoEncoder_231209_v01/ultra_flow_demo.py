__version__ = '0.0.1'
__author__ = 'ZyRot'
'''
超声跟随演示程序
超声测距值大于120mm时前进10mm，小于90mm时后退10mm
小车与障碍物保持距离在9－12cm之间
'''

import zyrot_miniMKNM 
import hcsr04_irq 
import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
import time
from max7219_8x8led_iosimu import disp_num

def ultraFlowDemo():
    print('Start ultraFlowDemo...')
    
    m2l = motor.Motor_ABEncoder(m1=5, m2=18, c1=17, c2=16, max_pwm_step=100)    #后左轮
    m2r = motor.Motor_ABEncoder(m1=21, m2=19, c1=23, c2=22, max_pwm_step=100)   #后右轮
    
    m1r = motor.Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26, max_pwm_step=100)  #前右轮
    m1l = motor.Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32, max_pwm_step=100)  #前左轮
    
    p2r = motor.PID(M=m2r, kp=0.6, kd=15, ki=3, umaxIn=800, tolerance=8,
             max_interItem=200,dbg_info=0)
    p2l = motor.PID(M=m2l, kp=0.6, kd=15, ki=3, umaxIn=800, tolerance=8,
             max_interItem=200,dbg_info=0)
    p1r = motor.PID(M=m1r, kp=0.6, kd=15, ki=3, umaxIn=800, tolerance=8,
             max_interItem=200,dbg_info=0)
    p1l = motor.PID(M=m1l, kp=0.6, kd=15, ki=3, umaxIn=800, tolerance=8,
             max_interItem=200,dbg_info=0)
    
    mini_mknm = zyrot_miniMKNM.MiniMknm(p1r,p1l,p2r,p2l)
    demo_stage = 0
    sr04 = hcsr04_irq.Hcsr04Irq(trigger_pin = 2, echo_pin=4)
    disp_cm = 0
    max_dist = 400
    min_dist = 50
    high_dist = 140
    low_dist = 100
    
    over_dist_range_cnt = 0
    max_over_dist_NO = 20
    
    for i in range(120*100):
        mini_mknm.miniMknmPositionLoop()
        if i%10 == 0:
            sr04.trig_start()
            distance = sr04.get_dist_mm()
            print('Dis_mm:',distance)
            if disp_cm != distance//10:
                disp_cm = distance//10
                disp_num(disp_cm)
            # 超声测距值大于110mm时前进10mm
            if (distance >= high_dist)and(distance <= max_dist):
                mini_mknm.setMknmDPos(10,0)
                over_dist_range_cnt = 0
            # 测距值小于90mm时后退10mm
            elif (distance <= low_dist)and(distance >= min_dist):
                mini_mknm.setMknmDPos(-10,0)
                over_dist_range_cnt = 0
            # 测距值超出最大最小范围累计时长
            elif (distance > max_dist) or (distance < min_dist):
                over_dist_range_cnt += 1
                if over_dist_range_cnt >= max_over_dist_NO:
                    break
                
                
        time.sleep_ms(10)

    mini_mknm.release_all_motor()
    mini_mknm.deinit_all_motor_pwm()
    print('End of ultraFlowDemo.') 
    
if __name__ == '__main__':
    ultraFlowDemo()
        

