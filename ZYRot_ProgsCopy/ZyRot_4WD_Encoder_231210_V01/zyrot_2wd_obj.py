import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
from machine import Timer, Pin

class ZYRot_2WD_obj():
    
    def ZYRot_2WD_Cb(self,t):
        if self.control_mode == 'position':
            self.PositionLoop()
        elif self.control_mode == 'speed':
            self.SpeedLoop()
        elif self.control_mode == 'stop':
            #self.time0.deinit()
            pass
        else:
            self.control_mode = 'stop'
            self.time0.deinit()
            print('control_mode error!')
    
    
    def __init__(self, wheel_d = 40):
        self.led_p5_r = Pin(5, Pin.OUT, value=0)
        self.led_p18_g = Pin(18, Pin.OUT, value=0)
        self.led_p19_r = Pin(19, Pin.OUT, value=0)
        self.led_p21_g = Pin(21, Pin.OUT, value=0)
        
        self.m1r = motor.Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26, max_pwm_step=100)  #front right wheel
        self.m1l = motor.Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32, max_pwm_step=100)  #front left wheel

        self.pid1R = motor.PID(M=self.m1r, kp=0.1, kd=-2, ki=0.05, umaxIn=900, tolerance=5,
                 max_interItem=200,dbg_info=0)
        self.pid1L = motor.PID(M=self.m1l, kp=0.1, kd=-2, ki=0.05, umaxIn=900, tolerance=5,
                 max_interItem=200,dbg_info=0)
                
  
        self.m1rSetPos = 0.0
        self.m1lSetPos = 0.0
        
        self.m1rSetSpeed = 0.0
        self.m1lSetSpeed = 0.0
        
        self.mknmCurX = 0.0
        self.mknmCurY = 0.0
        self.mknmCurDirArc = 0.0
        self.mknmSetX = 0.0
        self.mknmSetY = 0.0
        self.mknmSetDirArc = 0.0
        
        self.wheelD = wheel_d
        self.wheel_lrDis = 95
       
        self.control_mode = 'position'
        self.time0 = Timer(0)
        self.time0.init(period=25,mode=Timer.PERIODIC,callback=self.ZYRot_2WD_Cb)
        
    def setMotPwm(self, pwmr=0,pwml=0):
        self.m1r.setPWMduty(pwmr)
        self.m1l.setPWMduty(pwml)

    def setMotSpeed(self,speed_1r=0,speed_1l=0):
        self.m1rSetSpeed = speed_1r
        self.m1lSetSpeed = speed_1l

        self.pid1R.setSpeedForPID(speed_1r)
        self.pid1L.setSpeedForPID(speed_1l)
        
        self.control_mode = 'speed'
        
    def getMotSpeed(self):
        spe_1r = 0
        spe_1l = 0
        return spe_1r,spe1l
    
    def getMotPos(self):
        pos_1r = int(self.pid1R.M.pos*self.pid1R.M.k_pos_mm)
        pos_1l = int(self.pid1L.M.pos*self.pid1R.M.k_pos_mm)
        return pos_1r,pos_1l
        
        
    def setMotPos(self,pos1r=0,pos1l=0):
        self.m1rSetPos = pos1r
        self.m1lSetPos = pos1l
        self.pid1R.setPositionForPID(pos1r)
        self.pid1L.setPositionForPID(pos1l)
        self.control_mode = 'position'
  

    def set_dPos(self,dy=0.0):
        
        self.m1rSetPos += dy
        self.m1lSetPos += dy
        
        self.pid1R.setPositionForPID(self.m1rSetPos)
        self.pid1L.setPositionForPID(self.m1lSetPos)
        
        self.control_mode = 'position'
        
    def set_dDirArc(self, dDirArc=0.0):
        self.mknmSetDirArc += dDirArc
        
        dwheelR = dDirArc*self.wheel_lrDis
        dwheelL = -dwheelR
        
        self.m1rSetPos += dwheelR
        self.m1lSetPos += dwheelL
        
        self.pid1R.setPositionForPID(self.m1rSetPos)
        self.pid1L.setPositionForPID(self.m1lSetPos)
        
        self.control_mode = 'position'
        
    def setSpeed(self,vY=0.0,vW=0.0):
        voma = vW * self.wheel_lrDis
        self.m1rSetSpeed = vY + voma   
        self.m1lSetSpeed = vY - voma
        
        self.pid1R.setSpeedForPID(self.m1rSetSpeed)
        self.pid1L.setSpeedForPID(self.m1lSetSpeed)
        
        self.control_mode = 'speed'
    
        
    def SpeedLoop(self):
        self.pid1R.speedPIDloop()
        self.pid1L.speedPIDloop()
        
        
    def PositionLoop(self):
        self.pid1R.positionPIDloop()
        self.pid1L.positionPIDloop()
        
    def release_all_motor(self):
        self.pid1R.release_pid_motor()
        self.pid1L.release_pid_motor()
        
    
    
