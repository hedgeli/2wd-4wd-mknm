from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq
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
    def __init__(self, m1, m2, c1, c2, freq = 500, minPWM=10, maxPWM=1000,
                 max_pwm_step=200):
        self.pos = 0
        self.direction = 0
        self.enc_period_us = 0 
        self.encoder_circle_pulse = 450   # 输出轴转动一圈对应的编码器脉冲数
        self.wheeld_mm = config.WHEEL_D_mm              # 车轮直径40mm        
        #self.k_speed = 1000000/450*self.wheel_d*3.1416    #
        self.k_mmps = 363029     #  1000000/450*52*3.1416
        self.k_pos_mm = 0.363  #  5.2*3.1416/450 cm
        
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


    # A function for speed control without feedback(Open loop speed control)
    def setPWMduty(self,Duty):
        pwm = Duty
        
        # 限制PWM值单步增量，用于控制电压电流变化幅度，减小运动加速度
        if pwm - self.curpwm > abs(self.max_pwm_step):
            pwm = self.curpwm + abs(self.max_pwm_step)
        if self.curpwm - pwm > abs(self.max_pwm_step):
            pwm = self.curpwm - abs(self.max_pwm_step)
            
        if pwm > self.maxpwm:
            pwm = self.maxpwm
        elif pwm < -self.maxpwm:
            pwm = -self.maxpwm
            
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
        self.curpwm = pwm
        
            
    def breakStop(self):
        self.curpwm = 0
        self.p_in1.duty(1023)
        self.p_in2.duty(1023)
        
    def release_motor(self):
        self.curpwm = 0
        self.p_in1.duty(0)
        self.p_in2.duty(0)


class PID:
    posPrev = 0

    def __init__(self, M, kp=1, ki=0, kd=0, umaxIn=800, eprev=0, 
                 max_run_ms=2500, tolerance=10, loop_maxms = 500, loop_minms=25,
                 max_interItem=800, dbg_info=0, ditem_toler = 5):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        
        self.pos_kp = kp    # 直流电机位置速度双闭环控制
        self.pos_ki = ki    # 位置环PID参数
        self.pos_kd = kd
        
        self.eintegral = 0.0
        self.I_Item = 0.0
        self.P_Item = 0.0
        self.D_Item = 0.0
        self.maxI_Item = max_interItem
        self.tolerance = tolerance   #
        self.ditem_toler = ditem_toler
        self.M = M                   # Motor object
        self.umaxIn  =umaxIn
        self.eprev = eprev
        self.max_pid_run_ms = max_run_ms
        self.ms_stamp = ticks_ms()
        self.out_time_flags = 0
        self.loop_stamp_ms = ticks_ms()
        self.loop_T_maxms = loop_maxms
        self.loop_T_minms = loop_minms
        self.loop_pre_pos = 0  #self.M.pos
        self.target = 0
        self.realvalue = 0
        self.pid_start_ms_stamp = ticks_ms()
        self.print_cnt = 0
        self.ctl_cnt = 0
        self.pid_type = 'init'
        self.dbg_info = dbg_info
        
    def release_pid_motor(self):
        self.M.release_motor()
        
    def break_stop_motor(self):
        self.M.breakStop()

    def setSpeedPID_val(self, Kp=1, Ki=0, Kd=0):
        self.kp = Kp;
        self.ki = Ki;
        self.kd = Kd;
        
    def setPostionPID_val(self, Kp=1, Ki=0, Kd=0):
        self.pos_kp = kp   
        self.pos_ki = ki  
        self.pos_kd = kd
        
        
    def set_tol_maxout_maxIntItem(self,tolerance=10,maxout=800,
                                  max_interItem=800):
        self.maxI_Item = max_interItem
        self.tolerance = tolerance
        self.umaxIn = maxout
        

    def evalu(self,value, target, deltaT):
        e = target-value
        
        #if abs(e) <= abs(self.tolerance):    # 
        #    return 0

        # Derivative
        dedt = (e-self.eprev)/(deltaT)
        
        self.P_Item = self.kp*e

        # Integral
        self.ctl_cnt = self.ctl_cnt + 1

        self.eintegral = self.eintegral + e*deltaT
        #print('eintegral',self.eintegral)
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
        if u > 0:
            if u > self.umaxIn:
                u = self.umaxIn
        else:
            if u < -self.umaxIn:
                u = -self.umaxIn

        self.eprev = e
        
