from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq, Timer
import zyrot_config as config

# A class for functions related to motors
class Motor_ABEncoder:

    # Interrupt handler
    def handle_interrupt(self,pin):
        tick_us = ticks_us()
        self.enc_period_us = tick_us - self.stamp_us
        self.stamp_us = tick_us
        self.interrupt_stamp_ms = ticks_ms()
        a = self.px.value()
        if a > 0:
            self.pos = self.pos+1
            self.direction = 1
        else:
            self.pos = self.pos-1
            self.direction = -1

    # Constroctor for initializing the motor pins
    def __init__(self, m1, m2, c1, c2, freq = 500, minPWM=50, maxPWM=1000,
                 max_pwm_step=200):
        self.pos = 0
        self.direction = 0
        self.enc_period_us = 0 
        self.encoder_circle_pulse = 450   # 输出轴转动一圈对应的编码器脉冲数
        self.wheeld_mm = config.WHEEL_D_mm               # 车轮直径40mm
        
        #speed = (wheeld_mm*pi/450)/enc_period_us
        self.k_mmps = 1000000*3.1416* self.wheeld_mm/self.encoder_circle_pulse   
        self.k_pos_mm = self.wheeld_mm*3.1416/self.encoder_circle_pulse 
        
        self.stamp_us = ticks_us()
        self.interrupt_stamp_ms = 0
        self.enc_period_us = 0
        self.minpwm = minPWM
        self.maxpwm = maxPWM
        self.curpwm = 0
        self.max_pwm_step = max_pwm_step
        
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN, Pin.PULL_UP)
        self.freq = freq
        self.p_in1 = PWM(Pin(m1,Pin.OUT), freq=freq, duty=0)
        self.p_in2 = PWM(Pin(m2,Pin.OUT), freq=freq, duty=0)
        # Interrupt initialization
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)

    def get_pos_mm(self):
        return int(self.pos*self.k_pos_mm)
    
    def get_dir(self):
        return self.direction
    
    def get_speed_mmps(self):
        spe = 0
        if ((self.enc_period_us > 10) and
            ((ticks_ms() - self.interrupt_stamp_ms) < 100)):
            # 100ms对应最小可测量速度，40mm车轮时为2.8mm/s
            spe = int(self.direction * self.k_mmps / self.enc_period_us)
        return spe
            

    # A function for speed control without feedback(Open loop speed control)
    def setPWMduty(self,Duty):
        pwm = Duty
        
        if abs(pwm) >= abs(self.minpwm):
            # 限制PWM值单步增量，用于控制电压电流变化幅度，减小运动加速度
            if pwm - self.curpwm > abs(self.max_pwm_step):
                pwm = self.curpwm + abs(self.max_pwm_step)
            if self.curpwm - pwm > abs(self.max_pwm_step):
                pwm = self.curpwm - abs(self.max_pwm_step)
            
        pwm = int(pwm)
            
        if pwm > self.maxpwm:
            pwm = self.maxpwm
        elif pwm < -self.maxpwm:
            pwm = -self.maxpwm
            
        if pwm > 1023:    # 防止self.maxpwm的设定值出范围
            pwm = 1023
        elif pwm < -1023:
            pwm = -1023
        
        self.curpwm = pwm
            
        if abs(pwm) < abs(self.minpwm):
            pwm = 0
            self.p_in2.duty(0)
            self.p_in1.duty(0)
        elif pwm>0:
            self.p_in2.duty(0)
            self.p_in1.duty(pwm)
        else:
            self.p_in1.duty(0)
            self.p_in2.duty(-pwm)
        
        
            
    def breakStop(self):
        self.curpwm = 0
        self.p_in1.duty(1023)
        self.p_in2.duty(1023)
        
    def release_motor(self):
        self.curpwm = 0
        self.p_in1.duty(0)
        self.p_in2.duty(0)


