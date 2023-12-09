from time import sleep_ms, ticks_us, ticks_ms
from DCMot_PID import Motor, PID


class ZY2WD:
    def __init__(self,mL, mR, PidL, PidR, Para):
        self.mleft = mL
        self.mright = mR
        self.pidl = PidL
        self.pidr = PidR
        self.para = Para
        
    def turn_ang_relative(ang_deg=0):
        pass
    
    def move_distance(dis_mm = 0):
        pass
    
    def emerg_stop():
        pass
    
    def get_encoder():
        pass
    
    def get_pos():
        pass
    
    def check_pos():
        pass
    
    def check_angel():
        pass
    
    
    
    def zy2wd_loop():
        pass
        


if __name__ == '__main__':
    print('Start zy2wd test.')
    # Creating objects of each motor
    m1 = Motor(m1=14, m2=27, c1=16, c2=17)
    
    m2 = Motor(m1=12, m2=13, c1=22, c2=23)
    

    # Creating PID objects for each motor
    #p1 = PID(m1, 5, 0.1, 0.001, 800)
    #p1 = PID(M=m1, kp=20, kd=0.2, ki=180, umaxIn=900)    # for speed PID para
    p1 = PID(M=m1, kp=40, kd=0, ki=40, umaxIn=900,tolerance=2,PrintInfo = 0, Name='p1')    # for position PID para
    p2 = PID(M=m2, kp=40, kd=0, ki=40, umaxIn=900,tolerance=2,PrintInfo = 0, Name='p2')
    
    start_ms = ticks_ms()
    test_step = 0

    
    while(1):
        time_ms = ticks_ms()
        run_ms = time_ms - start_ms
        if run_ms <= 3000:
            if test_step ==0:
                test_step = 1
                #p1.setSpeedForPID(100)
                p1.setPositionForPID(100)
                p2.setPositionForPID(100)
        elif run_ms <= 8000:
            if test_step == 1:
                test_step = 2
                #p1.setSpeedForPID(50)
                p1.setPositionForPID(-50)
                p2.setPositionForPID(-50)
        elif run_ms <= 13000:
            if test_step == 2:
                #p1.setSpeedForPID(75)
                p1.setPositionForPID(80)
                p2.setPositionForPID(80)
                test_step = 3
        elif run_ms <= 18000:
            if test_step == 3:
                #p1.setSpeedForPID(75)
                p1.setPositionForPID(-80)
                p2.setPositionForPID(-80)
                test_step = 4
        if run_ms >= 26000:
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
        p2.positionPIDloop()    
    

