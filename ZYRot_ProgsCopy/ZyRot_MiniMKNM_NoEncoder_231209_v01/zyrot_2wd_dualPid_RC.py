from machine import Pin,ADC,PWM
import time
from dgram import UDPServer
from beep_music import beep_music_melody, pwm_set_0

import zyrot_utils
import zyrot_2wd_dualPID_obj as mod_zy2wd
import udpRawProtrol as udprpl
import zyrot_config as config
import zyrot_motctl_regs_obj  as mod_ctlregs
import uasyncio

'''
set v_mmps=300, w_degps=30, move_time=1.2s
fa 01 10 00 04 fc 01 fc 20 01 2c 00 1e 04 b0 04 27 fe

set v_mmps=200, w_degps=30, move_time=6s
fa 01 10 00 04 fc 01 fc 20 00 c8 00 1e 17 70 04 95 fe

set v_mmps=200, w_degps=0, move_time=1s
fa 01 10 00 04 fc 01 fc 20 00 c8 00 00 03 e8 04 db fe

set v_mmps=200, w_degps=0, move_time=2s
fa 01 10 00 04 fc 01 fc 20 00 c8 00 00 07 d0 04 c7 fe
'''


class ZYRot_2WD_DualPID_RC():
    
    def __init__(self, zy2wd_dpid_obj, ctlregs_obj):
        self.rec_cnt = 0
        self.parse_cnt = 0
        self.rc_stamp_ms = 0
        self.zy2wd = zy2wd_dpid_obj
        self.ctlregs = ctlregs_obj
        self.msg = None
        self.addr = None
        
    def zy2wd_rc_update_regs(self, regnum, regaddr, vals):
        #self.ctlregs.set_regs_val(regnum,regaddr,vals)
        vy = 0
        vw = 0
        move_t_s = 0.25
        if regaddr == self.ctlregs.FCODE_REG_ADDR_BASE:
            if ((vals[0]&0xffff == self.ctlregs.FCODE_SET_V_W_T) and
                (regnum == 4)):
                vy = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
                vw = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA2]
                move_t_s = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA3]/1000
            elif vals[0]&0xffff == self.ctlregs.FCODE_FORWARD:
                vy = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
            elif vals[0]&0xffff == self.ctlregs.FCODE_BACK:
                vy = -self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
            elif vals[0]&0xffff == self.ctlregs.FCODE_LEFT:
                vw = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
            elif vals[0]&0xffff == self.ctlregs.FCODE_RIGHT:
                vw = -self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
            elif vals[0]&0xffff == self.ctlregs.FCODE_TURN_LEFT:
                vw = self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
            elif vals[0]&0xffff == self.ctlregs.FCODE_TURN_RIGHT:
                vw = -self.ctlregs.motctl_regs_dict[self.ctlregs.FCODE_REG_ADDR_PARA1]
    
#             self.zy2wd.setSpeed_Vy_W_Movetime(vy*self.zy2wd.paras_dict['vxy_scale'],
#                                               vw*self.zy2wd.paras_dict['vw_scale'],
#                                               move_t_s)
            self.zy2wd.setSpeed_Vy_W_Movetime(vy,
                                              vw,
                                              move_t_s) 
                
        elif regaddr == self.ctlregs.JOYSTICK_REG_ADDR_BASE:
            vy = self.ctlregs.motctl_regs_dict[self.ctlregs.JOYSTICK_Y_REG_ADDR]
            vw = self.ctlregs.motctl_regs_dict[self.ctlregs.JOYSTICK_X_REG_ADDR]
            self.zy2wd.setSpeed_Vy_W_Movetime(vy*self.zy2wd.paras_dict['vxy_scale'],
                                              vw*self.zy2wd.paras_dict['vw_scale'],
                                              move_time_s=0.25)
        
    def ap_init(self):
        print('Begin ap_init() ticks_ms:' , time.ticks_ms())
        import network
        import binascii
        import machine 
        #global ap
        
        uid = machine.unique_id()
        idstr = binascii.hexlify(uid).decode()
        idstr_ssid = idstr[-4:]
        
        ap = network.WLAN(network.AP_IF) # create access-point interface
    #     ap.config(authmode=3)    # enable ap password
        print('wifi ssid',config.SSID_F+idstr_ssid)
        print('wifi password:',config.PWD)
        ap.config(essid=config.SSID_F+idstr_ssid, password=config.PWD) # set the SSID of the access point
        ap.config(max_clients=3) # set how many clients can connect to the network
        ap.active(True)         # activate the interface
        
    def dpid_2wd_rc_cb(self, msg, addr):
        self.rec_cnt = self.rec_cnt+1
        self.rc_stamp_ms = time.ticks_ms()
        self.msg = msg
        self.addr = addr
        if config.LOG_LEVEL&config.PARSE_LOG > 0:
            print('cnt:', self.rec_cnt, '++++',time.ticks_ms(),'Got:', msg)
            
        parsed_vals = udprpl.parse_recv_bytearr(self.msg)
                    
        if config.LOG_LEVEL&config.PARSE_LOG > 0:
            print('cnt:', self.rec_cnt, 'parsed_vals:', parsed_vals)
        if parsed_vals == []: 
            return 
        if parsed_vals['fcode'] == udprpl.FCODE_WRITE_REGS:
            self.ctlregs.set_regs_val(parsed_vals['regNum'][0],
                                      parsed_vals['regAddr'][0],
                                      parsed_vals['datas'])
            self.zy2wd_rc_update_regs(parsed_vals['regNum'][0],
                                      parsed_vals['regAddr'][0],
                                      parsed_vals['datas'] )    # 根据遥控参数控制电机运行
            return parsed_vals['ack_frm_bytearr']
        
        if parsed_vals['fcode'] == udprpl.FCODE_READ_REGS:
            if config.LOG_LEVEL > 0:
                print('cnt:', self.rec_cnt, 'udprpl.FCODE_READ_REGS')
            return parsed_vals['ack_frm_bytearr']
            
        
