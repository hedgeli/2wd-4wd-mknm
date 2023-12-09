from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq

# A class for functions related to motors
class Motor:

    pos = 0
    enc_period_us = 0 
    #encoder_circle_pulse = 48   # 输出轴转动一圈对应的编码器脉冲数
    encoder_circle_pulse = 450

    # Interrupt handler
    def handle_interrupt(self,pin):
        tick_us = ticks_us()
        self.enc_period_us = tick_us - self.stamp_us
        self.stamp_us = tick_us
        self.interrupt_stamp_ms = ticks_ms()
        a = self.px.value()
        if a > 0:
            self.pos = self.pos+1 
        else:
            self.pos = self.pos-1

    # Constroctor for initializing the motor pins
    def __init__(self, m1, m2, c1, c2, freq = 1000, minPWM=200, maxPWM=1000):
        self.stamp_us = ticks_us()
        self.interrupt_stamp_ms = 0
        self.enc_period_us = 0
        self.minpwm = minPWM
        self.maxpwm = maxPWM
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN, Pin.PULL_UP)
        self.freq = freq
        self.p_in1 = PWM(Pin(m1,Pin.OUT), freq=freq, duty=0)
        self.p_in2 = PWM(Pin(m2,Pin.OUT), freq=freq, duty=0)
        # Interrupt initialization
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)

    # Arduino's map() function implementation in python 
    def convert(self, x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    # A function for speed control without feedback(Open loop speed control)
    def speed(self,M):
        pwm = self.convert(abs(M),0, 1000, 0, 1000) 
        #self.p_en.duty(pwm)
        if pwm < self.minpwm:
            self.p_in2.duty(0)
            self.p_in1.duty(0)
        elif M>0:
            self.p_in2.duty(0)
            self.p_in1.duty(pwm)
        else:
            self.p_in1.duty(0)
            self.p_in2.duty(pwm)

# A class for closed loop speed and postion control
class PID:
    
    # Instance variable for this class
    posPrev = 0

    # Constructor for initializing PID values
    def __init__(self, M, kp=1, kd=0, ki=0, umaxIn=800, eprev=0, eintegral=0,
                 max_run_ms=10000, tolerance=10, loop_maxms = 1000, loop_minms=5):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.tolerance = tolerance   # 
        self.M = M                   # Motor object
        self.umaxIn  =umaxIn
        self.eprev = eprev
        self.eintegral = eintegral
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
        self.pid_type = 'init'

    # Function for calculating the Feedback signal. It takes the current value, user target value and the time delta.
    def evalu(self,value, target, deltaT):
        
        # Propotional
        e = target-value
        
        #if abs(e) <= abs(self.tolerance):    # 
        #    return 0

        # Derivative
        dedt = (e-self.eprev)/(deltaT)

        # Integral
        self.eintegral = self.eintegral + e*deltaT
        
        # Control signal
        u = self.kp*e + self.kd*dedt + self.ki*self.eintegral
        
        # Direction and power of  the control signal
        if u > 0:
            if u > self.umaxIn:
                u = self.umaxIn
            else:
                u = u
        else:
            if u < -self.umaxIn:
                u = -self.umaxIn
            else:
                u = u 
        self.eprev = e
        
        self.print_cnt = self.print_cnt + 1
        if self.print_cnt >= 10:
            self.print_cnt = 0
            print('U:', int(u/10), 'T:',int(target), 'V:', int(value))  # for debugging
        return u
    
    
    def setSpeedForPID(self, speed=0):
        self.pid_start_ms_stamp = ticks_ms()
        self.out_time_flags = 0
        self.eintegral = 0
        self.target = speed
        if self.pid_type != 'speed':
            self.loop_stamp_ms = ticks_ms()
            self.pid_type = 'speed'
        
    def setPositionForPID(self, Posi=0):
        self.pid_start_ms_stamp = ticks_ms()
        self.out_time_flags = 0
        self.eintegral = 0
        self.target = Posi
        if self.pid_type != 'position':
            self.loop_stamp_ms = ticks_ms()
            self.pid_type = 'position'
    
        
    
    def speedPIDloop(self):
        if self.pid_type != 'speed':
            return -5
        loop_ms = ticks_ms()
        if loop_ms - self.loop_stamp_ms < self.loop_T_minms:
            return -1
        if loop_ms - self.pid_start_ms_stamp > self.max_pid_run_ms:
            if self.out_time_flags <= 2:
                self.M.speed(0)     # out of time, stop motor
                print('pid run out of time.')
                self.out_time_flags = self.out_time_flags + 1
            return -2
        if self.out_time_flags > 0:
            return -3
        
        deltaT_ms = loop_ms - self.loop_stamp_ms
        self.loop_stamp_ms = loop_ms
        
        state = disable_irq()
        enc_pos = self.M.pos
        per_us = self.M.enc_period_us
        enc_pre_us = self.M.stamp_us
        enable_irq(state)
        
        if (self.loop_pre_pos != enc_pos)and(per_us>10):
            #self.realvalue = (enc_pos - self.loop_pre_pos)*1000000/per_us    # speed in rps
            self.realvalue = 1000000/per_us    # speed in rps
            self.loop_pre_pos = enc_pos
            
            # Call for control signal
            x = int(self.evalu(self.realvalue, self.target, deltaT_ms/1000))
            #print('enc x:',x)
            self.M.speed(x)
            #print(x, self.realvalue, self.target)   # For debugging

        elif (loop_ms-self.M.interrupt_stamp_ms) >= self.loop_T_maxms:
            x = int(self.evalu(0, self.target, self.loop_T_maxms/1000))
            self.M.speed(x)
            #print(x, 0, self.target)   # For debugging
            
        return 0
        
     
    def positionPIDloop(self):
        if self.pid_type != 'position':
            return -5
        
        loop_ms = ticks_ms()
        if loop_ms - self.loop_stamp_ms < self.loop_T_minms:
            return -1
        if loop_ms - self.pid_start_ms_stamp > self.max_pid_run_ms:
            if self.out_time_flags <= 2:
                self.M.speed(0)     # out of time, stop motor
                print('pid run out of time.')
                self.out_time_flags = self.out_time_flags + 1
            return -2
        if self.out_time_flags > 0:
            return -3
        
        deltaT_ms = loop_ms - self.loop_stamp_ms
        self.loop_stamp_ms = loop_ms
        
        state = disable_irq()
        enc_pos = self.M.pos
        per_us = self.M.enc_period_us
        enc_pre_us = self.M.stamp_us
        enable_irq(state)
        
        if (self.loop_pre_pos != enc_pos)and(per_us>10):
            #self.realvalue = 1000000/per_us    # speed in rps
            self.realvalue = enc_pos          # encoder counter as motor position
            self.loop_pre_pos = enc_pos
            
            if abs(self.realvalue-self.target) > abs(self.tolerance):
                # Call for control signal
                x = int(self.evalu(self.realvalue, self.target, deltaT_ms/1000))
            else:
                x = 0
                if self.pid_type != 'init':
                    self.pid_type = 'init'
                    print('U:', x, 'T:',int(self.target), 'V:', int(self.realvalue))
            self.M.speed(x)

        elif (loop_ms-self.M.interrupt_stamp_ms) >= self.loop_T_maxms:
            if abs(self.realvalue-self.target) > abs(self.tolerance):
                # Call for control signal
                x = int(self.evalu(self.realvalue, self.target, deltaT_ms/1000))
            else:
                x = 0
                if self.pid_type != 'init':
                    self.pid_type = 'init'
                    print('U:', x, 'T:',int(self.target), 'V:', int(self.realvalue))
                
            self.M.speed(x)
            
        return 0     


        
    
    # Function for closed loop position control
    def setTarget(self,target):
        
        deltaT = .02

        # Disable the interrupt to read the position of the encoder(encoder tick)               
        state = disable_irq()
        step = self.M.pos
        # Enable the intrrupt after reading the position value
        enable_irq(state)
        

        # Control signal call
        x = int(self.evalu(step, target, deltaT))
        
        # Set the speed 
        self.M.speed(x)
        print(x, step, target) # For debugging
        
        # Constant delay 
        sleep_ms(20)
        
    # Function for closed loop speed control
    def setSpeed(self, target):
        state = disable_irq()
        posi = self.M.pos
        enable_irq(state)

        # Delta is high because small delta causes drastic speed stepping.
        deltaT = .1

        # Target RPM
        vt = target 

        # Current encoder tick rate
        velocity = (posi - self.posPrev)/deltaT
        self.posPrev = posi

        # Converted to RPM
        v = 60*velocity/self.M.encoder_circle_pulse

        # Call for control signal
        x = int(self.evalu(v, vt, deltaT))

        # Set the motor speed
        self.M.speed(x)
        #print(x, v, vt)   # For debugging

        # Constant delay
        sleep_ms(100)

    
if __name__ == '__main__':
    print('Start DCMot_PID test.')
    # Creating objects of each motor
    m1 = Motor(m1=14, m2=27, c1=32, c2=33)
    #m2 = Motor(19, 18, 5, 14, 27)

    # Creating PID objects for each motor
    #p1 = PID(m1, 5, 0.1, 0.001, 800)
    p1 = PID(M=m1, kp=2, kd=0.2, ki=1, umaxIn=900)    # for speed PID para
    #p1 = PID(M=m1, kp=1, kd=0, ki=1, umaxIn=500,tolerance=10)    # for position PID para
    #p2 = PID(m2, 5, 0.1, 0.001, 800)
    
    start_ms = ticks_ms()
    test_step = 0

    
    while(1):
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 3000:
            if test_step ==0:
                test_step = 1
                p1.setSpeedForPID(100)
                #p1.setPositionForPID(100)
        elif run_ms <= 8000:
            if test_step == 1:
                test_step = 2
                p1.setSpeedForPID(50)
                #p1.setPositionForPID(50)
        elif run_ms <= 13000:
            if test_step == 2:
                p1.setSpeedForPID(75)
                #p1.setPositionForPID(80)
                test_step = 3
        if run_ms >= 26000:
            p1.M.speed(0)
            if p1.pid_type == 'position':
                print('U:', 0, 'T:',p1.target, 'V:', p1.realvalue)
                print('U:', 0, 'T:',p1.target, 'V:', p1.realvalue) 
            print('DCMot_PID test time over.')
            break
        
        p1.speedPIDloop()
        #p1.positionPIDloop()
    

