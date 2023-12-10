from time import sleep_ms, ticks_us, ticks_ms
from machine import Pin, PWM, disable_irq, enable_irq, ADC

# A class for functions related to motors
class Servo5line:
    
    def getAdcval(self):
        self.pos_adcval = self.adc.read()
        return self.pos_adcval
        
    def getAnglex10(self):
        adcval = self.getAdcval()
        self.pos_anglex10 = (self.max_angle - self.min_angle)*(adcval-self.zero_adc)/4095
        return self.pos_anglex10
    
    def setZeroAdcVal(self,zeroAdc=2047):
        self.zero_adc = zeroAdc
        
    def calibration(self):
        print('Start 5line servo calibration.')
        print('Please manuly rotate to 0 degree...')
        adcsum = 0
        for i in range(20):
            adcval = self.getAdcval()
            print('0deg Adc val:', adcval)
            if i>=15:
                adcsum = adcsum + adcval
            sleep_ms(500)
        adcv_0 = adcsum//5
        
        adcsum = 0
        print('Please manuly rotate to 90 degree...')
        for i in range(20):
            adcval = self.getAdcval()
            print('90deg Adc val:', adcval)
            if i>=15:
                adcsum = adcsum + adcval
            sleep_ms(500)
        adcv_90 = adcsum//5
        
        adcsum = 0
        print('Please manuly rotate to -90 degree...')
        for i in range(20):
            adcval = self.getAdcval()
            print('-90deg Adc val:', adcval)
            if i>=15:
                adcsum = adcsum + adcval
            sleep_ms(500)
        adcv_n90 = adcsum//5
        
        print('-90deg:',adcv_n90, '  0deg:',adcv_0, '  90deg:',adcv_90)
            

    # Constroctor for initializing the motor pins
    def __init__(self, m1, m2, a1, freq = 1000, minPWM=200, maxPWM=900, maxAngle=600, minAngle=-600):
        self.stamp_us = ticks_us()
        self.interrupt_stamp_ms = 0
        self.pos_adcval = 0
        self.pos_anglex10 = 0
        self.max_angle = maxAngle
        self.min_angle = minAngle
        self.zero_adc = 2047
        self.minpwm = minPWM
        self.maxpwm = maxPWM
        self.adc = ADC(Pin(a1))
        self.freq = freq
        self.p_in1 = PWM(Pin(m1,Pin.OUT), freq=freq, duty=0)
        self.p_in2 = PWM(Pin(m2,Pin.OUT), freq=freq, duty=0)

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
                 max_run_ms=10000, tolerance=10, loop_maxms = 1000, loop_minms=20,
                 eintClrTol=30):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.tolerance = tolerance   # 
        self.eint_clr_tol = eintClrTol
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


    def evalu(self,value, target, deltaT):
        
        # Propotional
        e = target-value
        
        # Derivative
        dedt = (e-self.eprev)/(deltaT)

        # Integral
        if abs(value-target) > self.eint_clr_tol:
            self.eintegral = self.eintegral + e*deltaT
        else:
            self.eintegral = 0
        
        # Control signal
        u = self.kp*e + self.kd*dedt + self.ki*self.eintegral
        
            
        
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
            print('U:', int(u), 'T:',int(target), 'V:', int(value))  # for debugging
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
        if Posi > self.M.max_angle:
            self.target = self.M.max_angle
        elif Posi < self.M.min_angle:
            self.target = self.M.min_angle
        else:
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
        
        #state = disable_irq()
        posi = self.M.getAnglex10()
        #enable_irq(state)
        
        if self.loop_pre_pos != posi:
            self.realvalue = posi          # angle value x10
            self.loop_pre_pos = posi
            
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
    print('Start servo_5line_pid test.')

    m1 = Servo5line(m1=22, m2=23, a1=32)
    #m2 = Motor(19, 18, 5, 14, 27)

    #p1 = PID(M=m1, kp=20, kd=0.2, ki=180, umaxIn=900)    # for speed PID para
    p1 = PID(M=m1, kp=3, kd=0, ki=10, umaxIn=450,tolerance=10)    # for position PID para
    #p2 = PID(m2, 5, 0.1, 0.001, 800)
    
    start_ms = ticks_ms()
    test_step = 0

    
    while(1):
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 3000:
            if test_step ==0:
                test_step = 1
                #p1.setSpeedForPID(100)
                p1.setPositionForPID(500)
        elif run_ms <= 9000:
            if test_step == 1:
                test_step = 2
                #p1.setSpeedForPID(50)
                p1.setPositionForPID(0)
        elif run_ms <= 18000:
            if test_step == 2:
                #p1.setSpeedForPID(75)
                p1.setPositionForPID(-500)
                test_step = 3
        elif run_ms <= 27000:
            if test_step == 3:
                #p1.setSpeedForPID(75)
                p1.setPositionForPID(0)
                test_step = 4
        if run_ms >= 36000:
            p1.M.speed(0)
            if p1.pid_type == 'position':
                print('U:', 0, 'T:',p1.target, 'V:', p1.realvalue)
                print('U:', 0, 'T:',p1.target, 'V:', p1.realvalue) 
            print('DCMot_PID test time over.')
            break
        #p1.setTarget(240)
        #p1.setSpeed(80)
        #p2.setTarget(-1000)
        
        #p1.speedPIDloop()
        p1.positionPIDloop()
    


