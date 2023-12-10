# 使用位置环和速度环双PID回路控制电机位置和速度
import dcmot_pid_speed_position as motor
from time import sleep_ms, ticks_us, ticks_ms
from machine import Timer, Pin
import zyrot_config as config
import dcmot_pos_spe_dualPID as mot2pid


class ZYRot_2WD_dualPID_obj():
    
    def __init__(self):
        self.paras_dict = {
                    'name'        : 'ZYRot_DPIC_2WD_D41',
                    'hw_version'  : 30,
                    'vxy_scale'   : 6,
                    'vw_scale'    : 2,
                    'wheel_Dia'   : 41,     # 轮直径41mm
                    'wheel_Dist'  : 95,     # 两轮轴距95mm
                                            # 前后轴距离125mm
                    'robot_length' : 130,   # 本体长度130mm
                    'robot_width' : 110,    # 本体宽度110mm
                    }
        if config.ROBOT_NAME != self.paras_dict['name']:
            print("Robot config isn't zyrot_2wd_dualPID")
            raise Exception("Invalid config! Please check file zyrot_config.py .")

        self.init_ms_stamp = ticks_ms()
        
        self.led_p5_r = Pin(5, Pin.OUT, value=0)
        self.led_p18_g = Pin(18, Pin.OUT, value=0)
        self.led_p19_r = Pin(19, Pin.OUT, value=0)
        self.led_p21_g = Pin(21, Pin.OUT, value=0)
        
        self.mot_r = mot2pid.Motor_ABEncoder(m1=12, m2=13, c1=25, c2=26)  #前右轮
        self.mot_l = mot2pid.Motor_ABEncoder(m1=14, m2=27, c1=33, c2=32)  #前左轮

        #m3 = Motor_ABEncoder(m1=18, m2=5, c1=16, c2=17)
        #m4 = Motor_ABEncoder(m1=21, m2=19, c1=23, c2=22)
        
        # Creating PID objects for each motor
        self.pid_speed_r = mot2pid.PID(kp=1.35, kd=0, ki=0.25, uMaxOut=900, tolerance=15,
                 samp_tms = 20, max_interItem=250,dbg_info=0, name='pid_spe_r')
        self.pid_postion_r = mot2pid.PID(kp=1.55, kd=0, ki=0.3, uMaxOut=600, tolerance=10,
                 samp_tms = 100, max_interItem=130,dbg_info=0,name='pid_pos_r')
        self.mot_pid_pos_spe_r = mot2pid.DCmot_PosSpe_Dual_PID(pid_outter=self.pid_postion_r,
                                                       pid_inner=self.pid_speed_r,
                                                       motor=self.mot_r,
                                                       timerId=0, name='dpid_R')
        
        self.pid_speed_l = mot2pid.PID(kp=1.35, kd=0, ki=0.25, uMaxOut=900, tolerance=15,
                 samp_tms = 20, max_interItem=250,dbg_info=0, name='pid_spe_l')
        self.pid_postion_l = mot2pid.PID(kp=1.55, kd=0, ki=0.3, uMaxOut=600, tolerance=10,
                 samp_tms = 100, max_interItem=130,dbg_info=0, name='pid_pos_l')
        self.mot_pid_pos_spe_l = mot2pid.DCmot_PosSpe_Dual_PID(pid_outter=self.pid_postion_l,
                                                       pid_inner=self.pid_speed_l,
                                                       motor=self.mot_l,
                                                       timerId=1, name='dpid_L')
        
