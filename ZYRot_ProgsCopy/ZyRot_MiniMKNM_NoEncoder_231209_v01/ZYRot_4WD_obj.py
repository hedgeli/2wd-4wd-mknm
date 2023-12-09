import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
from machine import Timer

class ZYRot_4WD_obj():
    
    def ZYRot_4WD_Cb(self,t):
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
        
        m2l = motor.Motor_ABEncoder(m1=5, m2=18, c1=17, c2=16, max_pwm_step=100)    #后左轮
        m2r = motor.Motor_ABEncoder(m1=21, m2=19, c1=23, c2=22, max_pwm_step=100)   #后右轮
        
        m1r = motor.Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26, max_pwm_step=100)  #前右轮
        m1l = motor.Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32, max_pwm_step=100)  #前左轮
        
        p2r = motor.PID(M=m2r, kp=0.8, kd=0, ki=0.8, umaxIn=900, tolerance=5,
                 max_interItem=300,dbg_info=0)
        p2l = motor.PID(M=m2l, kp=0.8, kd=0, ki=0.8, umaxIn=900, tolerance=5,
                 max_interItem=300,dbg_info=0)
        p1r = motor.PID(M=m1r, kp=0.8, kd=0, ki=0.8, umaxIn=900, tolerance=5,
                 max_interItem=300,dbg_info=0)
        p1l = motor.PID(M=m1l, kp=0.8, kd=0, ki=0.8, umaxIn=900, tolerance=5,
                 max_interItem=300,dbg_info=0)
                
        self.pid1R = p1r
        self.pid1L = p1l
        self.pid2R = p2r
        self.pid2L = p2l
        
        self.m1rSetPos = 0.0
        self.m1lSetPos = 0.0
        self.m2rSetPos = 0.0
        self.m2lSetPos = 0.0
        
        self.m1rSetSpeed = 0.0
        self.m1lSetSpeed = 0.0
        self.m2rSetSpeed = 0.0
        self.m2lSetSpeed = 0.0
        
        self.mknmCurX = 0.0
        self.mknmCurY = 0.0
        self.mknmCurDirArc = 0.0
        self.mknmSetX = 0.0
        self.mknmSetY = 0.0
        self.mknmSetDirArc = 0.0
        
        self.wheelD = wheel_d
        self.wheel_lrDis = 105
        self.wheel_llDis = 70
        #self.wheel_Ori_dis = 87.5   #63.1   #sqrt((lrDis/2)^2+(llDis/2)^2)
        
        self.control_mode = 'position'
        self.time0 = Timer(0)
        self.time0.init(period=25,mode=Timer.PERIODIC,callback=self.ZYRot_4WD_Cb)
        
        
    def setMotSpeed(self,speed_1r=0,speed_1l=0,speed_2r=0,speed_2l=0):
        self.m1rSetSpeed = speed_1r
        self.m1lSetSpeed = speed_1l
        self.m2rSetSpeed = speed_2r
        self.m2lSetSpeed = speed_2l
        self.pid1R.setSpeedForPID(speed_1r)
        self.pid1L.setSpeedForPID(speed_1l)
        self.pid2R.setSpeedForPID(speed_2r)
        self.pid2L.setSpeedForPID(speed_2l)
        
        self.control_mode = 'speed'
        
    def getMotSpeed(self):
        spe_1r = 0
        spe_1l = 0
        spe_2r = 0 
        spe_2l = 0
        return spe_1r,spe1l,spe2r,spe2l
    
    def getMotPos(self):
        pos_1r = int(self.pid1R.M.pos*self.pid1R.M.k_pos_mm)
        pos_1l = int(self.pid1L.M.pos*self.pid1R.M.k_pos_mm)
        pos_2r = int(self.pid2R.M.pos*self.pid1R.M.k_pos_mm)
        pos_2l = int(self.pid2L.M.pos*self.pid1R.M.k_pos_mm)
        return pos_1r,pos_1l,pos_2r,pos_2l
        
        
    def setMotPos(self,pos1r=0,pos1l=0,pos2r=0,pos2l=0):
        self.m1rSetPos = pos1r
        self.m1lSetPos = pos1l
        self.m2rSetPos = pos2r
        self.m2lSetPos = pos2l
        self.pid1R.setPositionForPID(pos1r)
        self.pid1L.setPositionForPID(pos1l)
        self.pid2R.setPositionForPID(pos2r)
        self.pid2L.setPositionForPID(pos2l)
        self.control_mode = 'position'
  
    '''
    def set_dPos(self,dX=0.0,dY=0.0):
        self.mknmSetX += dX
        self.mknmSetY += dY
        dm1r = dX + dY
        dm1l = dX - dY
        dm2r = dX - dY
        dm2l = dX + dY
        
        self.m1rSetPos += dm1r
        self.m1lSetPos += dm1l
        self.m2rSetPos += dm2r
        self.m2lSetPos += dm2l
        
        self.pid1R.setPositionForPID(self.m1rSetPos)
        self.pid1L.setPositionForPID(self.m1lSetPos)
        self.pid2R.setPositionForPID(self.m2rSetPos)
        self.pid2L.setPositionForPID(self.m2lSetPos)
        
        self.control_mode = 'position'
        
    def set_dDirArc(self, dDirArc=0.0):
        self.mknmSetDirArc += dDirArc
        
        dwheelR = dDirArc*self.wheel_Ori_dis
        dwheelL = -dwheelR
        
        self.m1rSetPos += dwheelR
        self.m1lSetPos += dwheelL
        self.m2rSetPos += dwheelR
        self.m2lSetPos += dwheelL
        
        self.pid1R.setPositionForPID(self.m1rSetPos)
        self.pid1L.setPositionForPID(self.m1lSetPos)
        self.pid2R.setPositionForPID(self.m2rSetPos)
        self.pid2L.setPositionForPID(self.m2lSetPos)
        
        self.control_mode = 'position'
        
    def setSpeed(self,vX=0.0,vY=0.0,vW=0.0):
        voma = vW * self.wheel_Ori_dis
        self.m1rSetSpeed = vX + vY + voma
        self.m1lSetSpeed = vX - vY - voma
        self.m2rSetSpeed = vX - vY + voma
        self.m2lSetSpeed = vX + vY - voma
        
        self.pid1R.setSpeedForPID(self.m1rSetSpeed)
        self.pid1L.setSpeedForPID(self.m1lSetSpeed)
        self.pid2R.setSpeedForPID(self.m2rSetSpeed)
        self.pid2L.setSpeedForPID(self.m2lSetSpeed)
        
        self.control_mode = 'speed'
    '''        
        
    def SpeedLoop(self):
        self.pid1R.speedPIDloop()
        self.pid1L.speedPIDloop()
        self.pid2R.speedPIDloop()
        self.pid2L.speedPIDloop()
        
        
    def PositionLoop(self):
        self.pid1R.positionPIDloop()
        self.pid1L.positionPIDloop()
        self.pid2R.positionPIDloop()
        self.pid2L.positionPIDloop()
        
    def release_all_motor(self):
        self.pid1R.release_pid_motor()
        self.pid1L.release_pid_motor()
        self.pid2R.release_pid_motor()
        self.pid2L.release_pid_motor()
        
    
