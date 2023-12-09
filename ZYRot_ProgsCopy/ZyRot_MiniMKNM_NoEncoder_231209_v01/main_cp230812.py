
'''
import machine
import pwm_motor_test
import umodbus
import uasyncio
import time
from dgram import UDPServer
from beep_music import beep_music_melody
import max7219_8x8led_iosimu as max7219

import zyrot_miniMKNM as miniMKNM
from zyrot_miniMKNM import miniMknmTest

import udpRawProtrol as udprpl
import zyrot_motctl_regs as mctlregs
import zyrot_config as config
# import zyrot_2WD as zy2wd
import zyrot_4WD as zy4wd
import zyrot_arm_4servo as arm4s
import zyrot_4MKNM as zy4mknm

from manual_teach_demo import manual_teach_Demo
from ultra_flow_demo import ultraFlowDemo
from max7219_8x8led_iosimu import disp_num
import hcsr04_irq

import batt_usb_adc
import zyrot_config

rec_cnt = 0
rc_stamp_ms = 0


def cb(msg, addr):
    global rec_cnt
    global rc_stamp_ms
    rec_cnt = rec_cnt+1
    rc_stamp_ms = time.ticks_ms()
    if config.LOG_LEVEL&config.PARSE_LOG > 0:
        print('cnt:', rec_cnt, '++++',time.ticks_ms(),'Got:', msg)
    parsed_vals = udprpl.parse_recv_bytearr(msg)
    if config.LOG_LEVEL&config.PARSE_LOG > 0:
        print('parsed_vals:', parsed_vals)
    if parsed_vals == []:
        return 
    if parsed_vals['fcode'] == udprpl.FCODE_WRITE_REGS:
        mctlregs.set_regs_val(parsed_vals['regNum'][0],parsed_vals['regAddr'][0],parsed_vals['datas'])
#         print(mctlregs.motctl_regs_dict)
#         if config.ROBOT_NAME == zy2wd.zyrot_2WD_paras_dict['name']:
# #             print('udp cb update pwm duty.')
#             zy2wd.update_pwm_duty()
        if config.ROBOT_NAME == zy4wd.zyrot_4WD_paras_dict['name']:
#             print('udp cb update pwm duty.')
            zy4wd.update_pwm_duty()
        if config.ROBOT_NAME == zy4mknm.zyrot_4MKNM_paras_dict['name']:
#             vy = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_Y_REG_ADDR]
#             vx = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_X_REG_ADDR]
#             vw = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_ANGSPE_REG_ADDR]
#             zy4mknm.mknm_update_reg_pwm(vy,vx,vw)
            zy4mknm.mknm_update_regs_pwm(parsed_vals['regNum'][0],parsed_vals['regAddr'][0],parsed_vals['datas'])
#         if config.ARM_TYPE == 'ARM_4X3L_SERVO':
#             arm4s.update_arm_4servo_angle()
        #return 'ack'.encode('bin')
        return parsed_vals['ack_frm_bytearr']
    
    if parsed_vals['fcode'] == udprpl.FCODE_READ_REGS:
        # Todo
        return parsed_vals['ack_frm_bytearr']
        
        

async def print_info():
    while True:
        print('...',time.ticks_ms())
        await uasyncio.sleep_ms(2500)
        
async def print_time():
    while True:
        print('time',time.ticks_ms())
        await uasyncio.sleep_ms(1000)
        

def main():
    global rc_stamp_ms
    print('Enter in main() ticks_ms:', time.ticks_ms())
#     if config.ROBOT_NAME == zy2wd.zyrot_2WD_paras_dict['name']:
#         zy2wd.pwm_init()
#         zy2wd.update_pwm_duty()
    if config.ROBOT_NAME == zy4wd.zyrot_4WD_paras_dict['name']:
        zy4wd.pwm_init()
        zy4wd.update_pwm_duty()
    if config.ROBOT_NAME == zy4mknm.zyrot_4MKNM_paras_dict['name']:
        zy4mknm.pwm_init()
        zy4mknm.update_pwm_duty()
    if config.ARM_TYPE == 'ARM_4X3L_SERVO':
        arm4s.init_arm_4servo()
        
    ap_init()
    time.sleep_ms(500)
    s = UDPServer()
#     l = uasyncio.get_event_loop()
#     l.run_until_complete(s.serve(cb,'0.0.0.0',port))
    #uasyncio.create_task(print_info())
    #uasyncio.create_task(print_time())
    uasyncio.run(s.serve(cb,'0.0.0.0',config.PORT))
    time.sleep_ms（200）
    rc_stamp_ms = time.ticks_ms()
    while True:
        if time.ticks_ms() % 1000 == 0:
            print('main:   ', time.ticks_ms())
        time.sleep_ms(10)
            
        if time.ticks_ms() - rc_stamp_ms >= config.RC_LOST_CONN_TIME_MS:
            if config.ROBOT_NAME == zy4wd.zyrot_4WD_paras_dict['name']:
                zy4wd.clear_pwm_duty()
            if config.ROBOT_NAME == zy4mknm.zyrot_4MKNM_paras_dict['name']:
                zy4mknm.clear_pwm_duty()
    

    
def ap_init():
    print('Begin ap_init() ticks_ms:' , time.ticks_ms())
    import network
    import binascii
    import machine 
    global ap
    
    uid = machine.unique_id()
    idstr = binascii.hexlify(uid).decode()
    idstr_ssid = idstr[-4:]
    
    ap = network.WLAN(network.AP_IF) # create access-point interface
#     ap.config(authmode=3)    # enable ap password
    print('wifi ssid',config.SSID_F+idstr_ssid)
    print('wifi password:',config.PWD)
    ap.config(essid=config.SSID_F+idstr_ssid, password=config.PWD) # set the SSID of the access point
    ap.config(max_clients=2) # set how many clients can connect to the network
    ap.active(True)         # activate the interface

'''
import time
#from zyrot_2wd_obj import zy2wd_mot_spe_test
from dcmot_pos_spe_dualPID import pos_spe_dualPID_test
    
