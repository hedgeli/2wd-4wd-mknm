
from machine import Pin, ADC, PWM
import time
#import math

DIR_F = 1
DIR_B = 2 
DIR_NO_INIT = 0 

DUTY_MAX = 1000    # 1023
DUTY_MIN = 50
DELTA_ERR_THRESHOLD = 1    #1.5
INTER_ERR_THRESHOLD = 5

DUTY_INTEGRATE_MAX = 600
DUTY_INTERGATE_MIN = 60

MOTOR_PWM_FREQ = 200

MOVE_TO_ANGLE_MAX_CYCLES = 200

UPDATE_POS_MAX_MS  = 1500

CTL_MODE_POSITION = 3
CTL_MODE_SPEED = 2
CTL_MODE_PWM  = 1


class servo_mot_5line():
    def __init__(self, adc_pin_no, pin1_no, pin2_no, name = 'Mot_XX_5line'):
        self.name = name
        self.adc_pin_no = adc_pin_no
        self.pin1_no = pin1_no
        self.pin2_no = pin2_no
        self.pinf_no = pin1_no
        self.pinb_no = pin2_no
        self.pwmf = PWM(Pin(self.pinf_no), freq = MOTOR_PWM_FREQ, duty = 0)
        self.pwmb = PWM(Pin(self.pinb_no), freq = MOTOR_PWM_FREQ, duty = 0)
        self.pwmf.deinit()
        self.pwmb.deinit()
        self.adc = ADC(Pin(adc_pin_no))
        self.pin1 = Pin(pin1_no, Pin.OUT)
        self.pin2 = Pin(pin2_no, Pin.OUT)
        self.pin1.off()
        self.pin2.off()
        self.adc.atten(ADC.ATTN_11DB)
        self.adcval = self.adc.read()
        self.ang_zero_val = 2047
        self.deg_per_val = 4095 / 333
        self.angle = (self.adcval-self.ang_zero_val)/self.deg_per_val
        self.dir = DIR_NO_INIT
        
        self.ctl_mode = CTL_MODE_POSITION
        
        self.set_angle = 0
        self.set_spe = 0     # degree/second
        self.Kp = 10
        self.Ki = 0.5
        self.Kd = 5
        
        self.pid_duty = 0
        self.integral_duty = 0
        self.err = 0
        self.err_prev = 0
        self.delta_err = 0
        self.delta_duty = 0
        self.real_duty = 0
        self.real_spe = 0
        
        self.tolerance_angle = 1
        
        self.tick_ms = 20
        
        self.update_pos_cnt = 0
        self.set_pos_stamp_ms = 0
        self.in_set_pos_cnt = 0
        self.set_pos_flag = 0
        self.max_update_pos_ms = 0
        
        self.calibrate_direction()
        
        
    def calibrate_direction(self):
        self.refresh_vals()
        angle_old = self.angle
        self.pin1 = Pin(self.pin1_no, Pin.OUT)
        self.pin2 = Pin(self.pin2_no, Pin.OUT)
        self.pin1.off()
        self.pin2.off()

        self.pwm1 = PWM(self.pin1,freq=1000,duty=750)
#         time.sleep_ms(150)
        for i in range(20):
            self.refresh_vals()
            if abs(self.angle - angle_old) >= 5:
                break
            time.sleep_ms(10)
            
        
        self.pwm1.deinit()
        self.pin1 = Pin(self.pin1_no, Pin.OUT)
        self.pin2 = Pin(self.pin2_no, Pin.OUT)
        self.pin1.off()
        self.pin2.off()
        self.refresh_vals()
        if(self.angle - angle_old >= 5):
            self.dir = DIR_F
            self.pinf_no = self.pin1_no
            self.pinb_no = self.pin2_no
        elif(self.angle - angle_old <= -5):
            self.dir = DIR_B
            self.pinf_no = self.pin2_no
            self.pinb_no = self.pin1_no
        else:
            self.dir = DIR_NO_INIT
            print('Moved angle:',self.angle - angle_old)
            print(self.name, 'calibrate_direction() failed!')
#         print(self.name, ' dir:', self.dir)
        
        
    def set_position(self, set_angle, max_time_ms = 1500):
        if(set_angle > 120):
            set_angle = 120
            print('set angle should <= 120 degree')
        elif(set_angle < -120):
            set_angle = -120
            print('set angle should >= -120 degree')
            
        self.set_angle = set_angle
        self.set_pos_stamp_ms = time.ticks_ms()
        self.in_set_pos_cnt = 0
        self.set_pos_flag = 1
        self.max_update_pos_ms = max_time_ms
        
        self.integral_duty = 0
        self.delta_duty = 0
        
        
        
    def update_position(self):
        if(self.dir == DIR_NO_INIT):
#             print(self.name, "direction not inited, can't update_position()")
            return
    
        if(self.set_pos_flag == 0):
            return
        
        
        time_ms = time.ticks_ms()
        if(time_ms - self.set_pos_stamp_ms > self.max_update_pos_ms):
            self.pwmf.deinit()
            self.pwmb.deinit()
            self.pin1 = Pin(self.pin1_no, Pin.OUT)
            self.pin2 = Pin(self.pin2_no, Pin.OUT)
            self.pin1.off()
            self.pin2.off()
            self.integral_duty = 0
            self.set_pos_flag = 0    
            print(self.name, 'Time out', self.max_update_pos_ms, "ms. update_position()")
            return
            
                    