'''    
def ZYRot_4WD_PositionTest(N=10):
    print('Start miniMknm_obj miniMknmPositionTest...')
    
    zy4wd = MiniMknm_obj()
    
    start_ms = ticks_ms()
    test_step = 0
    #while (1):
    while test_step < 20:
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                #mini_mknm.setMotPos(200,200,200,200)
                mini_mknm.setMknmDPos(200,0)
        elif run_ms <= 3000:
            if test_step == 1:
                test_step = 2
                #mini_mknm.setMotPos(400,0,0,400)
                mini_mknm.setMknmDPos(0,200)
        elif run_ms <= 4000:
            if test_step == 2:
                #mini_mknm.setMotPos(50,50,50,50)
                mini_mknm.setMknmDPos(-200,0)
                test_step = 3
        elif run_ms <= 5000:
            if test_step == 3:
                #mini_mknm.setMotPos(300,300,300,300)
                mini_mknm.setMknmDPos(0,-200)
                test_step = 4
        elif run_ms <= 6000:
            if test_step == 4:
                #mini_mknm.setMotPos(-100,-100,-100,-100)
                mini_mknm.setMknm_dDirArc(3.1416/2)
                test_step = 5
        elif run_ms <= 7000:
            if test_step == 5:
                #mini_mknm.setMotPos(100,100,100,100)
                mini_mknm.setMknm_dDirArc(-3.1416/2)
                test_step = 6 
        elif run_ms <= 8000:
            if test_step == 6:
                #mini_mknm.setMotPos(0,0,0,0)
                test_step = 7
        elif run_ms <= 9000:
            if test_step == 7:
                mini_mknm.setMotPos(0,0,0,0)
                test_step = 8
                start_ms = ticks_ms()
                test_step = 0
        elif run_ms <= 10000:
            if test_step == 8:
                mini_mknm.setMotPos(0,0,0,0)
                test_step = 9
        elif run_ms <= 11000:
            if test_step == 9:
                mini_mknm.setMotPos(0,0,0,0)
                test_step = 10
        if run_ms >= 12000:
            mini_mknm.setMotPos(0,0,0,0)
            print('MiniMknm test over.')
            test_step = 100
            
def ZYRot_4WD_SpeedTest(N=10):
    print('Start miniMknm_obj miniMknmSpeedTest...')
    
    mini_mknm = MiniMknm_obj()
    
    start_ms = ticks_ms()
    test_step = 0
    #while (1):
    while test_step < 20:
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 2000:
            if test_step ==0:
                test_step = 1
                mini_mknm.setMknmSpeed(20,0,0)
        elif run_ms <= 3000:
            if test_step == 1:
                test_step = 2
                mini_mknm.setMknmSpeed(0,0,0)
        elif run_ms <= 4000:
            if test_step == 2:
                mini_mknm.setMknmSpeed(0,0,1)
                test_step = 3
        elif run_ms <= 5000:
            if test_step == 3:
                mini_mknm.setMknmSpeed(0,30,0)
                test_step = 4
        elif run_ms <= 6000:
            if test_step == 4:
                mini_mknm.setMknmSpeed(10,10,0)
                test_step = 5
        elif run_ms <= 7000:
            if test_step == 5:
                mini_mknm.setMknmSpeed(0,0,0)
                test_step = 6 
        elif run_ms <= 8000:
            if test_step == 6:
                test_step = 7
        elif run_ms <= 9000:
            if test_step == 7:
                mini_mknm.setMknmSpeed(0,0,0)
                test_step = 8
                start_ms = ticks_ms()
                test_step = 0
        elif run_ms <= 10000:
            if test_step == 8:
                mini_mknm.setMotPos(0,0,0,0)
                test_step = 9
        elif run_ms <= 11000:
            if test_step == 9:
                mini_mknm.setMotPos(0,0,0,0)
                test_step = 10
        if run_ms >= 12000:
            mini_mknm.setMotPos(0,0,0,0)
            print('MiniMknm test over.')
            test_step = 100
'''

def zy4wd_mot_spe_test(N = 6, vl = 300, vr = 300):
    print('Start ZYRot_4WD_obj.py zy4wd_mot_spe_test()...')
    zy4wd = ZYRot_4WD_obj()
#     for i in range(N):
#         zy4wd.setMotSpeed(vr,vl,vr,vl)
#         sleep_ms(100)
#         print('F N,',i)
        
    for i in range(N):
        zy4wd.setMotSpeed(100,300,100,300)
        sleep_ms(100)
        print('R N,',i)
        
    for i in range(N):
        zy4wd.setMotSpeed(300,100,300,100)
        sleep_ms(100)
        print('L N,',i)
        
   
if __name__ == '__main__':
    zy4wd_mot_spe_test()
    #ZYRot_4WD_PositionTest()
    #ZYRot_4WD_SpeedTest()