class PID:
#    posPrev = 0

    def __init__(self, kp=1, ki=0, kd=0, samp_tms=10,
                 uMaxOut=800, eprev=0, name='pid',
                 max_run_ms=3200, tolerance=10,
                 loop_maxms = 300, loop_minms=5,
                 max_interItem=800, dbg_info=0, ditem_toler = 5):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        
        self.out_val = 0
        self.target = 0
        self.realvalue = 0
        
        self.create_stamp_ms = ticks_ms()
        
        self.name = name
        
        self.samp_tms = samp_tms
        
        self.eintegral = 0.0
        self.I_Item = 0.0
        self.P_Item = 0.0
        self.D_Item = 0.0
        self.maxI_Item = max_interItem
        self.tolerance = tolerance   #
        self.ditem_toler = ditem_toler
        self.uMaxOut  = uMaxOut   # 最大输出值
        self.eprev = eprev
        
        
        self.max_pid_run_ms = max_run_ms
        self.eval_stamp_ms = ticks_ms()
        self.over_time_flags = 0    # 超时标志
        self.loop_stamp_ms = ticks_ms()
        self.loop_T_maxms = loop_maxms
        self.loop_T_minms = loop_minms
        self.loop_pre_pos = 0  #self.M.pos
        self.pid_start_ms_stamp = ticks_ms()
        self.print_cnt = 0
        self.ctl_cnt = 0
#         self.pid_type = 'init'
        self.dbg_info = dbg_info
        
    def set_target(self, new_target):
        self.target = new_target
        self.over_time_flags = 0
        self.pid_start_ms_stamp = ticks_ms()   # 目标值改变时更新控制时间戳
        self.loop_stamp_ms = ticks_ms()
        
    def get_target(self):
        return self.target
        
    def set_maxout(self, max_out):
        self.uMaxOut  = new_maxout
        self.over_time_flags = 0
        self.pid_start_ms_stamp = ticks_ms()  
        self.loop_stamp_ms = ticks_ms() 
        
    def set_target_maxout(self, new_target, new_maxout):
        self.target = new_target
        self.uMaxOut  = new_maxout
        self.over_time_flags = 0
        self.pid_start_ms_stamp = ticks_ms()  
        self.loop_stamp_ms = ticks_ms() 
        

    def setPID_para(self, Kp=1, Ki=0, Kd=0):
        self.kp = Kp;
        self.ki = Ki;
        self.kd = Kd;
        
        self.over_time_flags = 0
        self.pid_start_ms_stamp = ticks_ms() 
        self.loop_stamp_ms = ticks_ms()
        
    def set_tol_maxout_maxIntItem(self,tolerance=10,maxout=800,
                                  max_i_Item=800):
        self.maxI_Item = max_i_Item
        self.tolerance = tolerance
        self.uMaxOut = maxout
        
    def set_realvalue(self, realvalue):
        self.realvalue = realvalue
        
    def get_realvalue(self):
        return self.realvalue

    def evalu(self,value, target):
        e = target-value
        delta_ms = ticks_ms() - self.eval_stamp_ms
        self.eval_stamp_ms = ticks_ms()
        
        if (ticks_ms() - self.pid_start_ms_stamp >= self.max_pid_run_ms):
            self.over_time_flags = 1
#             return self.out_val
#         
#         if abs(e) <= abs(self.tolerance):
#             self.print_pid_info()    
#             return self.out_val         # 小于控制误差时保持原输出
        
        delt_s = delta_ms / 1000

        # Derivative
        dedt = (e-self.eprev)/(delt_s)
        
        self.P_Item = self.kp*e

        # Integral

        self.eintegral = self.eintegral + e*delt_s
        self.I_Item = self.ki * self.eintegral
        #print('I_Item',self.I_Item)
        if self.I_Item > self.maxI_Item:
            self.I_Item = self.maxI_Item
        elif self.I_Item < -self.maxI_Item:
            self.I_Item = -self.maxI_Item
        
        if abs(dedt) <= abs(self.ditem_toler):
            dedt = 0
        self.D_Item = self.kd*dedt
        # Control signal
        u = self.P_Item + self.I_Item + self.D_Item 
        
        # Direction and power of  the control signal

        if u > abs(self.uMaxOut):
            u = abs(self.uMaxOut)

        if u < -abs(self.uMaxOut):
            u = -abs(self.uMaxOut)

        self.eprev = e
        self.out_val = u
        self.print_pid_info()         
        return u
    
    def print_pid_info(self):
        if config.motor_pid_log_level == config.MOTOR_PID_LOG:
            if self.dbg_info == 1:
                print(self.name, (ticks_ms()-self.create_stamp_ms)/1000,
                      ',U,', int(self.out_val), ',T,',int(self.target),
                      ',V,', int(self.realvalue))
           
         