#         self.set_angle = new_angle
#         self.self.in_set_pos_cnt = 0
#         for i in range(MOVE_TO_ANGLE_MAX_CYCLES):
        self.refresh_vals()
        err_angle = self.set_angle - self.angle
        self.delta_err = err_angle - self.err
        self.err = err_angle
        
        
        if(abs(err_angle) <= self.tolerance_angle):      
            #print('abs(err_angle) <= self.tolerance_angle')
            self.in_set_pos_cnt = self.in_set_pos_cnt + 1
            self.integral_duty = 0
            if(self.in_set_pos_cnt >= 3):
#                     print(self.name, 'set angle:', self.set_angle, 'real angle:', self.angle,
#                           'err:', self.angle - self.set_angle)
                self.set_pos_flag = 0    
                self.pwmf.deinit()
                self.pwmb.deinit()
                self.pin1 = Pin(self.pin1_no, Pin.OUT)
                self.pin2 = Pin(self.pin2_no, Pin.OUT)
                self.pin1.off()
                self.pin2.off()
                self.integral_duty = 0
                return
            
        else:
            self.in_set_pos_cnt = 0
        
        if(self.err > 0):
            if((self.delta_err < -DELTA_ERR_THRESHOLD) and (self.err < INTER_ERR_THRESHOLD)):
                self.integral_duty = DUTY_INTERGATE_MIN 
            else:
                self.integral_duty = self.integral_duty + self.Ki * err_angle
        elif(self.err < 0):
            if((self.delta_err > DELTA_ERR_THRESHOLD) and (self.err > -INTER_ERR_THRESHOLD)):
                self.integral_duty =  DUTY_INTERGATE_MIN
            else:
                self.integral_duty = self.integral_duty + self.Ki * err_angle
            
        if(self.integral_duty > DUTY_INTEGRATE_MAX):
            self.integral_duty = DUTY_INTEGRATE_MAX
        elif(self.integral_duty <- DUTY_INTEGRATE_MAX):
            self.integral_duty = -DUTY_INTEGRATE_MAX
            
        self.delta_duty = self.delta_err * self.Kd 
            
        self.pid_duty = self.Kp * err_angle + self.integral_duty + self.delta_duty
        
        if(self.pid_duty > DUTY_MAX):
            self.pid_duty = DUTY_MAX
        elif(self.pid_duty < -DUTY_MAX):
            self.pid_duty = -DUTY_MAX
        elif((self.pid_duty < DUTY_MIN) and (self.pid_duty >= 0)):
            self.pid_duty = DUTY_MIN
        elif((self.pid_duty > -DUTY_MIN) and (self.pid_duty < 0)):
            self.pid_duty = -DUTY_MIN
            
        if(self.pid_duty >= 0):
            self.pinb = Pin(self.pinb_no)
            self.pinb.off()
            self.pwmf=PWM(Pin(self.pinf_no),freq=MOTOR_PWM_FREQ, duty = int(self.pid_duty))
#             time.sleep_ms(10)
        
        elif(self.pid_duty < 0):
            self.pinf = Pin(self.pinf_no)
            self.pinf.off()
            self.pwmb=PWM(Pin(self.pinb_no),freq=MOTOR_PWM_FREQ, duty = int(-self.pid_duty))
#             time.sleep_ms(10)
        
        
        
            
    def move_to_angle(self, new_angle):
        #self.refresh_vals()
        #angle_old = self.angle
        if(self.dir == DIR_NO_INIT):
            print(self.name, "direction not init ok, can't move_to_angle()")
            return
        
        if(new_angle > 120):
            new_angle = 120
        elif(new_angle < -120):
            new_angle = -120
            
        self.set_angle = new_angle
        angle_reach_cnt = 0
        for i in range(MOVE_TO_ANGLE_MAX_CYCLES):
            self.refresh_vals()
            err_angle = new_angle - self.angle
            self.delta_err = err_angle - self.err
            self.err = err_angle
            
            
            if(i >= MOVE_TO_ANGLE_MAX_CYCLES-1):
                self.pwmf.deinit()
                self.pwmb.deinit()
                self.pin1 = Pin(self.pin1_no, Pin.OUT)
                self.pin2 = Pin(self.pin2_no, Pin.OUT)
                self.pin1.off()
                self.pin2.off()
                self.integral_duty = 0
#                 print(self.name, 'move_to_angle() Time out!')
#                 print('err_angle:', err_angle)
                break
            if(abs(err_angle) <= self.tolerance_angle):      
                #print('abs(err_angle) <= self.tolerance_angle')
                angle_reach_cnt = angle_reach_cnt + 1
                self.integral_duty = 0
                if(angle_reach_cnt >= 3):
                    #print('abs(err_angle) <= self.tolerance_angle')
