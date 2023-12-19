
__version__ = '0.0.1'
__author__ = 'ZyRot'
'''
超声自主避障演示程序
超声测距值小于60mm时左移10mm，小于50mm时后退10mm,大于100mm时前进20mm直到再次小于60mm.
总左移超过150mm,测距值不大于100mm时顺时针旋转找出距离最大值的方向前进.
小车与障碍物保持距离在9－11cm之间
'''

import zyrot_miniMKNM 
import hcsr04_irq 
import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
import time
from max7219_8x8led_iosimu import disp_num

def ultraAutoDemo():
    print('Start ultraAutoDemo...')
    
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
    max_dist = 900
    min_dist = 30
    high_dist = 110
    low_dist = 90
    
    pos_x = 0
    pos_y = 0
    car_dir = 0
    
    for i in range(30*100):
        mini_mknm.miniMknmPositionLoop()
        if i%10 == 0:
            sr04.trig_start()
            distance = sr04.get_dist_mm()
            print('Dis_mm:',distance)
            if disp_cm != distance//10:
                disp_cm = distance//10
                # 显示测距值,单位为cm
                disp_num(disp_cm)
            # 超声测距值大于90mm时前进10mm
            if (distance >= 90)and(distance <= max_dist):
                mini_mknm.setMknmDPos(10,0)
                pos_x += 10
            # 测距值小于90mm时右转90度
            elif (distance < 90)and(distance >= 60):
                #mini_mknm.setMknmDPos(0,-30)
                #pos_y -= 30
                mini_mknm.setMknm_dDirArc(3.1416/4)
                car_dir += 3.1416/4
            elif (distance < 60)and(distance >= 30):
                mini_mknm.setMknmDPos(-20,0)
                pos_x -= 20
            
        time.sleep_ms(10)


    mini_mknm.release_all_motor()
    mini_mknm.deinit_all_motor_pwm()
    print('End of ultraAutoDemo.') 
    
if __name__ == '__main__':
    ultraAutoDemo()
        