#         self.CurX = 0.0
#         self.CurY = 0.0
#         self.CurDirArc = 0.0
#         self.SetX = 0.0
#         self.SetY = 0.0
#         self.SetDirArc = 0.0
        
        self.wheelD = config.WHEEL_D_mm    # 41
        self.wheel_lrDis = config.WHEEL_LR_DIS    #95
        
    def print_info(self):
        print(self.paras_dict)
    
    def end_control(self):
        self.mot_pid_pos_spe_r.end_control()
        self.mot_pid_pos_spe_l.end_control()
       
  
    def setMotMaxPwm(self, pwmr=0,pwml=0):
        self.pid_speed_l.set_maxout(pwml)
        self.pid_speed_r.set_maxout(pwmr)

    def setMotMaxSpeed(self,speed_r=0,speed_l=0):
        self.pid_postion_l.set_maxout(speed_l)
        self.pid_postion_r.set_maxout(speed_r)
  

    def set_dPosYmm(self,dy_mm=0.0):
        l_pos_curr = self.pid_postion_l.get_target()
        r_pos_curr = self.pid_postion_r.get_target()
        self.pid_postion_l.set_target(dy_mm+l_pos_curr)
        self.pid_postion_r.set_target(dy_mm+r_pos_curr)
        self.mot_pid_pos_spe_l.start_control()
        self.mot_pid_pos_spe_r.start_control()

        
    def set_dDirDegree(self, dDirDeg=0.0):
        l_pos_curr = self.pid_postion_l.get_target()
        r_pos_curr = self.pid_postion_r.get_target()
        
        dwheelR = dDirDeg*3.1416/180*self.wheel_lrDis/2   # 取逆时针方向为正角度
        dwheelL = -dwheelR
        
        self.pid_postion_l.set_target(dwheelL + l_pos_curr)
        self.pid_postion_r.set_target(dwheelR + r_pos_curr)
        self.mot_pid_pos_spe_l.start_control()
        self.mot_pid_pos_spe_r.start_control()
        
        
    def setSpeed_Vy_W_Movetime(self,vYmmps=0.0, vWdegps=0.0,
                               move_time_s=0.0, move_mode=config.MOVE_MODE_BLOCK):
        voma = vWdegps*3.1416/180 * self.wheel_lrDis/2
        motor_r_speed = int(vYmmps + voma)    # 逆时针为角速度正方向
        motor_l_speed = int(vYmmps - voma)
        
        l_pos_curr = self.pid_postion_l.get_target()
        r_pos_curr = self.pid_postion_r.get_target()
        
        motor_r_pos = int(r_pos_curr + motor_r_speed * move_time_s)
        motor_l_pos = int(l_pos_curr + motor_l_speed * move_time_s)
        
        self.pid_postion_l.set_target_maxout(motor_l_pos, motor_l_speed)
        self.pid_postion_r.set_target_maxout(motor_r_pos, motor_r_speed)
        self.mot_pid_pos_spe_l.start_control()
        self.mot_pid_pos_spe_r.start_control()
        if (config.LOG_LEVEL & config.MOTOR_POS_LOG):
            print('ms,',ticks_ms() - self.init_ms_stamp,
                  ',LPos,', int(motor_l_pos),
                  ',RPos,', int(motor_r_pos) )
        if ((move_mode == config.MOVE_MODE_BLOCK)and
            (move_time_s >= config.MIN_MOVE_TIME_S)):
            self.mot_pid_pos_spe_l.callback_flag = 0
            self.mot_pid_pos_spe_r.callback_flag = 0
            mv_st_ms = ticks_ms()
            mv_run_ms = 0
            mv_tar_ms = int(move_time_s * 1000 + config.move_add_time_ms)
            while mv_run_ms <= mv_tar_ms:
                mv_run_ms = ticks_ms() - mv_st_ms
                self.mot_pid_pos_spe_l.dual_pid_loop()
                self.mot_pid_pos_spe_r.dual_pid_loop()
            self.urgency_stop()
                
        
        
        
    def release_all_motor(self):
        self.mot_r.release_motor()
        self.mot_l.release_motor()
        
    def urgency_stop(self):
        self.mot_r.breakStop()
        self.mot_l.breakStop()
        
    
    
def ZYRot_2WD_DPID_Test(N=12):
    print('Start ZYRot_2WD_DPID_Test...')
    
    zy2wd = ZYRot_2WD_dualPID_obj()
    
    start_ms = ticks_ms()
    test_step = 0
    for i in range(N):
        run_ms = ticks_ms() - start_ms
        # 以速度200mm/s 前进0.5秒, 即前进100mm
        zy2wd.setSpeed_Vy_W_Movetime(vYmmps=200,vWdegps=0, move_time_s=0.5)
        print('N,' , i , ',run_s,', (ticks_ms()-start_ms)//1000,
              ',L_tar,', zy2wd.pid_postion_l.get_target(),
              ',L_val,', zy2wd.pid_postion_l.get_realvalue(),
              ',R_tar,', zy2wd.pid_postion_r.get_target(),
              ',R_val,', zy2wd.pid_postion_r.get_realvalue() )
        sleep_ms(500)
        # 以速度100mm/s 角速度90deg/s 前进1秒, 即前进100mm同时逆时针转90度
        zy2wd.setSpeed_Vy_W_Movetime(vYmmps=100,vWdegps=90, move_time_s=1)
        print('N,' , i , ',run_s,', (ticks_ms()-start_ms)//1000,
              ',L_tar,', zy2wd.pid_postion_l.get_target(),
              ',L_val,', zy2wd.pid_postion_l.get_realvalue(),
              ',R_tar,', zy2wd.pid_postion_r.get_target(),
              ',R_val,', zy2wd.pid_postion_r.get_realvalue() )
        sleep_ms(500)
        
    zy2wd.end_control()
    zy2wd.release_all_motor()
    print('ZYRot_2WD_DPID_Test over.')

            
if __name__ == '__main__':
    ZYRot_2WD_DPID_Test()


