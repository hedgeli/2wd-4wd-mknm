__version__ = '0.0.1'
__author__ = 'ZyRot'
'''
手动示教演示程序
手动推动小车在地面运动,停止3秒后小车按推动时的速度复现示教运动
8x8点阵显示时间
'''

import zyrot_miniMKNM 
import hcsr04_irq 
import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
import time
from max7219_8x8led_iosimu import disp_num
    

def manual_teach_Demo():
    print('Start manual_teach_Demo...')
    start_time = time.ticks_ms()
    disp_time_s= -1
    
    teach_stage = 0
    
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

    sr04 = hcsr04_irq.Hcsr04Irq(trigger_pin = 2, echo_pin=4)
    disp_cm = 0
    max_dist = 500
    min_dist = 30
    high_dist = 110
    low_dist = 90
    
    teach_pos_list = []
    teach_cnt = 0
    flow_cnt = 0
    stop_cnt = 0
    
    mini_mknm.setMotPos(0,0,0,0)
    
    teach_max_times = 5
    teach_time_cnt = 0
    
    for i in range(120*100):
        if teach_stage == 1:
            mini_mknm.miniMknmPositionLoop()
        
        
        if i%10 == 0:
            cur_time_s = (time.ticks_ms()-start_time)//1000
            if cur_time_s != disp_time_s:
                # 显示时间,单位:秒
                disp_time_s = cur_time_s
                disp_num(int(disp_time_s)%100)
                
            # 记录手动示教的电机位置/速度数据
            if teach_stage == 0:
                motors_pos_mm = mini_mknm.getMotPos()
                print('TeaCnt:',teach_cnt,'Tea_pos1R:',motors_pos_mm[0],'Tea_pos1L:',motors_pos_mm[1],
                      'Tea_pos2R:',motors_pos_mm[2],'Tea_pos2L:',motors_pos_mm[3])
                teach_pos_list.append(motors_pos_mm)
                teach_cnt += 1
                if teach_cnt > 600:
                    print('teach time should less than 60 second.')
                    teach_stage = 10
                
                if teach_cnt > 2:
                    change = (abs(teach_pos_list[-1][0]-teach_pos_list[-2][0]) +
                             abs(teach_pos_list[-1][1]-teach_pos_list[-2][1]) +
                             abs(teach_pos_list[-1][2]-teach_pos_list[-2][2]) +
                             abs(teach_pos_list[-1][3]-teach_pos_list[-2][3]) )
                    if change <= 10:
                        stop_cnt += 1
                        if stop_cnt >= 50:     #  停止5秒后开始复现运动
                            teach_stage = 1
                    else:
                        stop_cnt = 0
                
            # 复现运动
            elif teach_stage == 1:
                if teach_cnt >= 60:
                    mini_mknm.setMotPos(teach_pos_list[flow_cnt][0],
                                        teach_pos_list[flow_cnt][1],
                                        teach_pos_list[flow_cnt][2],
                                        teach_pos_list[flow_cnt][3])
                    flow_cnt +=1
                    if flow_cnt >= teach_cnt:
                        print('Follow teach position finished.')
                        teach_time_cnt +=1
                        if teach_time_cnt <= teach_max_times:
                            teach_stage = 0
                            teach_cnt = 0
                            stop_cnt = 0
                            flow_cnt = 0
                            teach_pos_list.clear()
                            mini_mknm.release_all_motor()
                            start_time = time.ticks_ms()
                        else:
                            teach_stage = 2
                            teach_cnt = 0
                            stop_cnt = 0
                            flow_cnt = 0
                            teach_pos_list.clear()
                            mini_mknm.release_all_motor()
                            
                    motors_pos_mm = mini_mknm.getMotPos()
                    print('Len_cnt:',flow_cnt,'Lea_pos1R:',motors_pos_mm[0],'Lea_pos1L:',motors_pos_mm[1],
                      'Lea_pos2R:',motors_pos_mm[2],'Lea_pos2L:',motors_pos_mm[3])
                    
                else:
                    print("Teach time too short. Can't to flow.")
                    teach_time_cnt +=1
                    if teach_time_cnt == 1:
                        print('Motors are stoped,break teach mode')
                        break
                    if teach_time_cnt <= teach_max_times:
                        teach_stage = 0
                        teach_cnt = 0
                        stop_cnt = 0
                        flow_cnt = 0
                        teach_pos_list.clear()
                        mini_mknm.release_all_motor()
                        start_time = time.ticks_ms()
                    else:
                        teach_stage = 11
                        teach_cnt = 0
                        stop_cnt = 0
                        flow_cnt = 0
                        teach_pos_list.clear()
                        mini_mknm.release_all_motor()
            
            elif teach_stage == 2:
                print('Manual teach demo OK. teach_stage=', teach_stage)
                break
            else:
                print('error!  teach_stage=', teach_stage)
                break
                
        time.sleep_ms(10)

    mini_mknm.release_all_motor()
    mini_mknm.deinit_all_motor_pwm()
    time.sleep_ms(100)
    print('End of manual_teach_Demo.') 
    
if __name__ == '__main__':
    manual_teach_Demo()
        