#         if self.dbg_info == 1:
#             self.print_cnt = self.print_cnt + 1
#             if self.print_cnt >= 1:
#                 self.print_cnt = 0
#                 print('U:', int(u), 'T:',int(target), 'V:', int(value))  # for debugging           
        return u
    
    
    def setSpeedForPID(self, speed_mmps=0):
        self.pid_start_ms_stamp = ticks_ms()
        self.out_time_flags = 0
        self.target = speed_mmps
        if self.pid_type != 'speed':
            self.loop_stamp_ms = ticks_ms()
            self.pid_type = 'speed'
        
    def setPositionForPID(self, posi_mm=0):
        self.pid_start_ms_stamp = ticks_ms()
        self.out_time_flags = 0
        self.target = posi_mm
        if self.pid_type != 'position':
            self.loop_stamp_ms = ticks_ms()
            self.pid_type = 'position'
    
        
    
    def speedPIDloop(self):
        if self.pid_type != 'speed':
            return 
        
        loop_ms = ticks_ms()
        if loop_ms - self.loop_stamp_ms < self.loop_T_minms:
            return 
        
        if loop_ms - self.pid_start_ms_stamp > self.max_pid_run_ms:
            if self.out_time_flags <= 1:
                self.M.breakStop()     # out of time, stop motor
                #print('pid run out of time.')
                self.out_time_flags = self.out_time_flags + 1
            return 
        if self.out_time_flags > 0:
            return 
        
        deltaT_ms = loop_ms - self.loop_stamp_ms
        self.loop_stamp_ms = loop_ms
        
        state = disable_irq()
        enc_pos = self.M.pos
        per_us = self.M.enc_period_us
        enc_pre_us = self.M.stamp_us
        enable_irq(state)
        
        if self.target == 0:
            if per_us > 100:
                self.realvalue = self.M.direction*self.M.k_mmps/per_us
            if enc_pos == self.loop_pre_pos:
                self.realvalue = 0
            self.loop_pre_pos = enc_pos    
            self.print_pid_info()
            self.M.breakStop()
        
        elif (self.loop_pre_pos != enc_pos)and(per_us>100):
            #self.realvalue = 1000000/per_us/self.M.encoder_circle_pulse   # speed in rps
            self.realvalue = self.M.direction*self.M.k_mmps/per_us    # speed in mmps
            self.loop_pre_pos = enc_pos            
            x = int(self.evalu(self.realvalue, self.target, 1))
            self.M.setPWMduty(x)
            self.print_pid_info()

        elif (loop_ms-self.M.interrupt_stamp_ms) >= self.loop_T_maxms:
            self.realvalue = 0    # speed in mmps
            self.loop_pre_pos = enc_pos   
            x = int(self.evalu(self.realvalue, self.target, 1))
            self.M.setPWMduty(x)
            self.print_pid_info()
            
        return 
    
    def print_pid_info(self):
        if self.dbg_info == 1:
            print('U:', self.M.curpwm, 'T:',int(self.target), 'V:', int(self.realvalue))
           
        
     
    def positionPIDloop(self):
        loop_ms = ticks_ms()
        if loop_ms - self.loop_stamp_ms < self.loop_T_minms:
            return 
        
        if self.pid_type != 'position':
            return       
        
        if loop_ms - self.pid_start_ms_stamp > self.max_pid_run_ms:
            if self.out_time_flags <= 1:
                self.M.setPWMduty(0)     # out of time, stop motor
                #print('pid run out of time.')
                self.out_time_flags = self.out_time_flags + 1
            return 
        if self.out_time_flags > 0:
            return 
        
        deltaT_ms = loop_ms - self.loop_stamp_ms
        self.loop_stamp_ms = loop_ms
        
        state = disable_irq()
        enc_pos = self.M.pos
        per_us = self.M.enc_period_us
        enc_pre_us = self.M.stamp_us
        enable_irq(state)
        
        if (self.loop_pre_pos != enc_pos)and(per_us>100):
            self.realvalue = enc_pos*self.M.k_pos_mm
            self.loop_pre_pos = enc_pos
            
            if (self.target - self.realvalue) > abs(self.tolerance):
                # Call for control signal
                if self.eintegral < 0:
                    self.eintegral = 0
                if self.I_Item < 0:
                    self.I_Item = 0
                x = int(self.evalu(self.realvalue, self.target, 1))
                self.M.setPWMduty(x)
                self.print_pid_info()
            elif (self.realvalue - self.target) > abs(self.tolerance):
                if self.eintegral > 0:
                    self.eintegral = 0
                if self.I_Item > 0:
                    self.I_Item = 0
                x = int(self.evalu(self.realvalue, self.target, 1))
                self.M.setPWMduty(x)
                self.print_pid_info()
            else:
                x = 0
                self.eintegral = 0
                self.I_Item = 0
                self.M.breakStop()
                self.print_pid_info()
        else:
            self.realvalue = enc_pos*self.M.k_pos_mm
            self.loop_pre_pos = enc_pos
            if abs(self.realvalue-self.target) > abs(self.tolerance):
                x = int(self.evalu(self.realvalue, self.target, 1))
                self.M.setPWMduty(x)
                self.print_pid_info()
            else:
                x = 0
                self.eintegral = 0
                self.I_Item = 0
                self.M.breakStop()
                self.print_pid_info()            
        return
    
    