def ZYRot_2WD_PositionTest(N=10):
    print('Start zyrot_2wd_obj ZYRot_2WD_PositionTest...')
    
    zy2wd = ZYRot_2WD_obj()
    
    start_ms = ticks_ms()
    test_step = 0
    #while (1):
    while test_step < 20:
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                zy2wd.set_dPos(100)
        elif run_ms <= 3000:
            if test_step == 1:
                test_step = 2
                #mini_mknm.setMotPos(400,0,0,400)
                zy2wd.set_dPos(50)
        elif run_ms <= 4000:
            if test_step == 2:
                #mini_mknm.setMotPos(50,50,50,50)
                zy2wd.set_dPos(-100)
                test_step = 3
        elif run_ms <= 5000:
            if test_step == 3:
                #mini_mknm.setMotPos(300,300,300,300)
                zy2wd.set_dPos(-50)
                test_step = 4
        elif run_ms <= 6000:
            if test_step == 4:
                #mini_mknm.setMotPos(-100,-100,-100,-100)
                zy2wd.set_dDirArc(3.1416/2)
                test_step = 5
        elif run_ms <= 7000:
            if test_step == 5:
                #mini_mknm.setMotPos(100,100,100,100)
                zy2wd.set_dDirArc(-3.1416/2)
                test_step = 6 
        elif run_ms <= 8000:
            if test_step == 6:
                #zy2wd.setMotPos(0,0)
                test_step = 7
        elif run_ms <= 9000:
            if test_step == 7:
                zy2wd.setMotPos(0,0)
                test_step = 8
                start_ms = ticks_ms()
                test_step = 0
        elif run_ms <= 10000:
            if test_step == 8:
                zy2wd.setMotPos(0,0)
                test_step = 9
        elif run_ms <= 11000:
            if test_step == 9:
                zy2wd.setMotPos(0,0)
                test_step = 10
        if run_ms >= 12000:
            zy2wd.setMotPos(0,0)
            print('zy2wd test over.')
            test_step = 100
            
def ZYRot_2WD_SpeedTest(N=10):
    print('Start ZYRot_2WD_SpeedTest...')
    
    zy2wd = ZYRot_2WD_obj()
    
    start_ms = ticks_ms()
    test_step = 0
    while test_step < 20:
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                zy2wd.setSpeed(200,0)
        elif run_ms <= 3000:
            if test_step == 1:
                test_step = 2
                zy2wd.setSpeed(0,0)
        elif run_ms <= 4000:
            if test_step == 2:
                zy2wd.setSpeed(-200,0)
                test_step = 3
        elif run_ms <= 5000:
            if test_step == 3:
                zy2wd.setSpeed(0,0.2)
                test_step = 4
        elif run_ms <= 6000:
            if test_step == 4:
                zy2wd.setSpeed(0,0)
                test_step = 5
        elif run_ms <= 7000:
            if test_step == 5:
                zy2wd.setSpeed(0,0)
                test_step = 6 
        elif run_ms <= 8000:
            if test_step == 6:
                test_step = 7
        elif run_ms <= 9000:
            if test_step == 7:
                zy2wd.setSpeed(0,0)
                test_step = 8
#                 start_ms = ticks_ms()
#                 test_step = 0
        elif run_ms <= 10000:
            if test_step == 8:
                zy2wd.setMotPos(0,0)
                test_step = 9
        elif run_ms <= 11000:
            if test_step == 9:
                zy2wd.setMotPos(0,0)
                test_step = 10
        if run_ms >= 12000:
            zy2wd.setMotPos(0,0)
            print('zy2wd test over.')
            test_step = 100

def ZYRot_2WD_mot_spe_test(N = 10, vl = 300, vr = 300):
    print('Start ZYRot_2WD_obj.py zy4wd_mot_spe_test()...')
    zy2wd = ZYRot_2WD_obj()
        
    for i in range(N):
        print('zy2wd_mot_spe_test N,',i)

        sleep_ms(100)
        zy2wd.setSpeed(vY=0,vW=1)
        sleep_ms(1000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        zy2wd.setSpeed(vY=0,vW=-1)
        sleep_ms(1000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        zy2wd.setSpeed(vY=200,vW=0)
        sleep_ms(1000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        zy2wd.setSpeed(vY=-200,vW=0)
        sleep_ms(1000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        zy2wd.setSpeed(vY=200,vW=2)
        sleep_ms(2000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        zy2wd.setSpeed(vY=-200,vW=-2)
        sleep_ms(2000)
        zy2wd.setSpeed(vY=0,vW=0)
        sleep_ms(500)
        
    sleep_ms(2000)

        
   
if __name__ == '__main__':
    ZYRot_2WD_mot_spe_test()
    #ZYRot_2WD_PositionTest()
    #ZYRot_2WD_SpeedTest()