if __name__ == '__main__':
    start_ms = time.ticks_ms()
    print('Boot OK. ms:', start_ms)
#     miniMknmPositionTest()
    # zy2wd_mot_spe_test()
    pos_spe_dualPID_test()
    
'''    
    if zyrot_config.CHARGE_MODE_DEEPSLEEP == True:
        usb_V = batt_usb_adc.get_usb_voltage()
        print('USB voltage:', usb_V)
        max7219.disp_7219_all()
        time.sleep_ms(100)
        max7219.clear_7219() 
        time.sleep_ms(10)
        disp_num(int(usb_V)//100)
        time.sleep_ms(500)
        if usb_V >= zyrot_config.USB_V_ADC_TH:
            for i in range(20):
                print('Wait for deepsleep charge mode...', 20-i)
                disp_num(20-i)
                time.sleep_ms(500)
            print('Enter deepsleep charge mode.')
            max7219.clear_7219()
            time.sleep_ms(100)
            machine.deepsleep()
        
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('Woke from a deep sleep.')
    
    demo_mode = 'Teach'
    max7219.disp_7219_all()
    time.sleep_ms(1000)
    max7219.clear_7219()
    beep_music_melody(8)
    
    disp_time_s = (time.ticks_ms()-start_ms)//1000
    disp_num(int(disp_time_s)%100)
    
    dist_cm = 0
    pre_dist_cm = 0
    edge_rise_cnt = 0
    edge_fall_cnt = 0
    
    dist_high = 16
    max_dist = 80
    dist_low = 12
    min_dist = 6
    
    
    dptr_cnt = 0
    
    
#     pwm_motor_test.pwm_init()
#     pwm_motor_test.pwm_motor_test()
    
#     print('Enter Android wifi remote control mode.')
#     print('Please close 3G/4G/5G data and connect wifi use ZyrotEsp32MC app to control the roobt.')
#     max7219.disp_uppercase_char('R')
#     main()
    
    
    while True:
        time.sleep_ms(10)    
        
        if (demo_mode == 'Teach'):
            print('Enter manual_teach_Demo()')
            manual_teach_Demo()
            demo_mode = 'Flow'
            
        elif (demo_mode == 'Flow'):
            print('Enter ultraFlowDemo()')
            ultraFlowDemo()
            demo_mode = 'Android_RC'
            
        elif (demo_mode == 'Android_RC'):
            # 10 秒后转为Android遥控模式
            print('Enter Android wifi remote control mode.')
            #print('Please close 3G/4G/5G data and connect wifi use ZyrotEsp32MC app to control the roobt.')
            max7219.disp_uppercase_char('R')
            main()
        else :
            print('demo_mode Error!')
    
    
    #pwm_motor_test.pwm_init()
    #pwm_motor_test.pwm_motor_test()
    #zy4mknm.zyrot_4MKNM_test()
    #miniMknmTest()
    #batt_usb_adc.print_voltage()
    
'''