def pid_speed_test():
    print('Start dcmotor speed pid test.')
    # Creating objects of each motor
    m1 = Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32, max_pwm_step=250)
    #m2 = Motor(19, 18, 5, 14, 27)

    # Creating PID objects for each motor
    #p1 = PID(m1, 5, 0.1, 0.001, 800)
    p1 = PID(M=m1, kp=0.6, kd=0.3, ki=0.6, umaxIn=1000,
             max_interItem=1000 , dbg_info=1,tolerance=6)    # for speed PID para
    #p1 = PID(M=m1, kp=1, kd=0, ki=1, umaxIn=500,tolerance=10)    # for position PID para
    #p2 = PID(m2, 5, 0.1, 0.001, 800)
    
    start_ms = ticks_ms()
    test_step = 0
    while(1):
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                p1.setSpeedForPID(30)
        elif run_ms <= 4000:
            if test_step == 1:
                test_step = 2
                p1.setSpeedForPID(150)
        elif run_ms <= 6000:
            if test_step == 2:
                p1.setSpeedForPID(650)
                test_step = 3
        elif run_ms <= 8000:
            if test_step == 3:
                p1.setSpeedForPID(400)
                test_step = 4
        elif run_ms <= 10000:
            if test_step == 4:
                p1.setSpeedForPID(60)
                test_step = 5
        elif run_ms <= 12000:
            if test_step == 5:
                p1.setSpeedForPID(0)
                test_step = 6
        elif run_ms <= 14000:
            if test_step == 6:
                p1.setSpeedForPID(-300)
                test_step = 7
        elif run_ms <= 16000:
            if test_step == 7:
                p1.setSpeedForPID(-500)
                test_step = 8
        elif run_ms <= 18000:
            if test_step == 8:
                p1.setSpeedForPID(-600)
                test_step = 9
        elif run_ms <= 22000:
            if test_step == 9:
                p1.setSpeedForPID(-50)
                p1.M.breakStop()
                test_step = 10
        if run_ms >= 24000:
            p1.setSpeedForPID(0)
            if p1.pid_type == 'position':
                print('U:', 0, 'T:',p1.target, 'V:', int(p1.realvalue))
                print('U:', 0, 'T:',p1.target, 'V:', int(p1.realvalue))
            p1.M.breakStop()
            sleep_ms(300)
            p1.M.release_motor()
            print('DC motor speed pid test time over.')
            break
        
        p1.speedPIDloop()
        
        
def pid_position_test():
    print('Start dcmotor position pid test.')
    # Creating objects of each motor
    #m1 = Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32)
    #m1 = Motor_ABEncoder(m1=18, m2=5, c1=16, c2=17)
    m1 = Motor_ABEncoder(m1=21, m2=19, c1=23, c2=22)

    # Creating PID objects for each motor
    p1 = PID(M=m1, kp=0.6, kd=15, ki=3, umaxIn=900, tolerance=5,
             max_interItem=200,dbg_info=1)  
    #p2 = PID(m2, 5, 0.1, 0.001, 800)
    
    start_ms = ticks_ms()
    test_step = 0
    while(1):
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                p1.setPositionForPID(100)
        elif run_ms <= 3000:
            if test_step == 1:
                test_step = 2
                p1.setPositionForPID(50)
        elif run_ms <= 4000:
            if test_step == 2:
                p1.setPositionForPID(80)
                test_step = 3
        elif run_ms <= 5000:
            if test_step == 3:
                p1.setPositionForPID(180)
                test_step = 4
        elif run_ms <= 6000:
            if test_step == 4:
                p1.setPositionForPID(280)
                test_step = 5
        elif run_ms <= 7000:
            if test_step == 5:
                p1.setPositionForPID(0)
                test_step = 6
        elif run_ms <= 8000:
            if test_step == 6:
                p1.setPositionForPID(-200)
                test_step = 7
        elif run_ms <= 9000:
            if test_step == 7:
                p1.setPositionForPID(-250)
                test_step = 8
        elif run_ms <= 10000:
            if test_step == 8:
                p1.setPositionForPID(-80)
                test_step = 9
        elif run_ms <= 11000:
            if test_step == 9:
                p1.setPositionForPID(0)
                test_step = 10
        if run_ms >= 12000:
            p1.setPositionForPID(0)
            if p1.pid_type == 'position':
                print('U:', 0, 'T:',p1.target, 'V:', int(p1.realvalue))
                print('U:', 0, 'T:',p1.target, 'V:', int(p1.realvalue))
            p1.M.setPWMduty(0)
            p1.M.release_motor()
            print('DC motor position pid test time over.')
            break
        
        p1.positionPIDloop()

    
if __name__ == '__main__':
    pid_speed_test()
    #pid_position_test()

    