class DCmot_PosSpe_Dual_PID:
    def loop_callback(self, tim):
        #self.dual_pid_loop()    # 
        self.callback_flag = self.callback_flag + 1
    
    def __init__(self, pid_outter, pid_inner, motor, timerId=0,
                 max_run_ms=2000, name='dpid'):
        self.pid_outter = pid_outter   # 外环，位置环  
        self.pid_inner = pid_inner     # 内环，速度环
        self.motor = motor
        self.timerId = timerId
        self.flag_stop = 0
        self.name = name
        self.callback_flag = 0
        self.callback_period = min(self.pid_outter.samp_tms,
                                   self.pid_inner.samp_tms)
        self.timer = Timer(timerId)
        self.timer.init(period=self.callback_period, mode=Timer.PERIODIC,
                        callback=self.loop_callback)
        
    def end_control(self):
        if self.flag_stop == 0:
            #state = disable_irq()
            self.flag_stop = 1
            self.timer.deinit()
            self.pid_inner.set_target(0)
            self.motor.setPWMduty(0)
            self.motor.release_motor()
            if config.motor_pid_log_level == config.MOTOR_PID_LOG:
                print(self.pid_outter.name, 'end_control.')
            #enable_irq(state)
        
    def start_control(self):
        if self.flag_stop >= 1:
            self.flag_stop = 0
            self.timer = Timer(self.timerId)
            self.timer.init(period=self.callback_period, mode=Timer.PERIODIC,
                            callback=self.loop_callback)
        
    def dual_pid_loop(self):
        loop_ms = ticks_ms()
        if self.flag_stop == 1:
            self.end_control()
            self.motor.breakStop()
            return
        if self.callback_flag == 0:
            return
        if self.callback_flag >=2:
            print(self.name,'callback_flag,', self.callback_flag)
            
        self.callback_flag = 0
        if self.pid_outter.over_time_flags >= 1:
            self.end_control()
            self.motor.breakStop()
            self.pid_outter.over_time_flags = self.pid_outter.over_time_flags -1
            print(self.pid_outter.name, 'over_time !')
            return
            
        if loop_ms - self.pid_outter.loop_stamp_ms >= self.pid_outter.samp_tms:
            # 外环，位置环 PID 控制
            self.pid_outter.loop_stamp_ms = loop_ms
            # get real_val_out position
            real_position = self.motor.get_pos_mm()
            self.pid_outter.set_realvalue(real_position)
            
            if(abs(real_position - self.pid_outter.target) <=
               abs(self.pid_outter.tolerance)):
                #state = disable_irq()
                self.motor.breakStop()   # 小于位置控制允许误差后刹停电机
                #print('pid_pos less than tolerance.')
                self.pid_outter.eintegral = 0
                self.pid_outter.I_Item = 0
                self.pid_inner.eintegral = 0
                self.pid_inner.I_Item = 0
                self.pid_inner.set_target(0)  # 内环速度强置为0
                self.end_control()
                #enable_irq(state)
                return
               
#             else:
            ctl_d_ms = ticks_ms() - self.pid_outter.loop_stamp_ms
            pid_outter_res = self.pid_outter.evalu(real_position,
                                                self.pid_outter.target)
            # 设置内环速度目标值
            self.pid_inner.set_target(pid_outter_res)
            #return
            
        if ((loop_ms - self.pid_inner.loop_stamp_ms) >=
            self.pid_inner.samp_tms):
            # 内环，速度环 PID 控制
            self.pid_inner.loop_stamp_ms = loop_ms
            # get real_val_in  speed
            real_speed = self.motor.get_speed_mmps()
            self.pid_inner.set_realvalue(real_speed)
#             print('pid_inner', real_speed)
            pid_inner_result = self.pid_inner.evalu(real_speed,
                                                    self.pid_inner.target)
            # Control system set with pid_in_result
            if self.flag_stop == 0:
                self.motor.setPWMduty(pid_inner_result)
        return 
    
         