#                     print(self.name, 'set angle:', self.set_angle, 'real angle:', self.angle,
#                           'err:', self.angle - self.set_angle)
                    self.pwmf.deinit()
                    self.pwmb.deinit()
                    self.pin1 = Pin(self.pin1_no, Pin.OUT)
                    self.pin2 = Pin(self.pin2_no, Pin.OUT)
                    self.pin1.off()
                    self.pin2.off()
                    self.integral_duty = 0
                    break
                
            else:
                angle_reach_cnt = 0
            
            #abs_err = abs(err_angle)
            #self.integral_duty = self.integral_duty + self.Ki * err_angle
            if(self.err > 0):
                if((self.delta_err < -DELTA_ERR_THRESHOLD) and (self.err < INTER_ERR_THRESHOLD)):
                    self.integral_duty = DUTY_INTERGATE_MIN    #self.integral_duty
                    #pass
                else:
                    self.integral_duty = self.integral_duty + self.Ki * err_angle
            elif(self.err < 0):
                if((self.delta_err > DELTA_ERR_THRESHOLD) and (self.err > -INTER_ERR_THRESHOLD)):
                    self.integral_duty =  DUTY_INTERGATE_MIN    #self.integral_duty
                    #pass
                else:
                    self.integral_duty = self.integral_duty + self.Ki * err_angle
                
            if(self.integral_duty > DUTY_INTEGRATE_MAX):
                self.integral_duty = DUTY_INTEGRATE_MAX
            elif(self.integral_duty <- DUTY_INTEGRATE_MAX):
                self.integral_duty = -DUTY_INTEGRATE_MAX
                
            self.delta_duty = self.delta_err * self.Kd 
                
            self.pid_duty = self.Kp * err_angle + self.integral_duty + self.delta_duty
            #print('err_angle:',int(err_angle),'pid_duty:', int(self.pid_duty), 'int_duty:', int(self.integral_duty))
            
            if(self.pid_duty > DUTY_MAX):
                self.pid_duty = DUTY_MAX
            elif(self.pid_duty < -DUTY_MAX):
                self.pid_duty = -DUTY_MAX
            elif((self.pid_duty < DUTY_MIN) and (self.pid_duty >= 0)):
                self.pid_duty = DUTY_MIN
            elif((self.pid_duty > -DUTY_MIN) and (self.pid_duty < 0)):
                self.pid_duty = -DUTY_MIN
                
            if(self.pid_duty >= 0):
                self.pinb = Pin(self.pinb_no)
                self.pinb.off()
                self.pwmf=PWM(Pin(self.pinf_no),freq=MOTOR_PWM_FREQ, duty = int(self.pid_duty))
                time.sleep_ms(10)
            
            elif(self.pid_duty < 0):
                self.pinf = Pin(self.pinf_no)
                self.pinf.off()
                self.pwmb=PWM(Pin(self.pinb_no),freq=MOTOR_PWM_FREQ, duty = int(-self.pid_duty))
                time.sleep_ms(10)
           
        
        
        
    def refresh_vals(self):
        self.adcval = self.adc.read()
        self.angle = (self.adcval-self.ang_zero_val)/self.deg_per_val
        
    def get_adcval(self):
        self.adcval=self.adc.read()
        return self.adcval
    
    def get_angle(self):
        self.adcval=self.adc.read()
        self.angle = (self.adcval-self.ang_zero_val)/self.deg_per_val
        return self.angle
    
    
    
def servo_mot_5line_test():
    mot4 = servo_mot_5line(adc_pin_no=33,pin1_no=27,pin2_no=14, name='MotLeft')
    mot4.refresh_vals()
    #print('mot4 angle:', mot4.get_angle())
    mot5 = servo_mot_5line(adc_pin_no=32,pin1_no=13,pin2_no=12, name='MotRight')
    mot5.refresh_vals()
#     #print('mot5 angle:', mot5.get_angle())
#     #print('mot4 dir', mot4.dir)
#     #print('mot5 dir', mot5.dir)
    mot4.calibrate_direction()
    mot5.calibrate_direction()
#     print('mot4 dir', mot4.dir)
#     print('mot5 dir', mot5.dir)
    
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    mot4.move_to_angle(0)
    time.sleep_ms(200)
#     print('---------------------------------')
    mot5.move_to_angle(0)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    print(mot4.name, int(mot4.get_angle()),mot5.name, int(mot5.get_angle()))
    time.sleep_ms(20)
    
    time.sleep_ms(2000)
    for i in range(40):
        time.sleep_ms(250)
        print(mot4.name, int(mot4.get_angle()), int(mot4.set_angle), '---', mot5.name, int(mot5.get_angle()), int(mot5.set_angle))
        mot4.move_to_angle((i-20)*5)
        time.sleep_ms(50)
        mot5.move_to_angle((i-20)*5)
        time.sleep_ms(50)
     
    for i in range(10):
        print(mot4.name, int(mot4.get_angle()), int(mot4.set_angle), '---', mot5.name, int(mot5.get_angle()), int(mot5.set_angle))
        time.sleep_ms(50)
      
    print('motor test finished.')
    
    
if __name__ == '__main__':
    servo_mot_5line_test() 