#     def rc_task_parse(self):
#         if (self.rec_cnt - self.parse_cnt) >= 2:
#             if config.LOG_LEVEL&config.PARSE_LOG > 0:
#                 print('rec_cnt:', self.rec_cnt, 'parse_cnt:', self.parse_cnt)
#         if (self.rec_cnt - self.parse_cnt) >= 1:
#             self.parse_cnt = self.rec_cnt
#             
#             parsed_vals = udprpl.parse_recv_bytearr(self.msg)
#             if config.LOG_LEVEL&config.PARSE_LOG > 0:
#                 print('cnt:', self.rec_cnt, 'parsed_vals:', parsed_vals)
#             if parsed_vals == []: 
#                 return 
#             if parsed_vals['fcode'] == udprpl.FCODE_WRITE_REGS:
#                 self.ctlregs.set_regs_val(parsed_vals['regNum'][0],
#                                           parsed_vals['regAddr'][0],
#                                           parsed_vals['datas'])
#                 self.zy2wd_rc_update_regs(parsed_vals['regNum'][0],
#                                           parsed_vals['regAddr'][0],
#                                           parsed_vals['datas'] )    # 根据遥控参数控制电机运行
#                 return parsed_vals['ack_frm_bytearr']
#             
#             if parsed_vals['fcode'] == udprpl.FCODE_READ_REGS:
#                 if config.LOG_LEVEL > 0:
#                     print('cnt:', self.rec_cnt, 'udprpl.FCODE_READ_REGS')
#                 return parsed_vals['ack_frm_bytearr']


def print_time():
    start_ms = time.ticks_ms()
    stamp_ms = time.ticks_ms()
    while True:
        run_ms = time.ticks_ms() - start_ms
        print('task print_time: ', run_ms)
        await uasyncio.sleep_ms(1000)   

        
def print_info(robot):
    start_ms = time.ticks_ms()
    print_s = 0
    while True:
        run_ms = time.ticks_ms() - start_ms
        if print_s != run_ms//1000:
            print_s = run_ms//1000
            print('s,',run_ms/1000,
                  'pos_L,', robot.zy2wd.mot_pid_pos_spe_l.motor.get_pos_mm(),
                  'pos_R,', robot.zy2wd.mot_pid_pos_spe_r.motor.get_pos_mm())
        #robot.rc_task_parse()
        await uasyncio.sleep_ms(500)
        

def zy2wd_dpid_rc_main():
    print('Enter in zy2wd_dpid_rc_main() ticks_ms:', time.ticks_ms())
    pwm_set_0()
    zy2wd_robot = mod_zy2wd.ZYRot_2WD_dualPID_obj()
    zy2wd_regs = mod_ctlregs.ZYRot_motctl_regs_obj()
    zy2wd_rc = ZYRot_2WD_DualPID_RC(zy2wd_robot, zy2wd_regs)
        
    zy2wd_rc.ap_init()
    time.sleep_ms(500)
    s = UDPServer()
    #uasyncio.create_task(print_info(zy2wd_rc))
    #uasyncio.create_task(print_time())
    print('main: after uasyncio.uasyncio.create_task')
    #uasyncio.run(s.serve(zy2wd_rc.dpid_2wd_rc_cb,'0.0.0.0',config.PORT))
    uasyncio.create_task(s.serve(zy2wd_rc.dpid_2wd_rc_cb,'0.0.0.0',config.PORT))
    uasyncio.run(print_info(zy2wd_rc))    
    
    print('main: after uasyncio.run(...)')
    time.sleep_ms(20)
    mainloop_start_ms = time.ticks_ms()
    rc_stamp_ms = time.ticks_ms()
    print_s = mainloop_start_ms
    while True:
        run_ms = time.ticks_ms() - mainloop_start_ms
        if print_s != run_ms//1000:
            print_s = run_ms//1000
            print('main: ', run_ms)
        time.sleep_ms(10)
        zy2wd_rc.rc_task_parse()
#             
#         if time.ticks_ms() - rc_stamp_ms >= config.RC_LOST_CONN_TIME_MS:
#             # 遥控器断连，停止电机
#             print('RC singal lost. stop motor')
#             zy2wd_rc.zy2wd.release_all_motor()
    

if __name__ == '__main__':
    zy2wd_dpid_rc_main()