def pos_spe_dualPID_test(N=8):
    print('Start pos_spe_dualPID_test')
    # Creating objects of each motor
    
    m1 = Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26)  #前右轮
    m2 = Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32)  #前左轮

    #m1 = Motor_ABEncoder(m1=18, m2=5, c1=16, c2=17)
    #m1 = Motor_ABEncoder(m1=21, m2=19, c1=23, c2=22)
    
    # Creating PID objects for each motor
    pid_speed = PID(kp=1.3, kd=0, ki=0.2, uMaxOut=900, tolerance=15,
             samp_tms = 20, max_interItem=200,dbg_info=0, name='pid_spe')
    
    pid_postion = PID(kp=1.8, kd=0, ki=0.3, uMaxOut=600, tolerance=10,
             samp_tms = 100, max_interItem=80,dbg_info=0,name='pid_pos')
    mot_pid_pos_spe = DCmot_PosSpe_Dual_PID(pid_outter=pid_postion, pid_inner=pid_speed,
                          motor=m1, timerId=0)
    
    pid_speed2 = PID(kp=1.3, kd=0, ki=0.2, uMaxOut=900, tolerance=15,
             samp_tms = 20, max_interItem=200,dbg_info=0, name='pid_spe2')
    
    pid_postion2 = PID(kp=1.8, kd=0, ki=0.3, uMaxOut=600, tolerance=10,
             samp_tms = 100, max_interItem=80,dbg_info=0, name='pid_pos2')
    mot_pid_pos_spe2 = DCmot_PosSpe_Dual_PID(pid_outter=pid_postion2, pid_inner=pid_speed2,
                          motor=m2, timerId=1)
    
    start_ms = ticks_ms()
    test_s = 0
    para_set_s = -1
    test_stage = 0
    run_ms = 0
    print_pos_ms = -1
    while test_stage <= N:
        mot_pid_pos_spe2.dual_pid_loop()
        mot_pid_pos_spe.dual_pid_loop()
        
        i = test_stage
        run_ms = ticks_ms() - start_ms
        if (run_ms%100 == 0) and (print_pos_ms != run_ms):
            print_pos_ms = run_ms
#             print('m1_pos_mm,',m1.get_pos_mm(),
#               'm1_spe_mmps,',m1.get_speed_mmps(),
#               ',m2_pos_mm,', m2.get_pos_mm(),
#               ',m2_spe_mmps,', m2.get_speed_mmps())
            print('S',run_ms/1000, 'm1_pos,',m1.get_pos_mm(), 't1',pid_postion.get_target(),
              ',m2_pos,', m2.get_pos_mm(), 't2',pid_postion2.get_target() )
        test_s = run_ms//1000
        if((test_s==0)and(para_set_s!=test_s)):
            para_set_s = test_s
            pid_postion2.set_target_maxout(200, 200)
            mot_pid_pos_spe2.start_control()
            pid_postion.set_target_maxout(200, 200)
            mot_pid_pos_spe.start_control()
        if((test_s==2)and(para_set_s!=test_s)):
            para_set_s = test_s
            pid_postion2.set_target_maxout(0, -200)
            mot_pid_pos_spe2.start_control()
            pid_postion.set_target_maxout(0, -200)
            mot_pid_pos_spe.start_control()
#         if((test_s==4)and(para_set_s!=test_s)):
#             para_set_s = test_s
#             pid_postion2.set_target_maxout(200*i, 200)
#             mot_pid_pos_spe2.start_control()
#             pid_postion.set_target_maxout(200*i, -200)
#             mot_pid_pos_spe.start_control()
        if test_s >= 4:
            start_ms = ticks_ms()
            test_stage = test_stage + 1
            print('test_stage:', test_stage)
        
    mot_pid_pos_spe.end_control()
    mot_pid_pos_spe2.end_control()
    print('End pos_spe_dualPID_test')
    

def motor_pos_spe_test(N=60*4):
    m1 = Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26)  #前右轮
    m2 = Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32)  #前左轮
    
    for i in range(N):
        print('m1_pos_mm,',m1.get_pos_mm(),
              'm1_spe_mmps,',m1.get_speed_mmps(),
              ',m2_pos_mm,', m2.get_pos_mm(),
              ',m2_spe_mmps,', m2.get_speed_mmps()
              )
        sleep_ms(250)
    

    
if __name__ == '__main__':
    pos_spe_dualPID_test()
    #motor_pos_spe_test()

